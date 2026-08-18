from app.retrieval.vector_store import list_uploaded_document
from langsmith import traceable

@traceable(name="tool list uploaded document", project_name="Intelligent-Company-Knowledge-Assistant")
def tool_list_uploaded_document():
    documents = list_uploaded_document()
    if not documents:
        return "No documents found"
    return documents