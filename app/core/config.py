from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "rag_collection"

    chunk_size: int = 500
    chunk_overlap: int = 50

    # Retrieval configuration
    retrieval_type: str = "similarity"
    top_k: int = 4

    # MMR configuration
    mmr_fetch_k: int = 12
    mmr_lambda_mult: float = 0.5

    class Config:
        env_file = ".env"


settings = Settings()