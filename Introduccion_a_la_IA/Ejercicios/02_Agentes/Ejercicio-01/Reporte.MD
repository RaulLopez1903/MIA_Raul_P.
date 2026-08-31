# Reporte de Ejercicio 1 — Mundo del Wumpus

**Curso:** Maestría en Inteligencia Artificial  
**Alumno:** Raúl Alejandro Pérez López  
**Asignatura:** Introducción a la IA  

---

## 1. Configuración de la Cueva (`mi_cueva_4x4.yaml`)

Se diseñó una cueva de cuadrícula 4x4 modificando las posiciones del Wumpus y de los pozos (*pits*) con respecto al mapa clásico (`classic_4x4.yaml`), garantizando la validez de las reglas del entorno:

* **Agente (A):** Inicio en la casilla `[1, 1]`, con orientación `east` y 1 flecha disponible.
* **Wumpus (W):** Ubicado en `[3, 1]` (reubicado de la posición clásica `[1, 3]`).
* **Pozos (P):** Ubicados en `[4, 1]`, `[3, 2]` y `[4, 3]` (reubicados de las posiciones clásicas `[3, 1]`, `[3, 3]`, `[4, 4]`).
* **Oro (G):** Ubicado en `[4, 4]` (reubicado de la posición clásica `[2, 3]`).

### Diagrama ASCII de la Cueva

```text
  Y
4 | .   .   .   G     G = Oro (4,4)
3 | .   P   .   .     P = Pozo (4,1) , (3,2) y (2,3)
2 | .   .   P   .     W = Wumpus (4,1)
1 | A   .   W   P     A = Agente inicio (1,1) mirando al Este
  -----------------
    1   2   3   4   X

```
Una vez definido el entorno se ejecutó `python 01_wumpus_world.py --config config/mi_cueva_4x4.yaml` para la visualización del mismo, cuyo resultado se aprecia en la siguiente imagen:

![Mapa de la cueva](./Images/01-Wumpus_World.PNG)

## Ejecución de los agentes

Ejecutando `python 02_simple_reflex_agent.py --config config/mi_cueva_4x4.yaml`:

![Simple Reflex Agent](./Images/02-Simple_reflex_agent.PNG)

Ejecutando `python 03_model_based_agent.py  --config config/mi_cueva_4x4.yaml`:

![Model Based Agent](./Images/03-Model_based_agent.PNG)

Ejecutando `python 04_goal_based_agent.py   --config config/mi_cueva_4x4.yaml`:

![Goal Based Agent](./Images/04-Goal_based_agent.PNG)

Ejecutando `python 05_utility_based_agent.py --config config/mi_cueva_4x4.yaml`:

![Utility Based Agent](./Images/05-Utility_based_agent.PNG)

Ejecutando `python 06_learning_agent.py --episodes 1500 --config config/mi_cueva_4x4.yaml`:

![Learning Agent](./Images/06-Learning_agent.PNG)

### Resultados 

El resultado de los agentes ante la configuración de la cueva planteada fue el mismo, ninguno logró salir de la cueva con el oro. De hecho, solo el agente con aprendizaje logró salir de la cueva después de una única acción `climb`, el agente basado en utilidad logró derrotar al Wumpus pero en su siguiente paso se encontró con un Pit, por lo que su resultado fue `DIED`; los demás agentes únicamente recorrieron el mapa hasta que agotaron el límite de 200 movimientos.

El agente por reflejo simple gasó sus movimientos al llegar a una casilla donde la percepción fué `stench` y, como está definido que al llegar a una casilla con percepción `stench` o `breeze` la siguiente acción será `TURN_RIGHT`, por lo que el agente llegó a un bucle de giros a la derecha. Este agente podría *tener suerte* si en todo su camino no entra en bucle, la manera de esa suerte podría definirse, por ejemplo, estableciento una configuración del mapa donde el oro esté a ciertos pasos hacia adelante sin ninguna percepción.

El agente basado en modelo al tener memoria de casillas seguras logra cambiar de camino si percibe `stench` o `breeze`, considerando que una casilla segura se define como aquella en la que se hayan visitado dos casillas aledañas sin percepciones, el agente puede continuar siempre que se pueda seguir visitando casillas seguras; en el caso de `mi_cueva_4x4.yaml` el agente no puede seguir ya que llega a `[1, 3]` y no puede avanzar a `[1, 4]` pues aún no está definida como casilla segura, por lo que solo hace giros a la izquierda hasta agotar sus movimientos. Mas aún, si se coloca un Pit cercano a la salida, digamos `[1, 2]`, el agente no hará ningun movimiento de avance pues no puede estar seguro de que la casilla a la que avanzará es segura.

El agente basado en metas llega al mismo bucle que el basado en modelo, este tiene la habilidad de disparar la flecha, pero al estar en bucle en una casilla donde no está bloqueado el camino, si no que se desconoce que sea seguro, gasta sus movimientos girando. 

El agente basado en utilidad toma en principio el mismo camino pero decide que es mejor volver a donde estaba el wumpus, dispara la flecha, sigue pero ahí había un Pit, por lo que pierde.
