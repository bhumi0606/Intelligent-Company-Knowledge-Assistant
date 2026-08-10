from app.agents.base import BaseAgent

agent = BaseAgent(
    name="general_agent",
    system_prompt="""
        You are a general company knowledge assistant. 
        Answer the user's question using only the context provided. 
        Do not use outside knowledge.
        If the context does not contain answer, 
        say: 'I couldn't find information in provided documents.'
"""
)

def answer(question: str, session_id):
    return agent.answer(question, session_id)