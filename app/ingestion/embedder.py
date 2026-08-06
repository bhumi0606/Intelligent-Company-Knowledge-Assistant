
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# generate embeddings
def generate_embeddings(chunks):
    chunk = []
    for c in chunks:
        chunk.append(c["content"])
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = chunk
    )
    return response.data[0].embedding