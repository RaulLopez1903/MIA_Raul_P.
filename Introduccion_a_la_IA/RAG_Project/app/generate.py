import os
from google import genai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_rag_response(question: str, context_chunks: list[dict]) -> dict:
    if not context_chunks:
        return {
            "answer": "No tengo evidencia suficiente en el corpus para responder a esta pregunta.",
            "abstained": True
        }
    
    # Construcción del contexto numerado con citas[cite: 1, 5]
    context_lines = []
    for idx, chunk in enumerate(context_chunks, 1):
        context_lines.append(f"[{idx}] (Fuente: {chunk['source']})\n{chunk['text']}")
    
    context_text = "\n\n".join(context_lines)
    
    # Prompt estricto del curso para evitar alucinaciones[cite: 1, 5]
    contents = f"""Usa solo el siguiente contexto para responder la pregunta en español.
Si el contexto no contiene la respuesta o no es suficiente, responde exactamente: "No tengo evidencia suficiente en el corpus para responder a esta pregunta."
Cita las fuentes usando el formato [1], [2], etc.

Contexto:
{context_text}

Pregunta: {question}
"""

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )

    # Captura limpia del texto evitando partes de pensamiento (como en tu notebook)[cite: 5]
    answer = "".join(
        part.text
        for part in response.candidates[0].content.parts
        if getattr(part, "text", None)
    ).strip()

    abstained = "No tengo evidencia suficiente" in answer or answer == ""

    return {
        "answer": answer,
        "abstained": abstained
    }