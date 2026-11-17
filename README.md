# MIA_Raul_P

Repositorio personal de trabajos, prácticas y proyectos de la Maestría en Inteligencia Artificial de la Universidad Autónoma de Yucatán (UADY).

El repositorio reúne materiales de varias asignaturas. Contiene notebooks, presentaciones, reportes, ejercicios de programación, conjuntos de datos, aplicaciones de ejemplo y resultados de prácticas.

## Contenido del repositorio

| Carpeta | Asignatura | Contenido principal |
|---|---|---|
| [Introduccion_a_la_IA](./Introduccion_a_la_IA/) | Introducción a la Inteligencia Artificial | Agentes, búsqueda, visión computacional, clustering, redes neuronales y un proyecto RAG |
| [Programacion_para_la_IA](./Programacion_para_la_IA/) | Programación para la Inteligencia Artificial | Python moderno, NumPy, pandas, PyTorch, visualización, SQL/NoSQL, LangGraph, LangChain y proyecto final MCP |
| [Aprendizaje_supervisado](./Aprendizaje_supervisado/) | Aprendizaje supervisado | Materiales por unidades y módulos, notebooks de examen y prácticas, evaluaciones y sitio de publicación |

## Introducción a la Inteligencia Artificial

La carpeta [Introduccion_a_la_IA](./Introduccion_a_la_IA/) contiene notas y ejercicios organizados por tema:

- conceptos básicos de inteligencia artificial;
- agentes inteligentes y análisis PEAS;
- búsqueda no informada e informada;
- visión computacional con YOLO;
- agrupamiento con K-medias;
- perceptrón multicapa y redes neuronales;
- proyecto RAG con recuperación de documentos, embeddings y ChromaDB.

Los ejercicios incluyen reportes en Markdown, notebooks de Jupyter, imágenes de evidencia, presentaciones PDF y archivos de configuración YAML.

### Proyecto RAG

[RAG_Project](./Introduccion_a_la_IA/RAG_Project/) es una implementación experimental de recuperación aumentada por generación. Utiliza documentos locales, FastAPI, Streamlit, ChromaDB y modelos de Google Gemini.

El proyecto incluye:

- archivos de fuente en `data/`;
- configuración de entorno mediante `.env.example`;
- base vectorial persistente en `chroma/`;
- dependencias en `requirements.txt`.

## Programación para la Inteligencia Artificial

La carpeta [Programacion_para_la_IA](./Programacion_para_la_IA/) organiza el trabajo por unidades y sesiones:

### Unidad 1: Python moderno

- curso acelerado de Python y Zen de Python;
- tipado, Pydantic y modelos de datos;
- iteradores, recursos y concurrencia;
- organización de proyectos y reproducibilidad.

Cada sesión cuenta con una guía propia y prácticas ejecutables. Los proyectos usan Python moderno y, en varios casos, [`uv`](https://docs.astral.sh/uv/) para gestionar dependencias y entornos.

### Unidad 2: Procesamiento y análisis de datos

- NumPy y vectorización;
- pandas y análisis del conjunto de datos Titanic;
- PyTorch y entrenamiento básico;
- visualización de datos;
- pruebas automatizadas y notebooks.

Los proyectos incluyen aplicaciones pequeñas, módulos de procesamiento, conjuntos de datos y resultados generados.

### Unidad 3: Integración y calidad

- Python como cliente de SQLite y Neo4j;
- workflows de datos con LangGraph;
- agentes y herramientas MCP con LangChain;
- consultas parametrizadas, validación y organización de resultados.

La sesión de LangChain se marca como opcional y puede requerir credenciales propias para ejecutar el modelo.

### Proyecto final

[proyecto-final](./Programacion_para_la_IA/proyecto-final/) implementa un servidor MCP por HTTP para buscar y analizar productos de **Amazon Reviews 2023 · Electronics**.

El servidor expone herramientas para:

- búsqueda semántica de productos;
- análisis de calificaciones;
- comparación de productos;
- manejo de consultas inválidas y productos desconocidos.

El proyecto utiliza embeddings con PyTorch o NumPy, FastAPI y MCP. Los datos seleccionados se limitan a 600 productos y 6992 reseñas, por lo que los resultados no representan la totalidad del catálogo o de las opiniones de Amazon.

## Aprendizaje supervisado

La carpeta [Aprendizaje_supervisado](./Aprendizaje_supervisado/) contiene materiales del curso de aprendizaje supervisado:

- planeación didáctica;
- presentaciones de introducción y unidades;
- notebooks de actividades y soluciones;
- prácticas y exámenes de módulos;
- conjuntos de datos de estabilidad de redes eléctricas;
- un examen final publicado como sitio HTML;
- una página de presentación del curso.

Las unidades 1 a 3 incluyen actividades de EDA, preprocesamiento y selección de variables. Las unidades posteriores contienen presentaciones y notebooks sobre SVM, redes neuronales, evaluación de hiperparámetros, ensambles y boosting.

El README específico de esta línea académica se encuentra en [Aprendizaje_supervisado/README.md](./Aprendizaje_supervisado/README.md).

## Tecnologías utilizadas

Según el proyecto o la práctica, el repositorio utiliza:

- Python y Jupyter Notebook;
- NumPy y pandas;
- PyTorch;
- scikit-learn;
- TensorFlow / Keras;
- FastAPI y Streamlit;
- Pydantic;
- LangGraph y LangChain;
- MCP;
- SQLite y Neo4j;
- ChromaDB;
- modelos de embeddings y Google Gemini;
- YOLO / Ultralytics;
- OpenCV;
- UV para entornos y dependencias;
- Git y GitHub Pages.

## Ejecución general

No existe una aplicación única para todo el repositorio. Los proyectos suelen tener su propio entorno, notebook o guía de ejecución.

### Notebooks

Muchas prácticas pueden abrirse directamente con Jupyter, VS Code o Google Colab:

```bash
python -m pip install jupyter
jupyter notebook
```

### Proyectos administrados con `uv`

Dentro de la carpeta del proyecto:

```bash
uv sync --locked
uv run --locked python main.py
```

Los proyectos individuales pueden usar otros nombres de archivo. Consulta su README, notebook o archivo `pyproject.toml`.

### Proyecto RAG

Desde `Introduccion_a_la_IA/RAG_Project`:

```bash
python -m pip install -r requirements.txt
```

Debe configurarse un archivo `.env` a partir de `.env.example` antes de ejecutar las funciones que requieran una API de Google Gemini.

## Convenciones y contenido generado

Algunos directorios contienen artefactos de ejecución, entornos virtuales, cachés, salidas de pruebas o bases de datos locales. Se recomienda revisar los archivos `.gitignore` de cada proyecto antes de compartir o publicar cambios.

Los solucionarios y archivos de examen pueden estar restringidos por las reglas propias de cada asignatura. No deben publicarse contenidos que el curso indique mantener privados.

## Autor

Raúl Alejandro Pérez López
