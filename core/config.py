import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vatik API"
    DATABASE_URL: str = "postgresql+asyncpg://vatik_user:vatik_password@localhost:5432/vatik_db"
    # GROQ_API_KEY: str = ""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    class Config:
        env_file = ".env"

settings = Settings()
