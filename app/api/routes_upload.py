from fastapi import APIRouter, File, UploadFile, HTTPException, status
import os

from app.retrieval.vector_store import store_chunks
from app.ingestion.embedder import generate_embeddings
from app.ingestion.chunker import chunk_by_sentence
from app.ingestion.extractor import extract_text

from datetime import date

upload_router = APIRouter()

@upload_router.post('/upload')
async def upload_file(file: UploadFile = File()):
    file_ext = os.path.splitext(file.filename)[1].lower()

    # error handle
    if file_ext not in [".docx",".pdf",".txt"]:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"{file_ext} file type not allowd"
        )

    # make folder upload 
    os.makedirs("/Upload",exist_ok=True)
    # join file path 
    file_path = os.path.join("/Upload",file.filename)

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

        upload_date = date.today().isoformat()

        # store embeddings 
        store_chunks(
            chunks = chunks,
            file_name = file.filename,
            upload_date = upload_date
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error{e}"
        )

    return {
        "file_name":file.filename,
        "page_numbers": len(pages),
        "chunks": len(chunks),
        "upload_date": upload_date
    }