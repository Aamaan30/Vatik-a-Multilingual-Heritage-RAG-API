# Vatik Heritage RAG API

A production-grade RESTful API for a Multilingual Heritage RAG (Retrieval-Augmented Generation) system.

## Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL with `pgvector`
- **ORM:** SQLAlchemy (Async)
- **AI Orchestration:** LangChain
- **Embeddings:** Hugging Face (`sentence-transformers/all-MiniLM-L6-v2`)
- **LLM Inference:** Groq API (`llama-3.1-8b-instant`)

## Getting Started

### Prerequisites
1. Ensure you have Docker and Docker Compose installed (if running via Docker).
2. Install Python 3.11+.

### Environment Setup
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
```

### Running Locally
To run the application natively on your machine:
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python manage.py run
```
The FastAPI server and the beautifully styled web frontend will be available at `http://localhost:8000/`.

### Running with Docker
```bash
docker-compose up --build
```

## Features
- **Semantic Data Ingestion**: Insert new historical context into the vector database via the web interface.
- **AI Explorer**: Ask questions about the ingested heritage documents and receive markdown-formatted answers synthesized by Llama 3.
