
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# generate embeddings
def generate_embeddings(chunks):
    text = []
    for c in chunks:
        text.append(c["content"])
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = text
    )
    
    for chunk, embedding_obj in zip(chunks, response.data):
        chunk["embedding"] = embedding_obj.embedding

    return chunks