from app.agents.base import BaseAgent

agent = BaseAgent(
    name = "hr_agent",
    system_prompt = """ 
        You are the HR assistant for a company knowledge base. 
        Answer questions about leave policy, attendance, holidays, payroll, and employee benefits using only the context provided. 
        Do not use outside knowledge.
        If the context does not contain answer, 
        say: 'I couldn't find information in provided documents.'
    """
)

def answer(question: str, session_id):
    return agent.answer(question, session_id)