from app.api.routes_upload import upload_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(upload_router)