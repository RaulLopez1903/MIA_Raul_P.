# Dataset: Amazon Reviews 2023 · selección de Electronics

Usaremos **600 productos y 6 992 reseñas**, entre 5 y 30 por producto. La selección
incluye catálogo y opiniones, relacionados mediante `parent_asin`. Es un subconjunto
pequeño de Electronics, que contiene aproximadamente 43,9 millones de reseñas,
y de Amazon Reviews 2023, con aproximadamente 571,54 millones.
[Estadísticas oficiales](https://amazon-reviews-2023.github.io/#grouped-by-category).

## Archivos proporcionados

- [datasets/reviews.jsonl.gz](./datasets/reviews.jsonl.gz): opiniones, estrellas,
  ID de producto y número de línea en el archivo original.
- [datasets/products.jsonl.gz](./datasets/products.jsonl.gz): título,
  características, descripción disponible, categorías originales y familia.

Copia la carpeta `datasets/` a tu proyecto. Ambos archivos juntos ocupan aproximadamente
1,1 MB comprimido. Usa los archivos completos de **esta selección**; no descargues
la categoría completa ni construyas otra muestra para la entrega. El modelo de
embeddings se descarga por separado.

## Diversidad y selección

| Familia | Productos |
|---|---:|
| Computación y accesorios | 236 |
| Audio | 157 |
| Televisión y video | 77 |
| Fotografía | 58 |
| Accesorios y suministros | 52 |
| Wearables | 20 |
| **Total** | **600** |

La [notebook](./preparacion_datos.ipynb) incluye exploración y código de preparación.
Se leen las primeras **250 000 reseñas y 50 000 metadatos** originales, conservando
entre 5 y 30 reseñas válidas con texto por producto. Los productos se eligen por
turnos entre familias, con IDs ordenados. La agrupación usa la segunda entrada de
`categories`, o `main_category` si falta. Las familias con más candidatos ocupan
los lugares restantes cuando las otras se agotan.

Es una selección por conveniencia, **no aleatoria ni representativa**. Sus medias
describen solo las reseñas proporcionadas; el límite de 30 impide interpretar el
conteo como popularidad en Amazon.

Fuentes originales usadas para preparar los archivos pequeños:

- [Electronics.jsonl.gz](https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Electronics.jsonl.gz).
- [meta_Electronics.jsonl.gz](https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_Electronics.jsonl.gz).

## Formato

Los archivos son **JSONL comprimido con gzip**: cada línea contiene un objeto JSON
independiente. La notebook muestra cómo leerlos con `gzip.open()` y `json.loads()`.
Relaciona los archivos por `parent_asin`, no por posición.

## Campos principales

| Archivo | Campo | Uso |
|---|---|---|
| Reseñas | `text` | Texto que se utiliza en la búsqueda. |
| Reseñas | `rating` | Valoración de 1 a 5 estrellas. |
| Reseñas | `parent_asin` | Identificador del producto al que pertenece la reseña. |
| Metadatos | `parent_asin` | Identificador para relacionar el producto con sus reseñas. |
| Metadatos | `title` | Nombre del producto. |
| Metadatos | `features`, `description` | Listas de características y descripción; se unen al título para representar el catálogo. |
| Metadatos | `categories`, `family` | Categorías originales y agrupación utilizada para explorar diversidad. |
| Reseñas | `source_line` | Línea en el archivo original de Electronics; permite construir un ID estable. |

Los 600 productos tienen título; 596 tienen características y 303 tienen descripción.
Las listas vacías se omiten al construir el texto del catálogo.
Consulta la [guía](./GUIA.md) para combinar catálogo y reseñas.

Para IDs de reseña estables, utiliza `source_line`, por ejemplo `Electronics:123`.
`parent_asin` identifica al producto, no a una reseña individual.

[Diccionario de datos original](https://amazon-reviews-2023.github.io/#data-fields).
