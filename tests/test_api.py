from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db


client = TestClient(app)

# Upload API Tests
@patch("app.api.routes_upload.extract_text")
@patch("app.api.routes_upload.chunk_by_sentence")
@patch("app.api.routes_upload.generate_embeddings")
@patch("app.api.routes_upload.store_chunks")
def test_upload_file(
    mock_store,
    mock_generate,
    mock_chunk,
    mock_extract
):
    mock_extract.return_value = [
        {
            "page_number": 1,
            "text": "Sample policy content"
        }
    ]

    mock_chunk.return_value = [
        {
            "chunk_id": "c1",
            "content": "Sample policy content",
            "page_number": 1
        }
    ]

    mock_generate.return_value = [
        {
            "chunk_id": "c1",
            "content": "Sample policy content",
            "page_number": 1,
            "embedding": [0.1]
        }
    ]

    fake_db = MagicMock()

    # Mock database dependency
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        response = client.post(
            "/upload",
            files={
                "file": (
                    "test.pdf",
                    b"pdf content",
                    "application/pdf"
                )
            },
            data={
                "department": "hr"
            }
        )
        print("STATUS CODE:", response.status_code)
        print("RESPONSE BODY:", response.text)

        assert response.status_code == 200
        assert response.json()["file_name"] == "test.pdf"

    finally:
        app.dependency_overrides.clear()


def test_upload_invalid_file_extension():
    response = client.post(
        "/upload",
        files={
            "file": (
                "test.xyz",
                b"some content",
                "application/octet-stream"
            )
        },
        data={
            "department": "hr"
        }
    )

    assert response.status_code == 404


def test_upload_invalid_department():
    response = client.post(
        "/upload",
        files={
            "file": (
                "test.txt",
                b"sample content",
                "text/plain"
            )
        },
        data={
            "department": "invalid_dept"
        }
    )

    assert response.status_code == 404


# Chat Query API Tests
@patch("app.api.routes_chat.route")
def test_chat_query(mock_route):
    mock_route.return_value = {
        "answer": "Employees are entitled to 12 casual leaves.",
        "citations": [
            {
                "file_name": "HR-Policy.pdf",
                "page_number": 1,
                "chunk_id": "c1",
                "score": 0.95
            }
        ],
        "retrieved_chunks": [
            "Employees are entitled to 12 casual leaves."
        ],
        "agent_used": "hr_agent"
    }

    response = client.post(
        "/query",
        json={
            "question": "How many casual leaves can I take?",
            "session_id": "test_session_1"
        }
    )

    assert response.status_code == 200
    assert "answer" in response.json()
    assert response.json()["agent_used"] == "hr_agent"


# Feedback API Tests
def test_submit_feedback_success():
    fake_db = MagicMock()

    payload = {
        "session_id": "sess_123",
        "question": "What is the leave policy?",
        "retrieved_chunks": ["chunk 1"],
        "final_answer": "12 casual leaves.",
        "feedback": "helpful",
        "timestamp": "2026-08-11T12:00:00"
    }

    # Mock database dependency
    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        response = client.post(
            "/feedback",
            json=payload
        )

        assert response.status_code == 200
        assert response.json()["status"] == "feedback added."

        # Make sure database methods were called
        fake_db.add.assert_called_once()
        fake_db.commit.assert_called_once()

    finally:
        app.dependency_overrides.clear()


def test_feedback_invalid_value():
    payload = {
        "session_id": "sess_123",
        "question": "What is the policy?",
        "retrieved_chunks": ["chunk 1"],
        "final_answer": "Answer text",
        "feedback": "invalid_feedback_type",
        "timestamp": "2026-08-11T12:00:00"
    }

    response = client.post(
        "/feedback",
        json=payload
    )

    assert response.status_code == 400


def test_feedback_invalid_timestamp():
    payload = {
        "session_id": "sess_123",
        "question": "What is the policy?",
        "retrieved_chunks": ["chunk 1"],
        "final_answer": "Answer text",
        "feedback": "helpful",
        "timestamp": "invalid-date-format"
    }

    response = client.post(
        "/feedback",
        json=payload
    )

    assert response.status_code == 400