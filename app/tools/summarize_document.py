from app.retrieval.vector_store import get_chunks_by_file
from openai import OpenAI

client = OpenAI()

def summarize_document(filename: str):
    chunks = get_chunks_by_file(filename=filename)
    if not chunks:
        return f"No document found with the name:{filename}"

    text = ""
    for c in chunks:
        text += c["text"] + "\n"

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                'role':'user',
                'content': f"Summarize following document in 4-5 sentences: \n{text}"
            }
        ]
    )
    return response.choices[0].message.content