from unittest.mock import MagicMock, patch
import pytest

from app.ingestion.chunker import chunk_by_sentence
from app.retrieval.vector_store import store_chunks, similarity_search, get_chunks_by_file, list_uploaded_document
from app.retrieval.retriever import retrieve

# Chunker Tests
def test_chunk_by_sentence_basic():
    pages = [
        {"page_number": 1, "text": "Employees are entitled to 12 casual leaves per year. Attendance must be logged daily."}
    ]
    chunks = chunk_by_sentence(pages, "HR-Policy.pdf", chunk_size=500, overlap=50)

    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert chunks[0]["file_name"] == "HR-Policy.pdf"
    assert chunks[0]["page_number"] == 1
    assert "content" in chunks[0]
    assert "chunk_id" in chunks[0]


def test_chunk_by_sentence_invalid_args():
    pages = [{"page_number": 1, "text": "Hello world."}]
    with pytest.raises(ValueError):
        chunk_by_sentence(pages, "test.txt", chunk_size=0, overlap=5)

    with pytest.raises(ValueError):
        chunk_by_sentence(pages, "test.txt", chunk_size=10, overlap=20)


# Vector Store & Retriever Tests
@patch("app.retrieval.vector_store.collection")
def test_store_chunks(mock_collection):
    fake_chunk = {
        "chunk_id": "doc_p1_c1",
        "file_name": "policy.pdf",
        "page_number": 1,
        "content": "Sample policy content",
        "embedding": [0.1] * 1536
    }
    
    store_chunks([fake_chunk], "policy.pdf", "2026-08-11")
    assert mock_collection.upsert.called


@patch("app.retrieval.vector_store.collection")
def test_similarity_search(mock_collection):
    mock_collection.query.return_value = {
        "ids": [["doc_p1_c1"]],
        "documents": [["Sample text content"]],
        "metadatas": [[{"chunk_id": "doc_p1_c1", "file_name": "policy.pdf", "page_number": 1, "upload_date": "2026-08-11"}]],
        "distances": [[0.1]]
    }

    results = similarity_search(query_embeddings=[0.1] * 1536, top_k=1)
    assert len(results) == 1
    assert results[0]["file_name"] == "policy.pdf"
    assert results[0]["score"] == 0.9  # 1 - 0.1


@patch("app.retrieval.retriever.generate_query_embeddings")
@patch("app.retrieval.retriever.similarity_search")
def test_retrieve_with_similarity_threshold(mock_similarity, mock_generate_emb):
    mock_generate_emb.return_value = [0.1] * 1536
    mock_similarity.return_value = [
        {"chunk_id": "c1", "text": "Relevant text", "file_name": "policy.pdf", "page_number": 1, "score": 0.8},
        {"chunk_id": "c2", "text": "Irrelevant text", "file_name": "policy.pdf", "page_number": 2, "score": 0.1}
    ]

    results = retrieve("How many leaves?", top_k=2)
    assert len(results) == 1  # Only the score >= 0.35 threshold is kept
    assert results[0]["chunk_id"] == "c1"
