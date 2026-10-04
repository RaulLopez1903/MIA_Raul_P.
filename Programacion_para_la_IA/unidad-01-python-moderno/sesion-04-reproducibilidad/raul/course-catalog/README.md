# Práctica: un catálogo reproducible con MCP

## Ejercicio 1 · Punto de entrada

Ejecuta `uv run python -c "import main"`. Explica por qué no consulta el catálogo.
Identifica también la condición que impide iniciar el transporte al importar
`server.py`. Distingue registrar una herramienta de iniciar el servidor.

El codigo ejecutdo no connsulta el catalogo ya que 

## Ejercicio 2 · Datos y argumentos

Copia `data/courses.json` a `data/extra_courses.json` y agrega un curso cuyo título
incluya Python. Usa `--catalog` para consultar esa copia desde `main.py` y comprueba
que aparecen tres resultados. Prueba una ruta inexistente y registra el código
de salida. La herramienta MCP sigue usando el catálogo predeterminado.

```bash
uv run python main.py python --catalog data/extra_courses.json
```

```bash
INFO | catalog.search | Search completed: 3 matches
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  },
  {
    "code": "PY03",
    "title": "Python for machine learning",
    "hours": 18
  }
]
```

## Ejercicio 3 · Niveles y destinos

Compara una misma consulta con DEBUG, INFO y ERROR. Después usa
`--log-level ERROR --log-file logs/app.log`. Explica por qué el archivo conserva
mensajes que no aparecen en consola y por qué stdout debe reservarse al protocolo
en `server.py`.

```bash
uv run python main.py python --log-level ERROR --log-file logs/app.log
```

```bash
[  
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  }
]
```


```bash
uv run python main.py python --log-level DEBUG                        
```


```bash
DEBUG | catalog.search | Reading catalog: C:\Users\raul.perez\Documents\MIA\Github\MIA_Raul_P\Programacion_para_la_IA\unidad-01-python-moderno\sesion-04-reproducibilidad\raul\course-catalog\data\courses.json
INFO | catalog.search | Search completed: 2 matches
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  }
]
```


```bash 
uv run python main.py python --log-level INFO 
```

```bash
INFO | catalog.search | Search completed: 2 matches
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  }
]
```

```bash
uv run python main.py python --log-level ERROR

```

```bash
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  }
]
```


## Ejercicio 4 · Mejorar el diagnóstico

Añade al mensaje INFO de `catalog/search.py` la cantidad total de cursos leídos,
además de la cantidad de coincidencias. Usa argumentos de logging. Comprueba
que la consulta directa y la llamada MCP siguen devolviendo los mismos cursos.

```bash
uv run python main.py python --log-level INFO
```

```bash
INFO | catalog.search | Search completed: 3 readed courses
INFO | catalog.search | Search completed: 2 matches
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  }
]
```

## Ejercicio 5 · Reproducción y llamada MCP

Desde una copia limpia, ejecuta `uv sync --locked` y `client.py` con `python`,
`astronomy` y una cadena de espacios. Identifica la herramienta disponible y
distingue respuesta vacía de error. Explica qué aportan `pyproject.toml`,
`uv.lock` y `.python-version` y por qué no se entrega `.venv`.

```bash
uv run python main.py python  
```          

```bash
INFO | catalog.search | Search completed: 3 readed courses
INFO | catalog.search | Search completed: 2 matches
[
  {
    "code": "PY01",
    "title": "Python foundations",
    "hours": 12
  },
  {
    "code": "PY02",
    "title": "Python for data analysis",
    "hours": 16
  }
]
```

```bash
uv run python main.py astronomy
```

```bash
INFO | catalog.search | Search completed: 3 readed courses
INFO | catalog.search | Search completed: 0 matches
[]

uv run --locked python client.py " "                                  
Tools: ['find_courses']
{
  "meta": {
    "io.modelcontextprotocol/serverInfo": {
      "name": "Course catalog",
      "version": ""
    }
  },
  "content": [
    {
      "type": "text",
      "text": "Error executing tool find_courses: Cannot search the catalog. Check the query and server logs.",
      "annotations": null,
      "meta": null
    }
  ],
  "structured_content": null,
  "is_error": true,
  "result_type": "complete"
}
```

## Comprobaciones de calidad

Las pruebas incluyen un curso con horas negativas y una prueba de consola que
ejecuta `main.py` con un catálogo inexistente, comprobando código de salida 1
y stdout vacío. Un import temporal sin usar produjo el diagnóstico `F401` de
Ruff; se eliminó antes de las comprobaciones finales.

Desde una copia limpia, sin entorno virtual, cachés ni logs:

```bash
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy --strict main.py server.py client.py catalog
uv run --locked python -m pytest
```

Todas las comprobaciones pasaron: Ruff sin errores, 9 archivos con formato
correcto, mypy sin problemas en 6 archivos y pytest con 6 pruebas aprobadas.

## Entregables

- El proyecto con código, datos pequeños, pruebas, `pyproject.toml`, `uv.lock`,
  `.python-version` y `Makefile`.
- Un README con comandos, resultados de las llamadas y explicaciones de los
  ejercicios, incluida la evidencia de las comprobaciones de calidad.

Comprueba la ejecución desde una copia limpia. Entrega el proyecto sin `.venv`,
cachés ni logs.
