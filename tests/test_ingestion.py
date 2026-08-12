from unittest.mock import MagicMock, patch
import pytest

from app.ingestion.extractor import extract_docx, extract_pdf, extract_text, extract_txt
from app.ingestion.embedder import generate_embeddings

# extract_pdf
def test_extract_pdf_structure():
    result = extract_pdf("sample_docs/leave_policy_pdf.pdf")

    assert isinstance(result, list)
    assert len(result) > 0
    for res in result:
        assert set(res.keys()) == {"page_number", "text"}
        assert isinstance(res["page_number"], int)
        assert isinstance(res["text"], str)
        assert res["text"].strip() != ""


def test_extract_pdf_page_numbers_sequential():
    result = extract_pdf("sample_docs/leave_policy_pdf.pdf")
    page_numbers = [entry["page_number"] for entry in result]

    assert page_numbers == sorted(page_numbers)
    assert page_numbers[0] >= 1


def test_extract_pdf_missing_file():
    with pytest.raises(Exception):
        extract_pdf("sample_docs/does-not-exist.pdf")


# extract_docx
def test_extract_docx_structure():
    result = extract_docx("sample_docs/Finance_KB.docx")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["page_number"] == 1
    assert isinstance(result[0]["text"], str)
    assert result[0]["text"].strip() != ""


def test_extract_docx_missing_file():
    with pytest.raises(Exception):
        extract_docx("sample_docs/does-not-exist.docx")


# extract_txt
def test_extract_txt_structure():
    result = extract_txt("sample_docs/General_Knowledge_KB.txt")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["page_number"] == 1
    assert isinstance(result[0]["text"], str)


def test_extract_txt_missing_file():
    with pytest.raises(FileNotFoundError):
        extract_txt("sample_docs/does-not-exist.txt")


# extract_text (dispatcher)
@pytest.mark.parametrize("filename", [
    "sample_docs/leave_policy_pdf.pdf",
    "sample_docs/leave_policy_pdf.pdf",
    "sample_docs/General_Knowledge_KB.txt",
])
def test_extract_text_dispatches_by_extension(filename):
    result = extract_text(filename)
    assert result != []
    assert isinstance(result, list)


def test_extract_text_unsupported_extension():
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_text("sample_docs/notes.xyz")


# Embeddings Generation Test
@patch("app.ingestion.embedder.client")
def test_generate_embeddings(mock_client):
    fake_embedding_obj = MagicMock()
    fake_embedding_obj.embedding = [0.1] * 1536

    fake_response = MagicMock()
    fake_response.data = [fake_embedding_obj]

    mock_client.embeddings.create.return_value = fake_response

    sample_chunks = [{"chunk_id": "c1", "content": "Sample text"}]
    result = generate_embeddings(sample_chunks)

    assert len(result) == 1
    assert "embedding" in result[0]
    assert len(result[0]["embedding"]) == 1536
