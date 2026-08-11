from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:str
    SIMILARITY_THRESHOLD: float
    CHAT_MODEL: str
    EMBEDDING_MODEL: str
    TOP_K: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    UPLOAD_DIR: str
    
    model_config = {
        "env_file": ".env"
    }

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
SIMILARITY_THRESHOLD = settings.SIMILARITY_THRESHOLD
CHAT_MODEL = settings.CHAT_MODEL
EMBEDDING_MODEL = settings.EMBEDDING_MODEL
TOP_K = settings.TOP_K
CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP
UPLOAD_DIR = settings.UPLOAD_DIR