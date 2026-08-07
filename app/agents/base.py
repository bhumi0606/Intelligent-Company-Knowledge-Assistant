
from app.rag.generate_answer import answer_query


class BaseAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

    def answer(self, question: str):
        result = answer_query(question, self.system_prompt)
        return result