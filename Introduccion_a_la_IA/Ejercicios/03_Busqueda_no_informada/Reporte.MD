# Reporte de Búsqueda No Informada: Mapa de Rumania

**Asignatura:** Introducción a la Inteligencia Artificial  
**Alumno:** Raul Alejandro Perez Lopez  
**Tema:** Algoritmos de Búsqueda No Informada  
**Ejercicio:** Ejercicio 1 — Comparación y Evaluación de BFS, UCS, DFS, DLS e IDS  

---

## 1. Definición del Problema e Instancia Seleccionada

El objetivo de este reporte es evaluar y comparar el comportamiento de cinco algoritmos de búsqueda no informada al resolver el problema de encontrar rutas en el mapa de Rumania (*AIMA Cap. 3*).

Para este experimento se seleccionó la ruta:
* **Origen:** `Timisoara`
* **Destino:** `Bucharest`

### 1.1. Grafo General de Rumania
![Mapa Completo de Rumania](./03_Images/01_romania_map.PNG)

### 1.2. Subgrafo Relevante de la Instancia
A continuación se presenta el subgrafo que conecta `Timisoara` con `Bucharest` a través de las distintas rutas exploradas por los algoritmos, incluyendo las distancias reales en kilómetros ($km$) entre ciudades adyacentes:

```text
                  [Arad]
                 /      \
               118       140
               /          \
   [Timisoara]             [Sibiu]
                           /     \
                         99       80
                        /           \
               [Fagaras]             [Rimnicu Vilcea]
                  |                         |
                 211                       97
                  |                         |
              [Bucharest] <--- 101 --- [Pitesti]

```

* **Ruta A (Menos saltos / Hops):** `Timisoara` → `Arad` (118) → `Sibiu` (140) → `Fagaras` (99) → `Bucharest` (211)
* *Profundidad:* 4 carreteras | *Distancia:* $118 + 140 + 99 + 211 = \mathbf{568\text{ km}}$


* **Ruta B (Menor distancia total):** `Timisoara` → `Arad` (118) → `Sibiu` (140) → `Rimnicu Vilcea` (80) → `Pitesti` (97) → `Bucharest` (101)
* *Profundidad:* 5 carreteras | *Distancia:* $118 + 140 + 80 + 97 + 101 = \mathbf{536\text{ km}}$

---

## 2. Resumen Comparativo de Resultados

| Algoritmo | Estado (*Status*) | Camino Hallado (*Path*) | Profundidad (*Depth*) | Costo Total ($km$) | Nodos Expandidos | Nodos Generados |
| --- | --- | --- | --- | --- | --- | --- |
| **BFS** | `success` | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 7 | 17 |
| **UCS** | `success` | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest | 5 | 536 km | 12 | 31 |
| **DFS** | `success` | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 4 | 12 |
| **DLS ($l = 2$)** | `cutoff` | *Ninguno (Corte por límite)* | -- | -- | 3 | 8 |
| **DLS ($l = 4$)** | `success` | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 4 | 6 |
| **IDS** | `success` | Timisoara → Arad → Sibiu → Fagaras → Bucharest | 4 | 568 km | 14 | 34 |

---

## 3. Análisis de Resultados

### 3.1. Comparación BFS vs. UCS (Optimalidad en Saltos vs. Costo)

* **BFS (Breadth-First Search):** Garantiza la optimalidad en el número de saltos (*hops*). Encontró una ruta de **4 carreteras** con una distancia total de **568 km**. Al explorar el árbol por niveles, BFS prioriza el camino con la menor cantidad de aristas sin considerar el peso en kilómetros.
* **UCS (Uniform-Cost Search):** Garantiza la optimalidad en el costo acumulado $g(n)$. Encontró una ruta de **5 carreteras**, pero con una distancia de **536 km** (un ahorro de **32 km** en comparación con BFS). UCS expande los nodos ordenados en su frontera por costo real, eligiendo desviarse por `Rimnicu Vilcea` y `Pitesti` al ser tramos más cortos en kilómetros que el tramo directo por `Fagaras`.

### 3.2. Comportamiento de DFS y Criterio de Expansión

* **DFS (Depth-First Search):** Expandió un número reducido de nodos (**4 expandidos**) y encontró la ruta por `Fagaras`.
* *Nota de comportamiento:* Debido a que los vecinos se expanden en **orden alfabético**, la primera rama explorada tras `Sibiu` fue `Fagaras` antes que `Rimnicu Vilcea`. Dado que esa rama contenía directamente a `Bucharest` a profundidad 4, terminó con éxito. Si el orden alfabético hubiese favorecido un camino sin salida o más largo, DFS lo habría recorrido por completo sin ofrecer garantías de optimalidad ni en saltos ni en kilómetros.

### 3.3. Evaluación de DLS e IDS

* **DLS con límite 2 ($l = 2$):** Retornó `cutoff`. La solución más corta en número de saltos está a profundidad 4. Con un límite de 2, el algoritmo solo alcanza ciudades como `Arad`, `Lugoj` o `Mehadia`, por lo que detuvo la exploración antes de llegar a la meta.
* **DLS con límite 4 ($l = 4$):** Al incrementar el límite a 4 (profundidad suficiente), el algoritmo pasó de `cutoff` a `success`, devolviendo la solución de 4 saltos igual a la de BFS.
* **IDS (Iterative Deepening Search):** Ejecutó de forma iterativa búsquedas en profundidad limitada desde $l = 0$ hasta $l = 4$. Coincidió con la solución de BFS en número de saltos (4) y costo (568 km). Aunque expande un mayor número total de nodos (**14 expandidos**) debido a las re-evaluaciones de los niveles superiores, combina la **eficiencia de memoria de DFS** con la **optimalidad en saltos de BFS**.

---

## 4. Evidencias de Ejecución

A continuación se adjuntan las capturas de terminal que respaldan las ejecuciones de los comandos:

### 4.1. Búsqueda a lo ancho (BFS)

```bash
python 02_breadth_first_search.py --from-city Timisoara --to Bucharest
```

![Breadth First Search](./03_Images/02_breadth_first_search.PNG)

### 4.2. Búsqueda con costo uniforme (UCS)

```bash
python 03_uniform_cost_search.py --from-city Timisoara --to Bucharest
```

![Uniform Cost Search](./03_Images/03_uniform_cost_search.PNG)

### 4.3. Búsqueda a lo profundo (DFS)

```bash
python 04_depth_first_search.py --from-city Timisoara --to Bucharest
```

![Depth First Search](./03_Images/04_depth_first_search.PNG)

### 4.4. Búsqueda con profundidad limitada (DLS, Límite = 2)

```bash
python 05_depth_limited_search.py --from-city Timisoara --to Bucharest --limit 2
```

![Depth Limited Searh Limit 2](./03_Images/05_depth_limited_search_limit_2.PNG)

### 4.5. Búsqueda con profundidad limitada (DLS, Límite = 4)

```bash
python 05_depth_limited_search.py --from-city Timisoara --to Bucharest --limit 4
```

![Depth Limited Searh Limit 4](./03_Images/05_depth_limited_search_limit_4.PNG)

### 4.6. Búsqueda por profundización iterativa (IDS)

```bash
python 06_iterative_deepening_search.py --from-city Timisoara --to Bucharest
```

![Iterative Deepening Search](./03_Images/06_iterative_deepening_search.PNG)
