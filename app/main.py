from app.api.routes_upload import upload_router
from app.api.routes_chat import chat_router
from app.api.routes_feedback import feedback_router
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

app = FastAPI()

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(feedback_router)