import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents",
)

def store_chunks(chunks,file_name, upload_date):

    ids = []
    documents = []
    embeddings = []
    metadatas = []
    for c in chunks:
        ids.append(c["chunk_id"])
        documents.append(c["content"])
        embeddings.append(c["embedding"])
        metadatas.append({
            "file_name": file_name,
            "page_number": c["page_number"],
            "chunk_id": c["chunk_id"],
            "upload_date": upload_date
        })
    
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )