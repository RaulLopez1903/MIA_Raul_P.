import streamlit as st
import httpx

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Sistema RAG", page_icon="💬")
st.title("Sistema RAG (FastAPI + ChromaDB + Gemini)")

# Sidebar para Ingestar
with st.sidebar:
    st.header("Cargar Documentos")
    uploaded_file = st.file_uploader("Sube un archivo (.txt o .md)", type=["txt", "md"])
    if uploaded_file and st.button("Ingestar Documento"):
        with st.spinner("Indexando en ChromaDB..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")}
            try:
                res = httpx.post(f"{API_URL}/ingest", files=files, timeout=60.0)
                if res.status_code == 200:
                    st.success(f"Éxito: {res.json()['chunks_indexed']} chunks indexados.")
                else:
                    st.error("Error al procesar el archivo.")
            except Exception as e:
                st.error(f"No se pudo conectar con la API: {e}")

# Historial de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escribe tu pregunta sobre el corpus...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando evidencia y generando respuesta..."):
            try:
                response = httpx.post(
                    f"{API_URL}/query", 
                    json={"question": prompt, "top_k": 3},
                    timeout=30.0
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    st.markdown(answer)
                    
                    # Desplegar los fragmentos y scores si no se abstuvo
                    if not data["abstained"] and data.get("citations"):
                        with st.expander("Ver evidencia recuperada (Top-K)"):
                            for idx, cite in enumerate(data["citations"], 1):
                                st.write(f"**[{idx}] {cite['source']}** (Distancia: {cite['score']:.4f})")
                                st.caption(cite["text"])
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Error en la respuesta de la API.")
            except Exception as e:
                st.error(f"Error de conexión con FastAPI: {e}")