import os
import time
from typing import List
from google import genai
from google.genai import errors
from dotenv import load_dotenv , find_dotenv

load_dotenv(find_dotenv())  # Carga las variables de entorno desde el archivo .env

# Modelo estándar de embeddings de Google AI
EMBEDDING_MODEL = "gemini-embedding-001"

def get_genai_client() -> genai.Client:
    """Instancia y devuelve el cliente oficial de Google GenAI."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno.")
    return genai.Client(api_key=api_key)

def generate_embedding(text: str) -> List[float]:
    """Genera el vector embedding para un solo texto (p. ej., una consulta de usuario)."""
    client = get_genai_client()
    try:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        return response.embeddings[0].values
    except errors.APIError as e:
        raise RuntimeError(f"Error al generar embedding con Google AI: {e}")

def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Genera embeddings por lotes reducidos introduciendo pausas para no exceder cuotas (429)."""
    if not texts:
        return []
        
    client = get_genai_client()
    embeddings = []
    
    # Reducimos tamaño de lote a 5 para evitar picos de quota
    batch_size = 5
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch
            )
            for emb in response.embeddings:
                embeddings.append(emb.values)
                
            # Pausa de 1 segundo entre lotes para no exceder peticiones por minuto (RPM)
            time.sleep(1.0)

        except errors.APIError as e:
            # Si aún así da 429, esperamos 5 segundos y reintentamos el lote
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                time.sleep(5.0)
                response = client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=batch
                )
                for emb in response.embeddings:
                    embeddings.append(emb.values)
            else:
                raise RuntimeError(f"Error en lote de embeddings: {e}")

    return embeddings