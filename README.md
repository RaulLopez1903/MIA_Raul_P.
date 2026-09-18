# MIA_Raul_P

Repositorio personal de la asignatura de Introducción a la Inteligencia Artificial de la Maestría en Inteligencia Artificial UADY (2026-2027). Aquí se documentan ejercicios, reportes, notas y experimentos realizados a lo largo del curso, con enfoque en agentes inteligentes, búsqueda, visión computacional, clustering y redes neuronales.

## Descripción general

Este repositorio recopila el trabajo académico desarrollado en la carpeta `Introduccion_a_la_IA`, organizada por temas y actividades. El contenido incluye:

- ejercicios prácticos con scripts y ejemplos de programación,
- reportes escritos con análisis técnico y resultados,
- imágenes de evidencia de ejecución,
- notebooks de Python para modelos de aprendizaje automático,
- notas de lectura y conceptos fundamentales de IA.

## Estructura del repositorio

```text
MIA_Raul_P/
├── README.md
└── Introduccion_a_la_IA/
    ├── Ejercicios/
    │   ├── 01_Conceptos_básicos_de_Inteligencia_Artificial/
    │   │   └── Ejercicio-01.MD
    │   ├── 02_Agentes/
    │   │   ├── Ejercicio-01/
    │   │   │   ├── Images/
    │   │   │   ├── Reporte.MD
    │   │   │   ├── mi_cueva_4x4.yaml
    │   │   │   └── mi_cueva_dificil_4x4.yaml
    │   │   └── Ejercicio-02/
    │   │       └── Reporte.MD
    │   ├── 03_Busqueda_no_informada/
    │   │   ├── 03_Images/
    │   │   └── Reporte.MD
    │   ├── 04_Busqueda_informada/
    │   │   ├── 04_Images/
    │   │   └── Reporte.MD
    │   ├── 06_Vision_computacional/
    │   │   ├── 06_Images/
    │   │   ├── 13 YOLO ultralytics.ipynb
    │   │   └── Reporte.MD
    │   ├── 07_Clustering/
    │   │   ├── 07_Images/
    │   │   ├── 01 K-medias.ipynb
    │   │   └── Reporte.MD
    │   └── Perceptrón multicapa/
    │       ├── 05_Images/
    │       ├── 04 Multilayer perceptron.ipynb
    │       ├── 05 Keras - multilayer perceptron - iris.ipynb
    │       └── Reporte.MD
    └── Notas/
        └── 01_Conceptos_básicos_de_Inteligencia_Artificial.MD
```

## Temas abordados

### 1. Conceptos básicos de IA

Se incluyen definiciones y fundamentos introductorios sobre Inteligencia Artificial, así como una primera nota de lectura relacionada con el ensayo de Alan Turing: "Computing Machinery and Intelligence".

### 2. Agentes inteligentes

Se exploran distintos tipos de agentes:

- agente reactivo simple,
- agente basado en modelo,
- agente basado en metas,
- agente basado en utilidad,
- agente con aprendizaje,
- análisis PEAS para diferentes aplicaciones.

El ejercicio más destacado es la implementación y evaluación del entorno del Wumpus World, con configuraciones YAML y reportes visuales comparando el comportamiento de cada agente.

### 3. Búsqueda no informada

Se comparan algoritmos clásicos como:

- BFS (Breadth-First Search)
- UCS (Uniform-Cost Search)
- DFS (Depth-First Search)
- DLS (Depth-Limited Search)
- IDS (Iterative Deepening Search)

El caso de estudio es la ruta entre Timisoara y Bucharest en el mapa de Rumania, con métricas de profundidad, costo, nodos expandidos y generados.

### 4. Búsqueda informada

Se evaluan técnicas con heurísticas, principalmente:

- Greedy Best-First Search
- A* Search

Se analizan diferencias entre una estrategia miopista y otra que incorpora costo acumulado más la estimación heurística.

### 5. Visión computacional

Se trabaja con detección de objetos usando YOLOv8 y su inferencia sobre imágenes base y personalizadas. El repositorio incluye:

- notebooks de Google Colab,
- imágenes de salida,
- análisis del comportamiento del modelo,
- discusión sobre precisión, objetos omitidos y ajuste de parámetros.

### 6. Clustering

Se realiza un ejercicio de K-medias con visualización de centroides, inercia, silhouette score y separación de clústeres. El contenido incluye notebook y gráficas del proceso.

### 7. Redes neuronales y perceptrón multicapa

Se estudia el entrenamiento de perceptrones multicapa para clasificar el dataset Iris, comparando implementaciones manuales y con Keras/TensorFlow. Se analizan aspectos como:

- profundidad de la red,
- inicialización de pesos,
- desvanecimiento del gradiente,
- efecto de añadir capas ocultas.

## Archivos relevantes

- `Introduccion_a_la_IA/Notas/01_Conceptos_básicos_de_Inteligencia_Artificial.MD` — notas y materiales introductorios.
- `Introduccion_a_la_IA/Ejercicios/02_Agentes/Ejercicio-01/Reporte.MD` — análisis del mundo del Wumpus.
- `Introduccion_a_la_IA/Ejercicios/03_Busqueda_no_informada/Reporte.MD` — comparación de algoritmos de búsqueda no informada.
- `Introduccion_a_la_IA/Ejercicios/04_Busqueda_informada/Reporte.MD` — comparación de búsqueda informada.
- `Introduccion_a_la_IA/Ejercicios/06_Vision_computacional/Reporte.MD` — detección de objetos con YOLO.
- `Introduccion_a_la_IA/Ejercicios/07_Clustering/Reporte.MD` — análisis de clustering con K-medias.
- `Introduccion_a_la_IA/Ejercicios/Perceptrón multicapa/Reporte.MD` — estudio del MLP y sus derivados.

## Herramientas y entorno

Los ejercicios utilizan principalmente:

- Python
- Jupyter Notebook
- Google Colab
- NumPy
- TensorFlow / Keras
- OpenCV / ultralytics (en visión computacional)
- YAML para configuraciones de entornos

## Propósito del repositorio

Este repositorio sirve como portafolio académico y registro de aprendizaje del curso de Introducción a la Inteligencia Artificial, mostrando tanto la teoría como la práctica aplicada de los principales paradigmas de la IA.

## Autor

Raúl Alejandro Pérez López
