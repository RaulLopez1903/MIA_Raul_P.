# Proyecto final: búsqueda y análisis de productos de Amazon con MCP

Se construyó un servidor MCP por HTTP local para buscar y analizar productos de
**Amazon Reviews 2023 · Electronics**, utilizando embeddings y operaciones de
**PyTorch o NumPy**. Proporcionamos una selección de **600 productos y 6 992 reseñas**,
entre 5 y 30 por producto; no necesitas preparar otra muestra ni crear un agente.

## Ejecución de la aplicación

Desde esta carpeta, inicia el servidor HTTP en una terminal:

```bash
uv sync --locked
uv run --locked python server.py
```

En otra terminal, descubre las herramientas y ejecuta la demostración:

```bash
uv run --locked python main.py
```

Comprueba los tipos de todos los módulos:

```bash
uv run --locked mypy --strict server.py client.py main.py support
```

La carga del modelo, los datos y la matriz de embeddings ocurre al iniciar el
servidor. No hace falta ejecutar la notebook. El modelo
`sentence-transformers/all-MiniLM-L6-v2` está orientado al inglés y trunca entradas
largas a 256 tokens. La selección de reseñas es pequeña y no aleatoria; las
estadísticas describen únicamente las reseñas incluidas, no todas las opiniones
de Amazon ni la calidad general del producto.

### Ejemplos de consultas e interpretación

Se ejecutó ``uv run --locked python main.py`` como demostración de `search_products`, `analyze_products` y `compare_products`, cuyos resultados se detallan en [Resultados](#salida-de-la-demostración); en particular para la busqueda de productos:

- `A portable waterproof Bluetooth speaker`: entre los primeros resultados aparecen Altec Lansing Mini H2O - Waterproof Bluetooth Speaker (0.794) y EDUPLINK Waterproof Portable Bluetooth Speaker - 20W Louder Wireless Speaker with 20 Hours Playtime (0.790), cuyos títulos incluyen las características consultadas. La similitud ordena cercanía semántica en esta selección; no es probabilidad ni calidad del producto.
- `Comfortable headphones with good sound`: aparecen Sony MDR7506 Professional Large Diaphragm Headphone (0.729) y OneOdio Over Ear Headphone (0.717), candidatos que se pueden inspeccionar con el análisis de reseñas. Los resultados dependen de solo 5–30 reseñas seleccionadas por producto; además, el modelo está orientado al inglés y trunca textos largos.

## Ejecución y comportamiento

El servidor utiliza **Streamable HTTP** en **`http://127.0.0.1:8000/mcp`**.
El cliente debe descubrir e invocar las tres herramientas.

- `top_k`: entero entre 1 y 20; devuelve como máximo esa cantidad de coincidencias.
- Consulta o ID en blanco: error claro. En una comparación, los IDs deben ser distintos.
- Producto desconocido: análisis con conteo cero, conteos y proporciones en cero y
  media/mediana `null`. Si falta una media, la diferencia correspondiente también es `null`.
- Una llamada inválida no debe impedir una llamada válida posterior.

La búsqueda semántica devuelve los productos más cercanos incluso si la consulta
es poco relevante. Su puntuación no es una probabilidad ni mide la calidad del producto.

### Salida de la demostración

```json
(proyecto-final) PS C:\Users\raul.perez\Documents\MIA\Github\MIA_Raul_P\Programacion_para_la_IA\proyecto-final> uv run --locked python main.py
Tools: ['search_products', 'analyze_product', 'compare_products']

search_products: {'query': 'A portable waterproof Bluetooth speaker', 'top_k': 3}
Tool error: False
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Amazon Reviews 2023 Electronics",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"B0B786PFYJ\",\n  \"title\": \"Altec Lansing Mini H2O - Waterproof Bluetooth Speaker, IP67 Certified & Floats in Water, Compact & Portable Speaker for Hiking, Camping, Pool, and Beach\",\n  \"similarity\": 0.7942359447479248,\n  \"review_count\": 11\n}",
      "annotations": null,
      "meta": null
    },
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"B0BNY1L4JP\",\n  \"title\": \"EDUPLINK Waterproof Portable Bluetooth Speaker - 20W Louder Wireless Speaker with 20 Hours Playtime, TWS Pairing, RGB Lights and TF Slot - Perfect for Beach and Pool (Black)\",\n  \"similarity\": 0.7895708084106445,\n  \"review_count\": 13\n}",
      "annotations": null,
      "meta": null
    },
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"B09WWG19YS\",\n  \"title\": \"Bose SoundLink Micro: Small Portable Bluetooth Speaker (Waterproof), Midnight Blue\",\n  \"similarity\": 0.7579573392868042,\n  \"review_count\": 27\n}",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": {
    "result": [
      {
        "product_id": "B0B786PFYJ",
        "title": "Altec Lansing Mini H2O - Waterproof Bluetooth Speaker, IP67 Certified & Floats in Water, Compact & Portable Speaker for Hiking, Camping, Pool, and Beach",
        "similarity": 0.7942359447479248,
        "review_count": 11
      },
      {
        "product_id": "B0BNY1L4JP",
        "title": "EDUPLINK Waterproof Portable Bluetooth Speaker - 20W Louder Wireless Speaker with 20 Hours Playtime, TWS Pairing, RGB Lights and TF Slot - Perfect for Beach and Pool (Black)",
        "similarity": 0.7895708084106445,
        "review_count": 13
      },
      {
        "product_id": "B09WWG19YS",
        "title": "Bose SoundLink Micro: Small Portable Bluetooth Speaker (Waterproof), Midnight Blue",
        "similarity": 0.7579573392868042,
        "review_count": 27
      }
    ]
  },
  "is_error": false,
  "result_type": "complete"
}

analyze_product: {'product_id': 'B0BCTJMN63'}
Tool error: False
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Amazon Reviews 2023 Electronics",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"B0BCTJMN63\",\n  \"review_count\": 7,\n  \"rating_counts\": {\n    \"1\": 0,\n    \"2\": 0,\n    \"3\": 0,\n    \"4\": 3,\n    \"5\": 4\n  },\n  \"rating_proportions\": {\n    \"1\": 0.0,\n    \"2\": 0.0,\n    \"3\": 0.0,\n    \"4\": 0.42857142857142855,\n    \"5\": 0.5714285714285714\n  },\n  \"mean_rating\": 4.571428571428571,\n  \"median_rating\": 5.0\n}",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": {
    "product_id": "B0BCTJMN63",
    "review_count": 7,
    "rating_counts": {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 3,
      "5": 4
    },
    "rating_proportions": {
      "1": 0.0,
      "2": 0.0,
      "3": 0.0,
      "4": 0.42857142857142855,
      "5": 0.5714285714285714
    },
    "mean_rating": 4.571428571428571,
    "median_rating": 5.0
  },
  "is_error": false,
  "result_type": "complete"
}

compare_products: {'product_ids': ['B0BCTJMN63', 'B09MMWM2Y8']}
Tool error: False
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Amazon Reviews 2023 Electronics",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "{\n  \"baseline_product_id\": \"B0BCTJMN63\",\n  \"products\": [\n    {\n      \"product_id\": \"B0BCTJMN63\",\n      \"review_count\": 7,\n      \"rating_counts\": {\n        \"1\": 0,\n        \"2\": 0,\n        \"3\": 0,\n        \"4\": 3,\n        \"5\": 4\n      },\n      \"rating_proportions\": {\n        \"1\": 0.0,\n        \"2\": 0.0,\n        \"3\": 0.0,\n        \"4\": 0.42857142857142855,\n        \"5\": 0.5714285714285714\n      },\n      \"mean_rating\": 4.571428571428571,\n      \"median_rating\": 5.0,\n      \"mean_difference_from_first\": 0.0\n    },\n    {\n      \"product_id\": \"B09MMWM2Y8\",\n      \"review_count\": 20,\n      \"rating_counts\": {\n        \"1\": 2,\n        \"2\": 1,\n        \"3\": 0,\n        \"4\": 2,\n        \"5\": 15\n      },\n      \"rating_proportions\": {\n        \"1\": 0.1,\n        \"2\": 0.05,\n        \"3\": 0.0,\n        \"4\": 0.1,\n        \"5\": 0.75\n      },\n      \"mean_rating\": 4.35,\n      \"median_rating\": 5.0,\n      \"mean_difference_from_first\": -0.22142857142857153\n    }\n  ]\n}",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": {
    "baseline_product_id": "B0BCTJMN63",
    "products": [
      {
        "product_id": "B0BCTJMN63",
        "review_count": 7,
        "rating_counts": {
          "1": 0,
          "2": 0,
          "3": 0,
          "4": 3,
          "5": 4
        },
        "rating_proportions": {
          "1": 0.0,
          "2": 0.0,
          "3": 0.0,
          "4": 0.42857142857142855,
          "5": 0.5714285714285714
        },
        "mean_rating": 4.571428571428571,
        "median_rating": 5.0,
        "mean_difference_from_first": 0.0
      },
      {
        "product_id": "B09MMWM2Y8",
        "review_count": 20,
        "rating_counts": {
          "1": 2,
          "2": 1,
          "3": 0,
          "4": 2,
          "5": 15
        },
        "rating_proportions": {
          "1": 0.1,
          "2": 0.05,
          "3": 0.0,
          "4": 0.1,
          "5": 0.75
        },
        "mean_rating": 4.35,
        "median_rating": 5.0,
        "mean_difference_from_first": -0.22142857142857153
      }
    ]
  },
  "is_error": false,
  "result_type": "complete"
}

analyze_product: {'product_id': 'UNKNOWN_PRODUCT'}
Tool error: False
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Amazon Reviews 2023 Electronics",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"UNKNOWN_PRODUCT\",\n  \"review_count\": 0,\n  \"rating_counts\": {\n    \"1\": 0,\n    \"2\": 0,\n    \"3\": 0,\n    \"4\": 0,\n    \"5\": 0\n  },\n  \"rating_proportions\": {\n    \"1\": 0.0,\n    \"2\": 0.0,\n    \"3\": 0.0,\n    \"4\": 0.0,\n    \"5\": 0.0\n  },\n  \"mean_rating\": null,\n  \"median_rating\": null\n}",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": {
    "product_id": "UNKNOWN_PRODUCT",
    "review_count": 0,
    "rating_counts": {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0
    },
    "rating_proportions": {
      "1": 0.0,
      "2": 0.0,
      "3": 0.0,
      "4": 0.0,
      "5": 0.0
    },
    "mean_rating": null,
    "median_rating": null
  },
  "is_error": false,
  "result_type": "complete"
}

search_products: {'query': 'delivery', 'top_k': 0}
Tool error: True
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Amazon Reviews 2023 Electronics",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "Error executing tool search_products: top_k must be an integer between 1 and 20",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": null,
  "is_error": true,
  "result_type": "complete"
}

search_products: {'query': 'Comfortable headphones with good sound', 'top_k': 2}
Tool error: False
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Amazon Reviews 2023 Electronics",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"B07CQMZVZ6\",\n  \"title\": \"Sony MDR7506 Professional Large Diaphragm Headphone\",\n  \"similarity\": 0.7294141054153442,\n  \"review_count\": 30\n}",
      "annotations": null,
      "meta": null
    },
    {
      "type": "text",
      "text": "{\n  \"product_id\": \"B091K4WYD1\",\n  \"title\": \"OneOdio Over Ear Headphone, Wired Bass Headsets with 50mm Driver, Foldable Lightweight Headphones with Shareport and Mic for Recording Monitoring Podcast Guitar PC TV - (Red)\",\n  \"similarity\": 0.7165664434432983,\n  \"review_count\": 30\n}",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": {
    "result": [
      {
        "product_id": "B07CQMZVZ6",
        "title": "Sony MDR7506 Professional Large Diaphragm Headphone",
        "similarity": 0.7294141054153442,
        "review_count": 30
      },
      {
        "product_id": "B091K4WYD1",
        "title": "OneOdio Over Ear Headphone, Wired Bass Headsets with 50mm Driver, Foldable Lightweight Headphones with Shareport and Mic for Recording Monitoring Podcast Guitar PC TV - (Red)",
        "similarity": 0.7165664434432983,
        "review_count": 30
      }
    ]
  },
  "is_error": false,
  "result_type": "complete"
}
```