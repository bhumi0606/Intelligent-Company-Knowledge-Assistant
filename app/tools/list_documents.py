from app.retrieval.vector_store import list_uploaded_document

def tool_list_uploaded_document():
    documents = list_uploaded_document()
    if not documents:
        return "No documents found"
    return documents