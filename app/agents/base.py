
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
                messages = messages
                tools=tools
            )
        
        message = response.choices[0].message
        if not message.tool_calls:
            return None
        
        tool_messages = [message]
        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            tool_function = tool_mapping[call.function.name]
            result = tool_function(**args)
            tool_messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, default=str),
            })

        final_response = client.chat.completions.create(
            model = "gpt-5-mini",
            messages=[
                *messages
                *tool_messages,
            ]
        )
        return final_response.choices[0].message.content


    def answer(self, question: str, session_id: str):
        history = get_history(session_id)

        tool_answer = self.tool_calling(question, history)
        if tool_answer is not None:
            return {
                "answer": tool_answer,
                "agent_used": self.name
            }
        else:
            result = answer_query(question, self.system_prompt, history)
            result["agent_used"] = self.name
        
        add_message(session_id, "user", question)
        add_message(session_id, "assistant", result["answer"])

        return result