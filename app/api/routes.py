from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_chain import build_rag_chain

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        chain = build_rag_chain()
        result = chain.invoke({"query": request.question})
        sources = [
            doc.metadata.get("source", "unknown")
            for doc in result.get("source_documents", [])
        ]
        return QueryResponse(answer=result["result"], sources=list(set(sources)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))