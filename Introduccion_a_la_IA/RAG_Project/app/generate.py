from typing import List, Dict, Any, Tuple
from google.genai import errors
from app.embed import get_genai_client

GENERATION_MODEL = "gemini-3.6-flash"  # O gemini-1.5-flash según disponibilidad
SCORE_THRESHOLD = 0.35  # Umbral mínimo de similitud para considerar relevante un chunk

def generate_rag_response(
    question: str, 
    retrieved_chunks: List[Dict[str, Any]]
) -> Tuple[str, bool]:
    """
    Genera una respuesta anclada al contexto usando Gemini.
    Devuelve (respuesta, abstained_flag).
    """
    # 1. Filtro por umbral de score mínimo
    relevant_chunks = [c for c in retrieved_chunks if c.get("score", 0) >= SCORE_THRESHOLD]

    if not relevant_chunks:
        return (
            "No tengo evidencia suficiente en los documentos para responder a tu pregunta.",
            True
        )

    # 2. Formatear el contexto con numeración explícita [1], [2], ...
    context_text = ""
    for idx, chunk in enumerate(relevant_chunks, start=1):
        source = chunk.get("metadata", {}).get("source", "Desconocido")
        context_text += f"[{idx}] (Fuente: {source}):\n{chunk['text']}\n\n"

    # 3. Prompt estricto de anclaje (Groundedness)
    prompt = f"""
Eres un asistente RAG preciso. Tu única tarea es responder a la PREGUNTA usando EXCLUSIVAMENTE la información de los FRAGMENTOS DE EVIDENCIA provistos.

REGLAS STRICTAS:
1. Responde siempre en español.
2. Basate ÚNICAMENTE en la evidencia proporcionada. No uses conocimiento externo.
3. Cita tus fuentes dentro del texto usando la notación [1], [2], etc., correspondiente al fragmento de donde obtuviste el dato.
4. Si la evidencia NO contiene la respuesta o no es suficiente, debes responder EXACTAMENTE: "No tengo evidencia suficiente en los documentos para responder a tu pregunta." No intentes adivinar ni responder parcialmente.

FRAGMENTOS DE EVIDENCIA:
{context_text}

PREGUNTA:
{question}

RESPUESTA:
"""

    client = get_genai_client()
    try:
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt
        )
        answer = response.text.strip()
        
        # Evaluar si la respuesta fue una abstención explícita
        abstained = "no tengo evidencia suficiente" in answer.lower()
        
        return answer, abstained

    except errors.APIError as e:
        raise RuntimeError(f"Error al generar respuesta con Gemini: {e}")