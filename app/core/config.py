from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str = ""
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "rag_collection"
    chunk_size: int = 500
    chunk_overlap: int = 50

    class Config:
        env_file = ".env"

settings = Settings()