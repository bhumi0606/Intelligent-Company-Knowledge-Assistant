
from app.config import CHAT_MODEL
from app.memory.chat_history import add_message, get_history
from app.rag.generate_answer import answer_query
from app.tools.tool_schemas import tools, tool_mapping
import json
import inspect

from app.core.openai_client import client
from langsmith import traceable

class BaseAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    # check if tool is needed and execute the tool
    @traceable(name="Tool calling", project_name="Intelligent-Company-Knowledge-Assistant")
    async def tool_calling(self, question: str, history):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": question})
 
        response = client.chat.completions.create(
                model=CHAT_MODEL,
                messages = messages,
                tools=tools
            )
        
        message = response.choices[0].message
        if not message.tool_calls:
            return None, [], []
        
        tool_messages = [message]
        citations = []
        retrieved_chunks = []
        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            tool_function = tool_mapping[call.function.name]
            if inspect.iscoroutinefunction(tool_function):
                result = await tool_function(**args)    
            else:
                result = tool_function(**args)
            if call.function.name == "search_document" and result:
                for c in result:
                    retrieved_chunks.append(c["text"])
                    citations.append(
                        {
                            "file_name": c["file_name"],
                            "page_number": c["page_number"],
                            "chunk_id": c["chunk_id"],
                            "score": c["score"],
                        }
                )
 
            tool_messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, default=str),
            })

        final_response = client.chat.completions.create(
            model = CHAT_MODEL,
            messages=[
                *messages,
                *tool_messages,
            ]
        )
        return final_response.choices[0].message.content, citations, retrieved_chunks

    # answer the user's question
    @traceable(name="Agent Answer", project_name="Intelligent-Company-Knowledge-Assistant")
    async def answer(self, question: str, session_id: str):
        history = get_history(session_id)
        history = history[-3:]
        tool_answer, tool_citations, retrieved_chunks = await self.tool_calling(question, history)
        if tool_answer is not None:
            return {
                "answer": tool_answer,
                "citations": tool_citations,
                "retrieved_chunks": retrieved_chunks,
                "agent_used": self.name
            }
        else:
            result = answer_query(
                query=question,
                system_prompt=self.system_prompt,
                history=history
            )
            result["agent_used"] = self.name
        add_message(session_id, "user", question)
        add_message(session_id, "assistant", result["answer"])

        return result