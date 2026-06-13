import chromadb
from langchain_community.vectorstores import Chroma
from app.services.embedder import get_embeddings
from app.core.config import settings

def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_db_path,
    )