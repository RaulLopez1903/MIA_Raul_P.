# Sistema RAG con Streamlit + FastAPI + ChromaDB + Google AI

Este proyecto implementa una solución completa de Generación Aumentada por Recuperación (RAG) utilizando FastAPI como capa de API REST, ChromaDB como base de datos vectorial persistente, Google AI para embeddings (`gemini-embedding-001`) y generación anclada (`gemini-3.6-flash`), y Streamlit como interfaz gráfica.

## Requisitos previos

- Python 3.10+
- Una clave de API de Google AI Studio (`GEMINI_API_KEY`)

## Instalación

1. Crear y activar el entorno virtual:

```bash
   python3 -m venv venv
   # En Windows:
   .\venv\Scripts\Activate.ps1
   # En Linux/macOS:
   source venv/bin/activate
```

2. Instalar dependencias:
```bash
python -m pip install -r requirements.txt

```


3. Configurar variables de entorno:
Copiar `.env.example` como `.env` y definir la clave de API:
```env
GEMINI_API_KEY=api_key
```


## Ejecución del proyecto

Para levantar el sistema es necesario ejecutar la API y la UI en terminales separadas:

### 1. Iniciar servidor FastAPI (Backend)

```bash
uvicorn app.main:app --reload --port 8000

```

* Documentación interactiva de Swagger: `http://localhost:8000/docs`
* Estado de la API: `http://localhost:8000/health`

### 2. Iniciar cliente Streamlit (Frontend)

```bash
streamlit run ui/streamlit_app.py

```

* Acceso a la UI en el navegador: `http://localhost:8501`

## Criterio de Abstención

El sistema filtra los fragmentos recuperados con un umbral de similitud cosenoidal mínimo (`SCORE_THRESHOLD = 0.35`). Si ningún fragmento supera dicho score o si el contexto no contiene evidencia directa sobre la consulta, el sistema devuelve `abstained: true` y se abstiene de responder mediante una plantilla estricta de instrucción a Gemini.
