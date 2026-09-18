from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from app.chunk import chunk_text
from app.store import add_chunks_to_db, query_similar_chunks
from app.generate import generate_rag_response

app = FastAPI(title="RAG API")

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API activa y lista"}

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    chunks = chunk_text(content)
    add_chunks_to_db(chunks, source_name=file.filename)
    return {"status": "success", "filename": file.filename, "chunks_indexed": len(chunks)}

@app.post("/query")
def query_rag(req: QueryRequest):
    chunks = query_similar_chunks(req.question, top_k=req.top_k)
    result = generate_rag_response(req.question, chunks)
    return {
        "answer": result["answer"],
        "abstained": result["abstained"],
        "citations": chunks
    }