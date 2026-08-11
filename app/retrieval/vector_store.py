from typing import List

import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
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

def similarity_search(query_embeddings: List[float], top_k: int = 5):
    results = collection.query(
        query_embeddings = [query_embeddings],
        n_results = top_k
    )
    matches = []
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, chunk_id in enumerate(ids):
        metadata = metadatas[i]
        matches.append(
            {
                "chunk_id": metadata["chunk_id"],
                "text": documents[i],
                "file_name": metadata["file_name"],
                "page_number": metadata["page_number"],
                "upload_date": metadata["upload_date"],
                "score": 1 - distances[i]
            }
        )

    return matches

def get_chunks_by_file(filename: str):
    result = collection.get(
        where={"file_name":filename}
    )

    chunks = []
    for i in range(len(result["ids"])):
        metadata = result["metadatas"][i]
        chunks.append({
            "chunk_id": metadata["chunk_id"],
            "text": result["documents"][i],
            "page_number": metadata["page_number"]
        })
    return chunks

def list_uploaded_document():
    result = collection.get(
        include=["metadatas"]
    )
    documents = set()
    for metadata in result["metadatas"]:
        documents.add(metadata["file_name"])

    return documents