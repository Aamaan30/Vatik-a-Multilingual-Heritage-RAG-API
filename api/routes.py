from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.document import IngestRequest, QueryRequest, QueryResponse
from services.rag import ingest_document, query_heritage
from core.database import get_db

router = APIRouter()

@router.post("/ingest", status_code=201)
async def ingest(request: IngestRequest, db: AsyncSession = Depends(get_db)):
    try:
        await ingest_document(request.text, db)
        return {"message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest, db: AsyncSession = Depends(get_db)):
    try:
        answer = await query_heritage(request.query, db)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
