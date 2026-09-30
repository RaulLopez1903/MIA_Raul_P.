import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

# Ruta local para persistencia en disco
CHROMA_DATA_PATH = os.path.join(os.getcwd(), "chroma")
COLLECTION_NAME = "rag_documents"

def get_chroma_client() -> chromadb.PersistentClient:
    """Instancia el cliente de ChromaDB persistente en disco."""
    return chromadb.PersistentClient(path=CHROMA_DATA_PATH)

def get_or_create_collection():
    """Obtiene o crea la colección en ChromaDB."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"} # Usar similitud cosenoidal
    )

def add_chunks_to_store(chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
    """
    Guarda los chunks y sus vectores calculados por Google AI en ChromaDB.
    """
    if not chunks or not embeddings:
        return

    collection = get_or_create_collection()

    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    # Insertar o actualizar
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def query_similar_chunks(query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Busca los top-k chunks más parecidos al vector de la pregunta.
    """
    collection = get_or_create_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    formatted_results = []
    if results and results["ids"] and results["ids"][0]:
        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for idx, doc, meta, dist in zip(ids, docs, metas, distances):
            # Convertir distancia cosenoidal a score de similitud (0 a 1)
            similarity_score = round(1.0 - dist, 4)
            formatted_results.append({
                "id": idx,
                "text": doc,
                "metadata": meta,
                "score": similarity_score
            })

    return formatted_results

def get_store_stats() -> Dict[str, Any]:
    """Retorna estadísticas básicas del índice."""
    collection = get_or_create_collection()
    return {
        "total_chunks": collection.count(),
        "collection_name": COLLECTION_NAME
    }