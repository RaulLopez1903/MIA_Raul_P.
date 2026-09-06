```markdown
# Reporte de Ejercicio 1 — Mundo del Wumpus

**Curso:** Maestría en Inteligencia Artificial  
**Alumno:** Raúl Alejandro Pérez López  
**Asignatura:** Introducción a la IA  

---

## 1. Configuración de la Cueva (`mi_cueva_4x4.yaml`)

Se diseñó un entorno de cuadrícula de 4x4 modificando las posiciones del Wumpus, los pozos (*pits*) y el oro con respecto a la configuración clásica (`classic_4x4.yaml`), garantizando la validez de las reglas del entorno:

* **Agente (A):** Ubicación inicial en `[1, 1]`, orientación `east` (Este) y 1 flecha disponible.
* **Wumpus (W):** Reubicado en la casilla `[3, 1]` (posición clásica: `[1, 3]`).
* **Pozos (P):** Reubicados en las casillas `[4, 1]`, `[3, 2]` y `[4, 3]` (posiciones clásicas: `[3, 1]`, `[3, 3]`, `[4, 4]`).
* **Oro (G):** Reubicado en la casilla `[4, 4]` (posición clásica: `[2, 3]`).

### Diagrama ASCII de la Cueva

```text
  Y
4 | .   .   .   G     G = Oro [4, 4]
3 | .   .   P   .     P = Pozos [4, 1], [3, 2], [4, 3]
2 | .   P   .   .     W = Wumpus [3, 1]
1 | A   .   W   P     A = Agente inicio [1, 1] (mirando al Este)
  -----------------
    1   2   3   4   X

```

Tras definir la configuración en el archivo YAML, se verificó el entorno ejecutando:

```bash
python 01_wumpus_world.py --config config/mi_cueva_4x4.yaml

```

El mapa generado se visualiza a continuación:

---

## 2. Ejecución de los Agentes

Se ejecutaron los scripts correspondientes a las distintas arquitecturas de agentes para evaluar su desempeño en el entorno diseñado:

1. **Agente de Reflejo Simple:**
```bash
python 02_simple_reflex_agent.py --config config/mi_cueva_4x4.yaml

```


2. **Agente Basado en Modelo:**
```bash
python 03_model_based_agent.py --config config/mi_cueva_4x4.yaml

```


3. **Agente Basado en Metas:**
```bash
python 04_goal_based_agent.py --config config/mi_cueva_4x4.yaml

```


4. **Agente Basado en Utilidad:**
```bash
python 05_utility_based_agent.py --config config/mi_cueva_4x4.yaml

```


5. **Agente con Aprendizaje:**
```bash
python 06_learning_agent.py --episodes 1500 --config config/mi_cueva_4x4.yaml

```



---

## 3. Análisis de Resultados

### 3.1. Generalidades de Desempeño

Bajo la configuración planteada, ningún agente logró cumplir el objetivo de extraer el oro y salir exitosamente de la cueva:

* **Agente con Aprendizaje:** Salió de la cueva de forma inmediata ejecutando la acción `climb` en el primer paso.
* **Agente Basado en Utilidad:** Logró derrotar al Wumpus disparando la flecha; sin embargo, al avanzar hacia la siguiente casilla cayó en un pozo (*Pit*), concluyendo en estado `DIED`.
* **Agentes de Reflejo Simple, Basado en Modelo y Basado en Metas:** Recorrieron el mapa en bucles de movimientos hasta agotar el límite establecido de 200 pasos.

### 3.2. Agente de Reflejo Simple (Análisis de Falla o Suerte)

El agente de reflejo simple entra en un bucle infinito al ingresar a una casilla con percepción de hedor (`stench`). Debido a que su regla de condición-acción establece girar a la derecha (`TURN_RIGHT`) cuando percibe `stench` o brisa (`breeze`), el agente queda atrapado ejecutando giros sucesivos en la misma casilla.

Este agente solo podría *tener suerte* y resolver el problema si la disposición del mapa le permite encontrar un camino directo hacia el oro sin pasar por casillas adyacentes a pozos o al Wumpus, evitando así activar las percepciones que disparan la regla de giro.

### 3.3. Agente Basado en Modelo y Variación con Pozos

El agente basado en modelo mantiene un registro de las casillas clasificadas como "seguras" (definidas como aquellas con al menos dos casillas adyacentes visitadas sin percepciones de riesgo). Ante señales de `stench` o `breeze`, el agente redirige su trayectoria solo hacia casillas que pueda confirmar como seguras.

En la cueva `mi_cueva_4x4.yaml`, el agente se detiene al llegar a la casilla `[1, 3]`: al no tener la certeza de que la casilla `[1, 4]` sea segura, evita avanzar y se limita a girar a la izquierda hasta consumir sus 200 movimientos.

* **Efecto de acercar o alejar un pozo:** Si se posiciona un pozo en una casilla más cercana a la salida (por ejemplo, en `[1, 2]`), la percepción de brisa generada al inicio privará al agente de confirmar casillas vecinas como seguras. En consecuencia, el agente restringirá totalmente sus desplazamientos frontales y entrará en bucle de giros sin realizar ningún avance efectivo.

### 3.4. Agente Basado en Metas y Agente Basado en Utilidad

* **Basado en Metas:** Aunque cuenta con la capacidad operativa para disparar la flecha, al quedar atrapado en una zona donde desconoce si el camino subsecuente es seguro, prioriza girar sobre el avance, gastando todos sus movimientos en el bucle sin ejecutar el disparo.
* **Basado en Utilidad:** Evalúa una función de utilidad que lo lleva a retornar a la posición del Wumpus y disparar. No obstante, al no calcular la probabilidad de riesgo de la casilla posterior, avanza hacia un pozo no detectado y muere.

```

```
