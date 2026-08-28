# Reporte de Ejercicio 1 — Mundo del Wumpus

**Curso:** Maestría en Inteligencia Artificial  
**Alumno:** Raúl Pérez  
**Asignatura:** Agentes Inteligentes  
**Archivo de Configuración:** `config/mi_cueva_4x4.yaml`  

---

## 1. Configuración de la Cueva (`mi_cueva_4x4.yaml`)

Se diseñó una cueva de cuadrícula 4x4 modificando las posiciones del Wumpus y de los pozos (*pits*) con respecto al mapa clásico (`config/classic_4x4.yaml`), garantizando la validez de las reglas del entorno:

* **Agente (A):** Inicio en la casilla `[1, 1]`, con orientación `east` y 1 flecha disponible.
* **Wumpus (W):** Ubicado en `[4, 1]` (reubicado de la posición clásica `[1, 3]`).
* **Pozos (P):** Ubicados en `[2, 3]` y `[3, 2]` (reubicados de las posiciones clásicas `[3, 1]`, `[3, 3]`, `[4, 4]`).
* **Oro (G):** Ubicado en `[4, 4]`.

### Diagrama ASCII de la Cueva

```text
  Y
4 | .   .   .   G     G = Oro (4,4)
3 | .   P   .   .     P = Pozo (2,3) y (3,2)
2 | .   .   P   .     W = Wumpus (4,1)
1 | A   .   .   W     A = Agente inicio (1,1) mirando al Este
  -----------------
    1   2   3   4   X
