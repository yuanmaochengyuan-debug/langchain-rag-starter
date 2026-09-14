from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_chain import build_rag_chain


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class SourceInfo(BaseModel):
    file: str
    page: int | None = None
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        chain = build_rag_chain()
        result = chain.invoke({"query": request.question})

        sources = []
        seen = set()

        for doc in result.get("source_documents", []):
            source_path = doc.metadata.get("source", "unknown")
            file_name = Path(source_path).name

            page = doc.metadata.get("page")
            if isinstance(page, int):
                page += 1

            snippet = " ".join(doc.page_content.split())[:180]

            key = (file_name, page, snippet)

            if key not in seen:
                seen.add(key)
                sources.append(
                    SourceInfo(
                        file=file_name,
                        page=page,
                        snippet=snippet,
                    )
                )

        return QueryResponse(
            answer=result["result"],
            sources=sources,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))