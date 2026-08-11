from app.config import EMBEDDING_MODEL
from app.core.openai_client import client

# generate embeddings
def generate_embeddings(chunks):
    text = []
    for c in chunks:
        text.append(c["content"])
    response = client.embeddings.create(
        model = EMBEDDING_MODEL,
        input = text
    )
    
    for chunk, embedding_obj in zip(chunks, response.data):
        chunk["embedding"] = embedding_obj.embedding

    return chunks