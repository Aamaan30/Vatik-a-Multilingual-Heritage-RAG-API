from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    # 384 is the embedding dimension for sentence-transformers/all-MiniLM-L6-v2
    embedding = Column(Vector(384))
