from pydantic import BaseModel

class IngestRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
