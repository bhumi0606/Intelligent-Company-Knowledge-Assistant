from app.api.routes_upload import upload_router
from app.api.routes_chat import chat_router

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(upload_router)
app.include_router(chat_router)