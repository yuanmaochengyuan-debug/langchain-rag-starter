from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.core.prompts import RAG_PROMPT
from app.services.vectorstore import get_vectorstore

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=settings.gemini_api_key,
        temperature=0.3,
    )

def build_rag_chain() -> RetrievalQA:
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": RAG_PROMPT},
        return_source_documents=True,
    )