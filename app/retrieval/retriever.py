from typing import Optional

from openai import OpenAI
from app.retrieval.vector_store import similarity_search
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def generate_query_embeddings(query: str):
    response = client.embeddings.create(
            model = "text-embedding-3-small",
            input = [query]
        )

    return response.data[0].embedding

def retrieve(
        query: str,
        top_k: int = 5,
        document_filter: str = Optional[None]
):
    query_embedding = generate_query_embeddings(query)
    results = similarity_search(
        query_embeddings = query_embedding,
        top_k = top_k
    )

    if not results:
        return []

    return results