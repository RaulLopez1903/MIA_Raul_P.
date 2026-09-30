import os
from typing import List, Dict, Any
from pypdf import PdfReader

def extract_text_from_file(file_path: str) -> str:
    """Extrae el contenido de texto plano desde archivos .txt, .md o .pdf."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in [".txt", ".md"]:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
            
    elif ext == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
        
    else:
        raise ValueError(f"Formato no soportado: {ext}")

def create_chunks(
    text: str, 
    source_name: str, 
    chunk_size: int = 300, 
    chunk_overlap: int = 50
) -> List[Dict[str, Any]]:
    """
    Divide el texto en chunks por palabras con un solape (overlap) configurable.
    
    Args:
        text: El texto completo del documento.
        source_name: Nombre del archivo origen para metadatos.
        chunk_size: Número promedio de palabras por chunk.
        chunk_overlap: Número de palabras compartidas entre chunks consecutivos.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    chunk_idx = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "id": f"{source_name}_chunk_{chunk_idx}",
            "text": chunk_text,
            "metadata": {
                "source": source_name,
                "chunk_index": chunk_idx,
                "word_count": len(chunk_words)
            }
        })

        chunk_idx += 1
        # Avanzar considerando el overlap
        start += (chunk_size - chunk_overlap)
        
        # Evitar bucles infinitos si chunk_overlap >= chunk_size
        if chunk_size <= chunk_overlap:
            start += chunk_size

    return chunks