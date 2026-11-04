# Sesión 3: Agentes con LangChain · opcional

Exploraremos `create_agent`, mensajes, tools, guardrails de entrada y conexión MCP con el catálogo de
documentos. El modelo decide las llamadas a tools; LangGraph sostiene la ejecución.

**La sesión es opcional y no tiene entregable.** Ejecutar el agente requiere una
API key propia y puede generar cargos. Puedes revisar mensajes y probar las tools
localmente sin conectar un modelo.

## Material

- [Presentación (PDF)](https://drive.google.com/file/d/1UZk2iv7_CTsek4SLgyDy14KKZe0FVrE5/view?usp=drivesdk).

- [Notebook](./u3_n4_langchain_agents.ipynb).
- [Tools](./catalog_tools.py) y [construcción del agente](./agent_app.py).
- [Guardrails](./input_guardrails.py) y [cliente MCP](./mcp_client.py).
- [PRACTICA.md](./PRACTICA.md).
- [Fuentes oficiales](./FUENTES.md).

## Preparación

Abre esta carpeta en VS Code o PyCharm y ejecuta `uv sync --locked`.
Selecciona `.venv` como intérprete y kernel; utiliza las extensiones Python y
Jupyter en VS Code o la integración de notebooks de PyCharm.

Para conectar un proveedor, instala **una** integración:

| Proveedor | Preparación | `PROVIDER` | Variable de la clave |
|---|---|---|---|
| OpenAI | `uv sync --locked --extra openai` | `openai` | `OPENAI_API_KEY` |
| Anthropic | `uv sync --locked --extra anthropic` | `anthropic` | `ANTHROPIC_API_KEY` |
| Gemini | `uv sync --locked --extra gemini` | `google_genai` | `GOOGLE_API_KEY` |

`--extra` incorpora las dependencias opcionales de ese proveedor. Reinicia el
kernel si lo tenías abierto.

### Cargar la API key

1. Copia [.env.example](./.env.example) como `.env` en esta carpeta.
2. En `.env`, elige `PROVIDER`, escribe en `MODEL_NAME` el identificador de un modelo
   de tu cuenta que admita tools y completa **solo** la clave del proveedor elegido.
   Puedes obtenerla desde las guías de [OpenAI](https://docs.langchain.com/oss/python/integrations/chat/openai#credentials),
   [Anthropic](https://docs.langchain.com/oss/python/integrations/chat/anthropic#credentials)
   o [Gemini](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai#credentials).
3. Ejecuta la celda de configuración de la notebook. `load_dotenv()` carga el archivo
   en las variables de entorno que lee la integración; no imprime la clave.
4. Activa `RUN_MODEL = True` cuando quieras realizar la llamada.

El archivo `.env` está excluido de Git; `.env.example` contiene campos vacíos.
Si falta la clave, se solicita con `getpass()`, sin guardarla en la notebook.
Las variables ya definidas en el entorno tienen prioridad sobre `.env`. Si editas
el archivo después de cargarlo, reinicia el kernel y ejecuta las celdas de nuevo.

También puedes ejecutar el agente desde la terminal, sustituyendo el identificador:

```bash
uv run --locked --extra openai python main.py --provider openai --model <model-id>
```

El límite de tres llamadas al modelo por ejecución detiene el ciclo, pero no
establece un presupuesto de dinero. Los resultados generados deben contrastarse
con las tools y el catálogo.

## Guardrails y MCP

La notebook presenta primero una regla local y después un clasificador opcional
con salida estructurada. `RUN_LLM_GUARDRAIL` controla esa llamada adicional; su
modelo se configura en `GUARDRAIL_MODEL_NAME` dentro de `.env`. Si se deja vacío,
se utiliza `MODEL_NAME`; ese modelo debe admitir salida estructurada.

Para la demostración MCP, inicia el servidor del [proyecto final](../../proyecto-final/README.md)
en `http://127.0.0.1:8000/mcp`. No necesitas tener terminado tu servidor para seguir
la explicación en clase. En otro proceso, desde esta sesión:

```bash
uv sync --locked --extra mcp
uv run --locked --extra mcp python mcp_client.py
```

El cliente lista las tools y realiza una búsqueda sin un modelo generativo.
En la notebook, `RUN_MCP` habilita esa conexión y `RUN_MCP_AGENT` habilita el agente.
Para usar OpenAI y MCP juntos, conserva ambos extras:

```bash
uv sync --locked --extra mcp --extra openai
```

La integración actual `MCPAdapter` está en beta y queda fijada por `uv.lock`.
Si no conecta, comprueba que el servidor esté iniciado y que la URL incluya `/mcp`.

[Volver a la unidad](../README.md)
