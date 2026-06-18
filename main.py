from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import text
import os
from api.routes import router
from core.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup: Create tables and enable vector extension if not exists
    async with engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    yield
    # On shutdown
    pass

app = FastAPI(
    title="Vatik API",
    description="Multilingual Heritage RAG API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def root():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()
