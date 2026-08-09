
from app.agents.base import BaseAgent

agent = BaseAgent(
    name="finance_agent",
    system_prompt="""
        You are the Finance assistant for a company knowledge base.
        Answer questions about Expense claims, Travel reimbursement and Invoice process, Company reimbursements using only the context provided. 
        Do not use outside knowledge.
        If the context does not contain answer, 
        say: 'I couldn't find information in provided documents.'
"""
)

def answer(question: str):
    return agent.answer(question)