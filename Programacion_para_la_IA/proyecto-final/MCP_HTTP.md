# MCP mediante HTTP local

Utiliza el SDK oficial para Python **versión 2**, con **Streamable HTTP**.
La dirección del servidor será **`http://127.0.0.1:8000/mcp`**.

## Servidor

Este es el inicio de `server.py`; añade tus herramientas antes del bloque final:

```python
from mcp.server import MCPServer

mcp = MCPServer("Amazon reviews")

# Register your tools here with @mcp.tool().

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
```

Usa `@mcp.tool()` sobre las funciones `search_products`, `analyze_product` y
`compare_products`. Estas funciones utilizan los datos, la configuración y los
embeddings preparados por los módulos de `support/` descritos en la
[guía](./GUIA.md#estructura-del-proyecto).
Devuelve listas, diccionarios, cadenas y números de Python. Convierte resultados
NumPy o PyTorch con `.tolist()`, `float()` o `int()` cuando corresponda.

Para señalar una entrada inválida puedes utilizar `ToolError`:

```python
from mcp.server.mcpserver.exceptions import ToolError

# Inside search_products:
# if not query.strip():
#     raise ToolError("query must not be empty")
```

Inicia el servidor en una primera terminal:

```bash
uv run --locked python server.py
```

## Cliente proporcionado

Guarda este snippet como `client.py`. Los IDs de ejemplo están presentes en el
dataset. Puedes cambiar las consultas o los productos para tu demostración.

```python
from typing import Any

from mcp import Client


async def demonstrate() -> None:
    calls: list[tuple[str, dict[str, Any]]] = [
        ("search_products", {"query": "A portable waterproof Bluetooth speaker", "top_k": 3}),
        ("analyze_product", {"product_id": "B0BCTJMN63"}),
        ("compare_products", {"product_ids": ["B0BCTJMN63", "B09MMWM2Y8"]}),
        ("analyze_product", {"product_id": "UNKNOWN_PRODUCT"}),
        ("search_products", {"query": "delivery", "top_k": 0}),
        ("search_products", {"query": "Comfortable headphones with good sound", "top_k": 2}),
    ]
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print("Tools:", [tool.name for tool in tools.tools])
        for name, arguments in calls:
            print(f"\n{name}: {arguments}")
            result = await client.call_tool(name, arguments)
            print("Tool error:", result.is_error)
            print(result.model_dump_json(indent=2))
```

Guarda este snippet como `main.py`:

```python
import asyncio

from client import demonstrate

if __name__ == "__main__":
    asyncio.run(demonstrate())
```

Ejecuta en una segunda terminal:

```bash
uv run --locked python main.py
```

El cliente descubre las herramientas y muestra sus respuestas. La llamada con
`top_k=0` debe producir un error; la siguiente debe funcionar en la misma conexión.
Si falla la conexión, comprueba que el servidor sigue abierto en el puerto 8000
y que la URL termina en `/mcp`.

## Referencias oficiales

- [Herramientas del servidor](https://py.sdk.modelcontextprotocol.io/servers/tools/).
- [Errores de herramientas](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/).
- [Cliente Streamable HTTP](https://py.sdk.modelcontextprotocol.io/client/transports/).
