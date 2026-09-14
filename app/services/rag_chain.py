from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama

from app.core.prompts import RAG_PROMPT
from app.services.vectorstore import get_vectorstore


def get_llm():
    return ChatOllama(
        model="qwen2.5:3b",
        base_url="http://localhost:11434",
        temperature=0.3,
    )


def build_rag_chain() -> RetrievalQA:
    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )

    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": RAG_PROMPT},
        return_source_documents=True,
    )