from fastapi import FastAPI
from app.api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LangChain RAG Starter",
    description="A production-ready RAG pipeline using LangChain + ChromaDB",
    version="0.1.0",
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "RAG API is running. Visit /docs for the API explorer."}