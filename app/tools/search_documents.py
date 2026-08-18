from app.config import TOP_K
from app.retrieval.retriever import retrieve
from typing import Optional
from langsmith import traceable

@traceable(name="search document", project_name="Intelligent-Company-Knowledge-Assistant")
def search_document(
    query: str,
    top_k: int = TOP_K,
    document_filter: Optional[str] = None
):
    return retrieve(
        query= query,
        top_k = top_k,
        document_filter = document_filter
    )