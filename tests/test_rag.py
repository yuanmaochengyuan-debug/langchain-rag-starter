from app.core.config import settings
from app.services.embedder import get_embeddings

def test_settings_load():
    assert settings.llm_provider in ["gemini", "openai"]

def test_embeddings_init():
    embeddings = get_embeddings()
    assert embeddings is not None