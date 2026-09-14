from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama

from app.core.config import settings
from app.core.prompts import RAG_PROMPT
from app.services.vectorstore import get_vectorstore


def get_llm():
    return ChatOllama(
        model="qwen2.5:3b",
        base_url="http://localhost:11434",
        temperature=0.3,
    )


def build_retriever():
    vectorstore = get_vectorstore()

    if settings.retrieval_type == "mmr":
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": settings.top_k,
                "fetch_k": settings.mmr_fetch_k,
                "lambda_mult": settings.mmr_lambda_mult,
            },
        )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": settings.top_k,
        },
    )


def build_rag_chain() -> RetrievalQA:
    retriever = build_retriever()

    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": RAG_PROMPT},
        return_source_documents=True,
    )