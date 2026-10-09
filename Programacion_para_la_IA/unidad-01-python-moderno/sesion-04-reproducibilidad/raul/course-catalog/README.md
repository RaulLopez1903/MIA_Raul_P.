# Catálogo reproducible de cursos con MCP

Este documento recoge los resultados de la práctica descrita en
[PRACTICA.md](../../PRACTICA.md) y las evidencias de validación definidas en
[CALIDAD.md](../../CALIDAD.md), aplicadas al proyecto construido siguiendo la
[guía](../../GUIA.md).

## Resultados de PRACTICA.md

### Resumen

- La aplicación de consola consulta el catálogo por defecto o un archivo
  indicado mediante `--catalog`.
- La búsqueda de `python` devuelve `PY01` y `PY02`; al consultar el catálogo
  ampliado, la coincidencia aumenta a tres cursos.
- Una consulta sin resultados termina correctamente con `[]`; una consulta
  vacía o un catálogo inexistente se reporta como error.
- La herramienta MCP se llama `find_courses` y usa el catálogo por defecto.

### Ejercicio 1: punto de entrada

```bash
uv run python -c "import main"
```

La importación de `main.py` no ejecuta la búsqueda de cursos porque la llamada a
`main()` queda protegida por `if __name__ == "__main__"`. Al importar el módulo,
`__name__` no coincide con `"__main__"`; por tanto, se definen las funciones y
los argumentos, pero no se dispara la consulta al catálogo.

Cuando se importa `server.py`, se crea el objeto MCP y se registra `find_courses`
con el decorador `@mcp.tool()`. El transporte no se inicia hasta que el archivo
se ejecuta directamente, ya que la llamada a `mcp.run(transport="stdio")`
también está protegida por la misma condición. Registrar una herramienta la
deja disponible para el servidor, pero no arranca por sí mismo el servicio.

### Ejercicio 2: datos y argumentos

Se amplió el catálogo base en `data/extra_courses.json` con el curso adicional:

```json
{
  "code": "PY03",
  "title": "Python for machine learning",
  "hours": 18
}
```

La búsqueda sobre esta copia devuelve tres resultados:

```bash
uv run python main.py python --catalog data/extra_courses.json
```

```text
INFO | catalog.search | Search completed: 4 readed courses
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

La salida incluye `PY01` (*Python foundations*), `PY02` (*Python for data
analysis*) y `PY03` (*Python for machine learning*). La opción `--catalog`
modifica la ejecución de la consola, mientras que la herramienta MCP sigue
usando el catálogo predeterminado.

Una ruta de catálogo inexistente provoca un error y devuelve el código de salida
`1`. La prueba de consola además verifica que `stdout` permanezca vacío:

```bash
uv run python main.py python --catalog data/missing.json
```

```text
ERROR | __main__ | Catalog search failed
Traceback (most recent call last):
  File "C:\Users\raul.perez\Documents\MIA\Github\MIA_Raul_P\Programacion_para_la_IA\unidad-01-python-moderno\sesion-04-reproducibilidad\raul\course-catalog\main.py", line 23, in main
    courses = search_courses(args.query, args.catalog)
  File "C:\Users\raul.perez\Documents\MIA\Github\MIA_Raul_P\Programacion_para_la_IA\unidad-01-python-moderno\sesion-04-reproducibilidad\raul\course-catalog\catalog\search.py", line 25, in search_courses
    with path.open(encoding="utf-8") as source:
         ~~~~~~~~~~~~~~~~
  File "C:\Users\raul.perez\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\Lib\pathlib\_local.py", line 537, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~~~~~~~~~~
FileNotFoundError: [Errno 2] No such file or directory: 'data\\missing.json'
```

### Ejercicio 3: niveles y destinos de logging

Con el catálogo predeterminado, la consulta `python` devuelve `PY01` y `PY02`.
El nivel de logging seleccionado determina qué mensajes se muestran en consola:

| Nivel | Mensajes visibles |
| --- | --- |
| `DEBUG` | Ruta del catálogo y resumen de la búsqueda. |
| `INFO` | Resumen de coincidencias. |
| `ERROR` | Ningún mensaje para una consulta exitosa. |

Ejemplo de ejecución con `DEBUG`:

```bash
uv run python main.py python --log-level DEBUG
```

```text
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

Para guardar los mensajes en un archivo de log:

```bash
uv run python main.py python --log-level ERROR --log-file logs/app.log
```

```text
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

El handler de consola respeta el nivel seleccionado, mientras que el handler de
archivo recibe mensajes desde `DEBUG`. Por ese motivo, `logs/app.log` puede
contener trazas que no aparecen en la terminal. La aplicación imprime el JSON de
resultados en `stdout` y envía los logs a `stderr`. En el servidor MCP, `stdout`
queda reservado para el protocolo stdio; escribir diagnósticos ahí podría
interferir con la comunicación.

### Ejercicio 4: mejora del diagnóstico

El mensaje `INFO` ahora registra tanto el número total de cursos leídos como el
número de coincidencias. La búsqueda de `python` sobre el catálogo
predeterminado lee tres cursos y encuentra dos:

```bash
uv run python main.py python --log-level INFO
```

```text
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

La salida de búsqueda sigue siendo `PY01` y `PY02`. Como la búsqueda compartida
se usa tanto desde la consola como desde `find_courses`, la llamada MCP aplica la
misma lógica y conserva los mismos resultados para el catálogo por defecto.

### Ejercicio 5: reproducción y llamada MCP

La aplicación de consola devuelve dos cursos al buscar `python` y una lista
vacía cuando no hay coincidencias:

```bash
uv run python main.py python
uv run python main.py astronomy
```

```text
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

```text
INFO | catalog.search | Search completed: 3 readed courses
INFO | catalog.search | Search completed: 0 matches
[]
```

La lista vacía es una respuesta válida y la ejecución termina correctamente. En
las llamadas MCP, el cliente descubre la herramienta `find_courses`: `python`
devuelve `PY01` y `PY02`, mientras que `astronomy` finaliza correctamente con
una lista vacía. Una cadena formada solo por espacios no es una consulta válida:
el cliente recibe un resultado con `is_error: true` y finaliza con código `1`.
El servidor registra el detalle del error y devuelve al cliente un mensaje
controlado.

```bash
uv run --locked python client.py python
uv run --locked python client.py astronomy
uv run --locked python client.py " "
```

```text
Tools: ['find_courses']
Error executing tool find_courses: Cannot search the catalog. Check the query and server logs.
is_error: true
```

La reproducción del entorno se realiza a partir del archivo de bloqueo:

```bash
uv sync --locked
```

- `pyproject.toml` declara los requisitos de Python y las dependencias del
  proyecto.
- `uv.lock` fija las versiones resueltas para garantizar una instalación
  reproducible.
- `.python-version` indica la versión de Python seleccionada para el proyecto.
- `.venv` es un entorno local reconstruible y, por tanto, no se incluye entre
  los entregables.

## Evidencias de los ejercicios de CALIDAD.md

Los ejercicios de calidad se resolvieron en los archivos de prueba y de
configuración del proyecto. Las evidencias que siguen muestran qué se
implementó y qué comprueba cada resultado.

### Ejercicio 1: validar horas negativas

En [tests/test_catalog.py](./tests/test_catalog.py), la prueba
`test_negative_course_hours` escribe un curso temporal con `"hours": -1` y
comprueba que `search_courses` lanza un `ValidationError`. Esto confirma que el
modelo `Course` rechaza horas no positivas. El catálogo temporal mantiene los
datos de prueba aislados y evita modificar el catálogo del proyecto.

### Ejercicio 2: comprobar el error de la interfaz de consola

En [tests/test_cli.py](./tests/test_cli.py), la prueba
`test_missing_catalog_exits_without_stdout` ejecuta `main.py` como proceso
independiente con una ruta de catálogo inexistente. Usa `subprocess.run` con
`capture_output=True` y una ruta temporal de pytest; después valida que el
código de salida sea `1` y que `stdout` permanezca vacío. Así se comprueba el
contrato de error de la aplicación desde la perspectiva del usuario que la
ejecuta, no solo la excepción interna de la función de búsqueda.

### Ejercicio 3: detectar y corregir un import sin usar

Durante el ejercicio se añadió temporalmente un import no utilizado. Ruff lo
identificó con el diagnóstico `F401`; dicho import se eliminó y la comprobación
final de lint terminó sin errores. Esta prueba manual confirma que la regla de
imports no utilizados está activa y que la versión entregada no conserva ese
defecto.

```text
I001 [*] Import block is un-sorted or un-formatted
 --> main.py:3:1
  |
1 |   """Query the catalog directly from the terminal."""
2 |
3 | / import argparse
4 | | import json
5 | | import logging
6 | | from pathlib import Path
7 | | import matplotlib
8 | | from catalog.logging_config import configure_logging
9 | | from catalog.search import DEFAULT_CATALOG, search_courses
  | |__________________________________________________________^
help: Organize imports
   |
6  | from pathlib import Path
7  +
8  | import matplotlib
9  +
10 | from catalog.logging_config import configure_logging
   |

F401 [*] `matplotlib` imported but unused
 --> main.py:7:8
  |
5 | import logging
6 | from pathlib import Path
7 | import matplotlib
  |        ^^^^^^^^^^
8 | from catalog.logging_config import configure_logging
9 | from catalog.search import DEFAULT_CATALOG, search_courses
  |
help: Remove unused import: `matplotlib`
  |
6 | from pathlib import Path
  - import matplotlib
7 | from catalog.logging_config import configure_logging
  |

Found 2 errors.
[*] 2 fixable with the `--fix` option.
```

### Ejercicio 4: ejecutar las comprobaciones desde una copia limpia

Se partió de una copia limpia, sin entorno virtual, cachés ni logs. Se
reconstruyó el entorno con el lockfile y se ejecutaron las cuatro verificaciones
solicitadas en [CALIDAD.md](../../CALIDAD.md):

```bash
uv sync --locked
uv run --locked ruff check
uv run --locked ruff format --check
uv run --locked mypy --strict main.py server.py client.py catalog
uv run --locked python -m pytest
```

| Comprobación | Evidencia y resultado |
| --- | --- |
| `ruff check .` | All checks passed! |
| `ruff format --check .` | 9 files already formatted |
| `mypy --strict main.py server.py client.py catalog` | Success: no issues found in 6 source files |
| `python -m pytest` | 6 passed in 1.09s |

La secuencia completa terminó correctamente. `uv sync --locked` demuestra que
las dependencias pueden instalarse a partir de `uv.lock` sin modificarlo; Ruff
comprueba lint y formato, mypy revisa los tipos y pytest ejecuta las pruebas,
incluidas las dos evidencias automatizadas descritas en el enunciado.