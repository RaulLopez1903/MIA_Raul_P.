import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

from app.chunk import create_chunks, extract_text_from_file
from app.embed import generate_embeddings_batch, generate_embedding
from app.store import add_chunks_to_store, query_similar_chunks, get_store_stats
from app.generate import generate_rag_response

load_dotenv(find_dotenv())

app = FastAPI(
    title="RAG API - Google AI + ChromaDB",
    description="API RAG con ingesta de documentos, almacenamiento vectorial y respuestas ancladas con citas.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Esquemas Pydantic ---
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class Citation(BaseModel):
    id: str
    source: str
    text: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    abstained: bool

# --- Endpoints ---

@app.get("/health", tags=["Estado"])
def health_check():
    stats = get_store_stats()
    return {
        "status": "ok",
        "google_api_key_configured": bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")),
        "chroma_status": "connected",
        "total_chunks_indexed": stats["total_chunks"]
    }

@app.post("/ingest", tags=["Ingesta"])
async def ingest_files(
    files: List[UploadFile] = File(...),
    chunk_size: int = Form(300),
    chunk_overlap: int = Form(50)
):
    """Sube y procesa archivos (.txt, .md, .pdf), genera embeddings e indexa en ChromaDB."""
    if not files:
        raise HTTPException(status_code=400, detail="No se enviaron archivos.")

    temp_dir = "data_temp"
    os.makedirs(temp_dir, exist_ok=True)

    total_docs = len(files)
    all_chunks = []

    try:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extraer y dividir texto
            text = extract_text_from_file(file_path)
            chunks = create_chunks(text, source_name=file.filename, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            all_chunks.extend(chunks)

            os.remove(file_path)

        if not all_chunks:
            return {"message": "No se extrajo texto válido de los archivos.", "documents": total_docs, "chunks_indexed": 0}

        # Generar embeddings e indexar
        texts = [c["text"] for c in all_chunks]
        embeddings = generate_embeddings_batch(texts)
        add_chunks_to_store(all_chunks, embeddings)

        return {
            "message": "Ingesta completada exitosamente.",
            "documents_processed": total_docs,
            "chunks_indexed": len(all_chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la ingesta: {str(e)}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/query", response_model=QueryResponse, tags=["Consulta"])
def query_rag(request: QueryRequest):
    """Consulta el sistema RAG recuperando evidencia de ChromaDB y generando respuesta con Gemini."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    try:
        # 1. Generar embedding de la pregunta
        q_embedding = generate_embedding(request.question)

        # 2. Recuperar vecinos más cercanos
        retrieved = query_similar_chunks(q_embedding, top_k=request.top_k)

        # 3. Generar respuesta anclada con Gemini
        answer, abstained = generate_rag_response(request.question, retrieved)

        # 4. Formatear citas para la respuesta
        citations = [
            Citation(
                id=c["id"],
                source=c["metadata"].get("source", "desconocido"),
                text=c["text"],
                score=c["score"]
            )
            for c in retrieved
        ]

        return QueryResponse(
            answer=answer,
            citations=citations,
            abstained=abstained
        )

    except Exception as e:
        # Requisito: No devolver 500 para fallos de dominio, pero manejar excepciones críticas
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")