from typing import Optional

from app.config import EMBEDDING_MODEL, SIMILARITY_THRESHOLD, TOP_K
from app.retrieval.vector_store import similarity_search
from app.core.openai_client import client
from langsmith import traceable

# generate embeddings of query
def generate_query_embeddings(query: str):
    response = client.embeddings.create(
            model = EMBEDDING_MODEL,
            input = [query]
        )

    return response.data[0].embedding

# retrieve chunks 

@traceable(name="retrieve chunks", project_name="Intelligent-Company-Knowledge-Assistant")
def retrieve(
        query: str,
        top_k: int = TOP_K,
        document_filter: Optional[str] = None
):
    query_embedding = generate_query_embeddings(query)
    results = similarity_search(
        query_embeddings = query_embedding,
        top_k = top_k
    )

    if not results:
        return []

    filtered_results = []

    for chunk in results:
        if chunk["score"] >= SIMILARITY_THRESHOLD:
            filtered_results.append(chunk)

    return filtered_results