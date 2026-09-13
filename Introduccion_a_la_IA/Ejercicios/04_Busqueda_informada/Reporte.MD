# Reporte de Búsqueda Informada: Mapa de Rumania

**Asignatura:** Introducción a la Inteligencia Artificial  
**Alumno:** Raul Alejandro Perez Lopez  
**Tema:** Algoritmos de Búsqueda Informada  
**Ejercicio:** Ejercicio 1 — Comparación y Evaluación de Greedy Best-First Search y A*  

---

## 1. Definición del Problema e Instancia Seleccionada

En este ejercicio se evalúa la eficacia de la incorporación de conocimiento heurístico mediante los algoritmos **Greedy Best-First Search** y **A\*** al resolver la ruta entre:
* **Origen:** `Timisoara`
* **Destino:** `Bucharest`

### 1.1. Grafo General de Rumania
![Mapa Completo de Rumania](./04_Images/01_romania_map.PNG)

### 1.2. Subgrafo Relevante de la Instancia
El siguiente diagrama integra las ciudades exploradas por ambos algoritmos, indicando las distancias reales en kilómetros entre ciudades adyacentes ($g$) y los valores heurísticos de distancia en línea recta hacia `Bucharest` ($h$):

```text
                           [Arad] (h=366)
                          /      \
                      118         140
                      /             \
          [Timisoara]                [Sibiu] (h=253)
           (h=329)                   /     \
           /                       99       80
         111                      /           \
         /               [Fagaras]             [Rimnicu Vilcea] (h=193)
   [Lugoj] (h=244)       (h=176)                      |
      |                     |                         97
     70                    211                        |
      |                     |                     [Pitesti] (h=100)
   [Mehadia] (h=241)        |                         |
      |                     |                        101
     75                     |                         |
      |                     v                         v
   [Drobeta] (h=242) ----> [Craiova] (h=160) ----138----> [Bucharest] (h=0)

```

#### Comparativa de Rutas Generadas:

* **Ruta Greedy (Guiada solo por $h$):** `Timisoara` → `Lugoj` → `Mehadia` → `Drobeta` → `Craiova` → `Pitesti` → `Bucharest`
* *Profundidad:* 6 carreteras | *Distancia Total:* $111 + 70 + 75 + 120 + 138 + 101 = \mathbf{615\text{ km}}$

* **Ruta A* (Optimizada por $f = g + h$):** `Timisoara` → `Arad` → `Sibiu` → `Rimnicu Vilcea` → `Pitesti` → `Bucharest`
* *Profundidad:* 5 carreteras | *Distancia Total:* $118 + 140 + 80 + 97 + 101 = \mathbf{536\text{ km}}$

---

## 2. Resumen Comparativo de Resultados

| Algoritmo | Estado (*Status*) | Camino Hallado (*Path*) | Profundidad (*Depth*) | Costo Total ($km$) | Nodos Expandidos | Nodos Generados | Tabla Heurística |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Greedy Search** | `success` | Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest | 6 | 615 km | 6 | 15 | AIMA Table |
| **A* Search** | `success` | Timisoara → Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest | 5 | 536 km | 10 | 27 | AIMA Table |

---

## 3. Análisis Técnico de Resultados

### 3.1. Evaluación del Camino Hallado: A* vs. Greedy Search

* **Greedy Search (Miopía Heurística):** No encontró el camino de menor kilometraje y sufrió un desvío significativo. Al estar en `Timisoara`, evaluó las opciones de `Lugoj` ($h = 244$) y `Arad` ($h = 366$). Como Greedy solo evalúa la heurística ($f(n) = h(n)$), eligió `Lugoj` por parecer estar más cerca de `Bucharest` en línea recta. Esto lo encadenó a rodear toda la región sur pasando por `Mehadia`, `Drobeta` y `Craiova`, resultando en una ruta subóptima de **615 km**.
* **A* Search (Optimalidad de Costo):** Halló la ruta óptima de **536 km**. A* utiliza la función de evaluación $f(n) = g(n) + h(n)$. Aunque `Lugoj` tenía un valor $h$ atractivo, conforme avanzó la exploración, el costo real acumulado ($g$) penalizó esa rama. Esto permitió a A* corregir el rumbo a través de `Arad`, `Sibiu`, `Rimnicu Vilcea` y `Pitesti`, garantizando el camino más corto en distancia total.

### 3.2. Suboptimalidad de Greedy Search con Heurísticas Admisibles

* Greedy Search ignora por completo el costo acumulado de la trayectoria recorrida ($g(n)$). Su única meta es minimizar la estimación restante $h(n)$.
* Aunque la heurística $h(n)$ sea **admisible** (nunca sobreestima la distancia real al objetivo), Greedy toma decisiones totalmente "miopes" basándose solo en el atractivo del nodo inmediato. No identifica si para avanzar unos pocos kilómetros en línea recta está recorriendo tramos de carretera extremadamente largos en el mundo real, cayendo fácilmente en soluciones locales subóptimas.

### 3.3. Monotonicidad de la Función $f(n)$ en A*

* En el camino óptimo encontrado por A*, los valores de la función de evaluación $f(n)$ son **monótonamente no decrecientes** ($f(n_1) \le f(n_2) \le \dots$).
* Esto sucede porque la heurística de distancia en línea recta es **consistente (o monótona)**, cumpliendo con la desigualdad triangular:

$$h(n) \le c(n, a, n') + h(n')$$

Dado que la estimación nunca sobrepasa el costo real de viajar a un nodo vecino más su propia heurística, la suma total $f(n) = g(n) + h(n)$ mantiene un crecimiento constante o se preserva a lo largo del camino óptimo a medida que se revela la verdadera geografía del mapa.

---

## 4. Evidencias de Ejecución

A continuación se presentan las capturas de pantalla de la ejecución de las herramientas y algoritmos:

### 4.1. Evaluación de Heurísticas

```bash
python 02_heuristics.py --from-city Timisoara --to Bucharest
```

![Heuristics](./04_Images/02_heuristics.PNG)

### 4.2. Búsqueda Greedy Best-First Search

```bash
python 03_greedy_best_first_search.py --from-city Timisoara --to Bucharest
```

![Greedy Search](./04_Images/03_greedy_best_first_search.PNG)

### 4.3. Búsqueda A* (A-Star Search)

```bash
python 04_a_star_search.py --from-city Timisoara --to Bucharest
```

![A Star Search](./04_Images/04_a_star_search.PNG)

