from openai import OpenAI
from dotenv import load_dotenv

from app.agents.hr_agent import answer as hr_answer
from app.agents.it_agent import answer as it_answer
from app.agents.finance_agent import answer as finance_answer
from app.agents.general_agent import answer as general_answer

load_dotenv()
client = OpenAI()

def create_intent_prompt(question: str):
    intent_prompt = f"""
        Classify the following user question into exactly one category:
        hr, it, finance, or general
        - hr: Leave policy, Attendance, Holidays, Payroll, Employee benefits
        - it: VPN, Password reset, Software installation, Laptop requests, Email setup
        - finance: Expense claims, Travel reimbursemen, Invoice process, Company reimbursements
        - general: anything else
        Respond with only the single category word, nothing else
        Question:{question}
        """
    return intent_prompt

def detect_intent(question: str):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages = [
            {
                "role":"user",
                "content": create_intent_prompt(question)
            }
        ]
    )

    category = response.choices[0].message.content.strip().lower()

    if category not in ["hr", "it", "finance", "general"]:
        return "general"
    return category

def route(question: str):
    intent = detect_intent(question)
    if intent == "hr":
        return hr_answer(question)
    if intent == "it":
        return it_answer(question)
    if intent == "finance":
        return finance_answer(question)
    if intent == "general":
        return general_answer(question)