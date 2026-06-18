import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pgvector.sqlalchemy import Vector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.document import Document
from core.config import settings

# Initialize Embeddings model
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    groq_api_key=settings.GROQ_API_KEY
)

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful assistant for answering questions about heritage based on the provided context.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question:
{question}

Answer:"""
)

chain = prompt_template | llm | StrOutputParser()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

async def ingest_document(text: str, db: AsyncSession):
    # Chunk the text
    chunks = text_splitter.split_text(text)
    
    # Generate embeddings and save to DB
    for chunk in chunks:
        vector = embeddings_model.embed_query(chunk)
        db_doc = Document(content=chunk, embedding=vector)
        db.add(db_doc)
        
    await db.commit()

async def query_heritage(query: str, db: AsyncSession) -> str:
    # 1. Generate embedding for query
    query_vector = embeddings_model.embed_query(query)
    
    # 2. Perform vector similarity search in DB
    # Using cosine distance
    stmt = select(Document).order_by(Document.embedding.cosine_distance(query_vector)).limit(3)
    result = await db.execute(stmt)
    docs = result.scalars().all()
    
    # 3. Retrieve context
    context = "\n\n".join([doc.content for doc in docs])
    
    # 4. Pass context to Groq API
    answer = await chain.ainvoke({"context": context, "question": query})
    return answer
