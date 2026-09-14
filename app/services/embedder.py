from langchain_community.embeddings import OllamaEmbeddings


def get_embeddings():
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )