
from app.memory.chat_history import add_message, get_history
from app.rag.generate_answer import answer_query
from openai import OpenAI
from app.tools.tool_schemas import tools, tool_mapping
import json

client = OpenAI()

class BaseAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def tool_calling(self, question: str, history):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": question})
 
        response = client.chat.completions.create(
                model="gpt-5-mini",
                messages = messages,
                tools=tools
            )
        
        message = response.choices[0].message
        if not message.tool_calls:
            return None, []
        
        tool_messages = [message]
        citations = []
        retrieved_chunks = []
        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            tool_function = tool_mapping[call.function.name]
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
            model = "gpt-5-mini",
            messages=[
                *messages,
                *tool_messages,
            ]
        )
        return final_response.choices[0].message.content, citations, retrieved_chunks


    def answer(self, question: str, session_id: str):
        history = get_history(session_id)

        tool_answer, tool_citations, retrieved_chunks = self.tool_calling(question, history)
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