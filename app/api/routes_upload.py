from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Form
import os

from app.config import UPLOAD_DIR
from app.db.database import get_db
from app.db.models import Document
from app.retrieval.vector_store import store_chunks
from app.ingestion.embedder import generate_embeddings
from app.ingestion.chunker import chunk_by_sentence
from app.ingestion.extractor import extract_text

from datetime import datetime
from sqlalchemy.orm import Session

upload_router = APIRouter()

@upload_router.post('/upload')
async def upload_file(file: UploadFile = File(), department: str = Form(), db: Session = Depends(get_db)):
    file_ext = os.path.splitext(file.filename)[1].lower()

    # error handle
    if file_ext not in [".docx",".pdf",".txt"]:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"{file_ext} file type not allowed"
        )

    if department not in ["hr", "it", "finance", "general"]:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"{department} department not allowed"
        )

    # make folder upload 
    os.makedirs(UPLOAD_DIR,exist_ok=True)
    # join file path 
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    print("FilePath:", file_path)
    # save file contents into file
    
    content = await file.read()
    with open(file_path,"wb") as f:
        f.write(content)

    try:
        # extract file
        pages = extract_text(file_path)
        if not pages:
            raise HTTPException(
                status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail = "No text found in file"
            )

        # split into chunks
        chunks = chunk_by_sentence(
            pages = pages,
            file_name = file.filename
        )

        # generate embeddings
        chunks = generate_embeddings(
            chunks = chunks
        )
        upload_time = datetime.utcnow()
        upload_date = upload_time.date().isoformat()

        # store embeddings 
        store_chunks(
            chunks = chunks,
            file_name = file.filename,
            upload_date = upload_date
        )

        doc_row = Document(file_name=file.filename, upload_date=upload_time, department=department)
        db.add(doc_row)
        db.commit()
        db.refresh(doc_row)

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error{e}"
        )

    return {
        "document_id": doc_row.id,
        "file_name":file.filename,
        "department": department,
        "page_numbers": len(pages),
        "chunks": len(chunks),
        "upload_date": upload_date
    }