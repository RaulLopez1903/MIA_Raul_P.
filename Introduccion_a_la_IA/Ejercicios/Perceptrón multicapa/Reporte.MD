# Reporte

**Materia:** Introducción a la Inteligencia Artificial
**Alumno:** Raul Alejandro Perez Lopez
**Tema:** Perceptrón Multicapa
**Ejercicio:** Más capas en el perceptrón multicapa (Iris)

---

## 1. Ejecución de redes default

1. Numpy 
Después de haber creado la copia de ```04 Multilayer perceptron.ipynb``` se ejecutaron todas las celdas en el entorno de Colab, con la topología 4X3X3 se obtuvo la siguiente curva de error:

![]

Donde el valor de error al final de las 500 epocas fue de **0.057507**.

2. Keras
Para  ```05 Keras - multilayer perceptron.ipynb```, con la misma topología se obtuvo la curva de error:

![]

Con un valor de pérdida final de **0.1958**.

3. Interpretación

Puede notarse que las curvas de error tienen un comportamiento distinto, la implementación con numpy inicializa con un error de **0.8297207** se notan unos picos hacia $0.4$ donde comienza un descenso suave, por contraparte, en keras la pérdida comienza en **0.2512**, se nota una caida empinada hacia 0.22 y suave hacia la pérdida final. Esto podría deberse a la inicialización de los parámetros, en Numpy se hace aleatoriamente, mientras que Keras puede que tenga una mejor manera de inicializar y por eso la pérdida comienza mucho menor, aunque como vimos, en numpy el error termina siendo menor al final de las 500 epocas.

---

## 2. Ejecución de redes profundas (4X3X3X3X3)

1. Numpy

![]

2. Keras

![]


3. Interpretación

---

## 3. Resultados





