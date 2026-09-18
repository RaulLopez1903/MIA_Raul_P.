import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# Clase de Embedding idéntica a la vista en la clase 04 del curso[cite: 5]
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        response = gemini_client.models.embed_content(
            model="gemini-embedding-001",
            contents=input,
        )
        return [embedding.values for embedding in response.embeddings]

gemini_ef = GeminiEmbeddingFunction()

# Persistencia tal como se trabajó en las notebooks[cite: 5]
client = chromadb.PersistentClient(path="./chroma_gemini")
collection = client.get_or_create_collection(
    name="rag_collection",
    embedding_function=gemini_ef,
)

def add_chunks_to_db(chunks: list[str], source_name: str):
    documents = chunks
    metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]
    ids = [f"{source_name}_chunk_{i}" for i in range(len(chunks))]
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def query_similar_chunks(query_text: str, top_k: int = 3):
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )
    
    formatted_results = []
    if results["documents"] and len(results["documents"][0]) > 0:
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "score": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
            })
    return formatted_results