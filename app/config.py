from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:str
    SIMILARITY_THRESHOLD: float
    
    model_config = {
        "env_file": ".env"
    }

settings = Settings()

DATABASE_URL = settings.DATABASE_URL
SIMILARITY_THRESHOLD = settings.SIMILARITY_THRESHOLD