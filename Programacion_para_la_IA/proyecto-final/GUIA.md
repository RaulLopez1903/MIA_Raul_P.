# Guía de desarrollo

Consulta el [README](./README.md) para el alcance y los entregables.

## 1. Crear el entorno y explorar los datos

Crea una carpeta propia y ejecuta:

```bash
uv init
uv add numpy torch sentence-transformers "mcp>=2,<3"
uv add --dev mypy pandas matplotlib ipykernel
```

Copia la [notebook](./preparacion_datos.ipynb), [datasets](./datasets/) y
[config.json](./config.json) a tu proyecto. Abre la notebook en VS Code o PyCharm
con el intérprete de `.venv` y ejecuta la lectura y exploración. La sección de
regeneración es opcional.

### Estructura del proyecto

Organiza la aplicación con esta estructura; puedes elegir otro nombre para la
carpeta del proyecto:

```text
amazon-products/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── config.json
├── server.py
├── client.py
├── main.py
├── support/
│   ├── __init__.py
│   ├── data.py
│   ├── settings.py
│   └── encoder.py
└── datasets/
    ├── products.jsonl.gz
    └── reviews.jsonl.gz
```

`server.py` contiene el servidor y las tres herramientas MCP. `client.py` realiza
las llamadas de demostración y `main.py` ejecuta ese cliente; sus snippets están
en [MCP_HTTP.md](./MCP_HTTP.md). Implementa en `support/`:

- `data.py`: lectura de los archivos y preparación de textos e IDs.
- `settings.py`: carga y validación de la configuración.
- `encoder.py`: carga del modelo, codificación y construcción de los vectores de producto.

La notebook es una referencia para explorar y adaptar la preparación de datos.
El servidor debe importar y utilizar estos módulos, sin depender de ejecutar la
notebook ni de sus variables.

Al preparar el archivo de entrega, omite `.venv`, cachés y pesos del modelo.

## 2. Preparar los datos y el modelo

Adapta las funciones de lectura de la notebook en `support/data.py` y conserva
sus IDs de reseña. En `support/settings.py`, carga los valores de `config.json`:
modelo, tamaño del lote y dispositivo.
Comprueba que el nombre no esté vacío y que el tamaño de lote sea un entero positivo.
Puedes usar un modelo Pydantic para validar esta configuración.

## 3. Generar los embeddings para la búsqueda

Un embedding es un vector que representa un texto. Con este modelo, cada reseña
produce **384 números**. La consulta se convierte en otro vector y se compara
con una representación de cada producto. Combinaremos lo que ofrece el catálogo
con lo que cuentan sus clientes.

### Seleccionar los textos y conservar su orden

Retoma `texts`, `review_ids` y `review_product_ids` de la sección 7 de la
[notebook](./preparacion_datos.ipynb). La fila `i` de los embeddings corresponde a
`texts[i]` y a esos mismos IDs: no ordenes ni filtres las listas por separado.

### Empezar con tres textos

Este ejemplo aislado muestra la carga y la codificación. En tu aplicación,
obtén el nombre del modelo, dispositivo y tamaño del lote de `config.json`.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
)
example_texts = [
    "The package arrived two weeks late.",
    "The headphones feel comfortable.",
    "Customer support answered my question quickly.",
]
review_vectors = model.encode(
    example_texts,
    batch_size=2,
    convert_to_tensor=True,
    normalize_embeddings=True,
)
print("Shape:", review_vectors.shape)  # torch.Size([3, 384])
```

`batch_size=2` procesa hasta dos textos por lote; el resultado contiene los tres,
en su orden original. `convert_to_tensor=True` devuelve un tensor PyTorch.
`normalize_embeddings=True` ajusta cada vector a longitud uno, lo que permite
calcular similitud coseno mediante producto escalar. Puedes normalizar los vectores
con PyTorch o NumPy por separado, como en clase.

La primera carga descarga el modelo. Las siguientes aprovechan su caché local.
Este modelo está orientado a inglés y trunca textos mayores de 256 tokens de su
tokenizador: utiliza consultas en inglés y menciona esta limitación en tu interpretación.

### Representar cada producto con catálogo y reseñas

El catálogo aporta `title` y las listas `features` y `description`. Utiliza
**título + características + descripción disponible** como texto de catálogo.
Une cada lista con `" ".join(...)`; una lista vacía aporta una cadena vacía.

Codifica el catálogo por producto y las reseñas por separado, con el mismo modelo
y `normalize_embeddings=True`. No concatenes todas las reseñas: el modelo truncaría
el texto. Agrupa sus vectores por `product_id` y calcula la media. Por ejemplo,
para un tensor de forma `(5, 384)`, `mean(dim=0)` produce `(384,)`; resume temas, no estrellas.

El cálculo tiene tres pasos:

1. Obtén el vector normalizado del catálogo.
2. Promedia los vectores de las reseñas con texto de ese producto y normaliza el promedio.
3. Combina ambos con **50 % de cada fuente** y normaliza el resultado.

Ejemplo numérico aislado para comprender las operaciones:

```python
import torch
import torch.nn.functional as F

catalog_vector = F.normalize(torch.tensor([1.0, 0.0]), dim=0)
review_vectors_for_product = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
review_average = review_vectors_for_product.mean(dim=0)
review_summary = F.normalize(review_average, dim=0)
product_vector = F.normalize(0.5 * catalog_vector + 0.5 * review_summary, dim=0)
print("Product vector:", product_vector)
```

Aquí usamos dos componentes para leer los números; los vectores reales tienen
384. Normalizar el promedio antes de combinar da el mismo peso a ambas fuentes,
independientemente de la longitud de ese promedio. Cada reseña aporta lo mismo;
no ponderes por estrellas ni por cantidad total de reseñas de otros productos.

Puedes recorrer los IDs de producto con un `for`, seleccionar las posiciones de
sus reseñas y calcular `mean(dim=0)`. Al terminar, reúne los vectores con
`torch.stack`. En NumPy, las operaciones equivalentes son `mean(axis=0)`,
normalización por longitud y `np.stack`.

Reúne los vectores finales en una matriz **`(600, 384)`** y conserva `product_ids`
en el mismo orden. Los datos proporcionados tienen catálogo y reseñas para los
600 productos. Mantén la matriz y el modelo en memoria para reutilizarlos.

### Codificar una consulta

Utiliza el mismo objeto `model` y la misma normalización:

```python
query = "My delivery arrived late."
query_vectors = model.encode(
    [query], convert_to_tensor=True, normalize_embeddings=True
)
query_vector = query_vectors[0]
print("Query shape:", query_vectors.shape)  # torch.Size([1, 384])
print("Vector shape:", query_vector.shape)  # torch.Size([384])
```

`[0]` obtiene el vector de la única consulta. Codifícala en cada llamada y
compárala con la matriz preparada. Para usar NumPy, convierte los tensores de CPU
con `.cpu().numpy()`.

## 4. Implementar búsqueda y análisis

Dentro de `search_products`, sigue este recorrido:

1. Valida la consulta y `top_k` según el enunciado.
2. Codifica la consulta con el modelo ya cargado.
3. Calcula un puntaje por producto: el producto de la matriz normalizada por el
   vector normalizado de la consulta. Para el dataset, `(600, 384) @ (384,)`
   produce `(600,)`.
4. Selecciona las posiciones con mayor puntaje usando `torch.topk` o
   `np.argsort` en orden descendente. Limita la cantidad al número de candidatos.
5. Recupera los productos mediante esas posiciones en `product_ids` y devuelve
   ID, título, similitud y conteo total de reseñas como valores de Python.

Prueba consultas de catálogo, como `"A portable waterproof Bluetooth speaker"`, y consultas
de experiencias, como `"Comfortable headphones with good sound"`. Revisa
los títulos recuperados y sus tamaños de muestra.

Para el análisis, selecciona las valoraciones del producto y calcula conteos,
proporciones, media y mediana. La comparación reutiliza estos cálculos.

## 5. Conectar y demostrar

Sigue [MCP_HTTP.md](./MCP_HTTP.md) para registrar las herramientas y utilizar los
snippets de `client.py` y `main.py`. Ejecuta el servidor y el cliente en terminales
separadas; el cliente incluye los casos de demostración.

## 6. Comprobar y entregar

Comprueba todos los módulos de la aplicación, incluidos los de `support/`:

```bash
uv run --locked mypy --strict server.py client.py main.py support
```

Añade al comando cualquier otro archivo o módulo Python de la aplicación que
hayas creado; el análisis debe finalizar sin errores. Conserva `uv.lock` y verifica
`uv sync --locked` desde una copia sin `.venv`. Comprueba que el servidor prepara
los datos y embeddings al iniciar, sin ejecutar antes la notebook. Documenta tus
comandos y entrega los archivos de la aplicación y la explicación de resultados
indicados en el README.

## Referencias para embeddings

- [Modelo y dimensiones](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- [Codificación y similitud de textos](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html).
- [Parámetros de `encode`](https://www.sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html).
