from dotenv import load_dotenv, find_dotenv
from app.chunk import create_chunks
from app.embed import generate_embeddings_batch, generate_embedding
from app.store import add_chunks_to_store, query_similar_chunks, get_store_stats

load_dotenv(find_dotenv())

# 1. Crear chunks
doc_text = """
FastAPI es un marco web moderno y rápido para construir APIs con Python 3.8+.
ChromaDB es una base de datos de vectores de código abierto ideada para AI.
Gemini 1.5 y 2.0 son modelos de lenguaje avanzados desarrollados por Google AI.
"""

chunks = create_chunks(doc_text, source_name="manual_test.txt", chunk_size=15, chunk_overlap=3)
print(f"Chunks a indexar: {len(chunks)}")

# 2. Generar embeddings
texts = [c["text"] for c in chunks]
embeddings = generate_embeddings_batch(texts)

# 3. Guardar en ChromaDB
add_chunks_to_store(chunks, embeddings)
print("Estadísticas del índice:", get_store_stats())

# 4. Hacer consulta k-NN
question = "¿Qué es ChromaDB?"
question_embedding = generate_embedding(question)
results = query_similar_chunks(question_embedding, top_k=2)

print(f"\nResultados para la pregunta: '{question}'")
for r in results:
    print(f"- ID: {r['id']} | Score: {r['score']}")
    print(f"  Texto: {r['text']}\n")