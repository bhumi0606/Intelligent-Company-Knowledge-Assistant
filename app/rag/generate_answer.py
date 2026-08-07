from typing import List
from openai import OpenAI

from app.retrieval.retriever import retrieve
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
default_system_prompt = """ You are a company knowledge assistant. 
                    Answer the user's question using only the information given in context below. 
                    Do not use any outside knowledge. 
                    If the context does not contain answer, 
                    say: 'I couldn't find information in provided documents.'"""

def create_context(chunks):
    context = []
    for c in chunks:
        context.append(
            f"[filename: {c['file_name']}, Page {c['page_number']}]\n{c['text']}"
        )

    return "\n".join(context)

def generate_answer(
        query: str,
        chunks: List[dict],
        system_prompt: str = default_system_prompt
):
    context = create_context(chunks)
    user_prompt = f"context: {context}, Question: {query}"
    
    response = client.chat.completions.create(
        model = "gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content


def answer_query(query: str, system_prompt: str = default_system_prompt,top_k: int = 5):
    chunks = retrieve(query,top_k)

    if not chunks:
        return {"answer":"No information"}

    answer = generate_answer(query, chunks, system_prompt)
    return answer
