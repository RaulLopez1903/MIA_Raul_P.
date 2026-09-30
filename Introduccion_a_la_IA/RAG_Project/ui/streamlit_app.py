import streamlit as st
import httpx

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RAG System — Google AI & ChromaDB",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Sistema RAG: Generación Aumentada por Recuperación")
st.caption("Cliente Streamlit interactuando con la API de FastAPI (ChromaDB + Google AI)")

# Verificar conectividad con la API
@st.cache_data(ttl=5)
def check_api_health():
    try:
        response = httpx.get(f"{API_BASE_URL}/health", timeout=3.0)
        return response.status_code == 200, response.json()
    except Exception:
        return False, {}

api_online, health_data = check_api_health()

if not api_online:
    st.error("⚠️ La API de FastAPI no está disponible en http://localhost:8000. Asegúrate de iniciar `uvicorn app.main:app --reload`.")
    st.stop()
elif not health_data.get("google_api_key_configured"):
    st.warning("⚠️ La API está activa pero la clave de Google AI (`GEMINI_API_KEY`) no está configurada en el archivo `.env`.")

# Sidebar: Configuración e Ingesta
with st.sidebar:
    st.header("⚙️ Estado del Sistema")
    st.success(f"API Online | Chunks indexados: **{health_data.get('total_chunks_indexed', 0)}**")
    
    st.divider()
    st.header("📥 Ingesta de Documentos")
    uploaded_files = st.file_uploader(
        "Sube archivos (.txt, .md, .pdf)", 
        type=["txt", "md", "pdf"], 
        accept_multiple_files=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        chunk_size = st.number_input("Chunk size", min_value=50, max_value=1000, value=300, step=50)
    with col2:
        chunk_overlap = st.number_input("Overlap", min_value=0, max_value=200, value=50, step=10)

    if st.button("Procesar e Indexar", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Selecciona al menos un archivo primero.")
        else:
            with st.spinner("Procesando documentos, generando embeddings e indexando..."):
                files_payload = [
                    ("files", (f.name, f.getvalue(), f.type or "application/octet-stream"))
                    for f in uploaded_files
                ]
                data_payload = {
                    "chunk_size": str(chunk_size),
                    "chunk_overlap": str(chunk_overlap)
                }
                
                try:
                    res = httpx.post(f"{API_BASE_URL}/ingest", files=files_payload, data=data_payload, timeout=60.0)
                    if res.status_code == 200:
                        result = res.json()
                        st.success(f"¡Éxito! {result.get('chunks_indexed')} chunks creados desde {result.get('documents_processed')} documento(s).")
                        st.rerun()
                    else:
                        st.error(f"Error en ingesta: {res.text}")
                except Exception as e:
                    st.error(f"Error al conectar con la API: {str(e)}")

# Sección Principal: Chat / Consulta
st.subheader("❓ Realizar Consulta")

top_k = st.slider("Número de fragmentos a recuperar (top-k)", min_value=1, max_value=10, value=3)
question = st.text_input("Escribe tu pregunta sobre los documentos indexados:", placeholder="Ej. ¿De qué trata el documento X?")

if st.button("Buscar Respuesta", type="primary"):
    if not question.strip():
        st.warning("Escribe una pregunta antes de enviar.")
    else:
        with st.spinner("Buscando en ChromaDB y generando respuesta con Gemini..."):
            try:
                res = httpx.post(
                    f"{API_BASE_URL}/query",
                    json={"question": question, "top_k": top_k},
                    timeout=30.0
                )
                
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "")
                    citations = data.get("citations", [])
                    abstained = data.get("abstained", False)

                    st.markdown("### 💬 Respuesta")
                    if abstained:
                        st.warning(answer)
                    else:
                        st.info(answer)

                    # Mostrar Evidencia / Citas
                    st.markdown("### 🔍 Evidencia Recuperada")
                    if not citations:
                        st.write("No se recuperaron fragmentos.")
                    else:
                        for idx, cit in enumerate(citations, start=1):
                            with st.expander(f"Chunk [{idx}] — Fuente: {cit.get('source')} | Score: {cit.get('score')}"):
                                st.write(cit.get("text"))
                                st.caption(f"ID: {cit.get('id')}")

                else:
                    st.error(f"Error de la API: {res.text}")

            except Exception as e:
                st.error(f"Error al conectar con la API: {str(e)}")