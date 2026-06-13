from app.core.config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.gemini_api_key
    )