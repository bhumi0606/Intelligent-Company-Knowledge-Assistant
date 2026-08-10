from app.retrieval.retriever import retrieve
from typing import Optional

def search_document(
    query: str,
    top_k: int = 5,
    document_filter: str = Optional[None]
):
    return retrieve(
        query= query,
        top_k = top_k,
        document_filter = document_filter
    )