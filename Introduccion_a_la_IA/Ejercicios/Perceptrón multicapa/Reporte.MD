# Reporte: Clasificación del Dataset Iris con Perceptrón Multicapa (MLP)

**Asignatura:** Introducción a la Inteligencia Artificial  
**Alumno:** Raul Alejandro Perez Lopez  
**Tema:** Redes Neuronales — Perceptrón Multicapa (MLP)  
**Ejercicio:** Evaluación del Impacto de la Profundidad en el Perceptrón Multicapa  
**Entorno de Ejecución:** Google Colab  

---

## 1. Definición del Experimento e Instancia de Control (Red Default: $4 \times 3 \times 3$)

El objetivo de este reporte es evaluar el comportamiento del entrenamiento de un Perceptrón Multicapa al clasificar las tres especies del dataset **Iris** (*Setosa*, *Versicolor*, *Virginica*) en función de 4 atributos morfológicos (largo y ancho de pétalo y sépalo).

Se implementaron y compararon dos arquitecturas de software sobre los mismas hiperparámetros:
* **Tasa de aprendizaje ($\eta$):** $0.03$
* **Épocas:** 500
* **Función de activación:** Sigmoide en todas las capas
* **Función de pérdida:** Error Cuadrático Medio ($MSE$)

### 1.1. Ejecución de la Red Base ($4 \times 3 \times 3$)

#### 1. Implementación Manual (NumPy)
Se ejecutó el algoritmo de propagación hacia adelante (*forward*) y retropropagación (*backpropagation*) construido manualmente en el notebook `01 Multilayer perceptron.ipynb`.

![Curva de Error NumPy Base](./05_Images/01_Curva_de_error_multilayer_perceptrón.PNG)

* **Comportamiento:** Muestra una caída pronunciada del error inicial de **0.77** hasta aproximadamente **0.35** dentro de las primeras 100 épocas, estabilizándose con una pendiente leve hasta alcanzar un error final de **0.34**.

#### 2. Implementación Framework (Keras / TensorFlow)
Se ejecutó el modelo declarativo `Sequential` utilizando la biblioteca Keras en `02 Keras - multilayer perceptron - iris.ipynb`.

```bash
model.summary()
```

![Keras Model Summary](./05_Images/03_model_summary.PNG)

* **Parámetros entrenables:** 27 parámetros.
* **Curva de pérdida:**

```bash
plt.plot(history.history['loss'])
plt.show()
```

![Keras Model Loss Curve](./05_Images/04_model_loss_curve.PNG)

* **Comportamiento:** La pérdida se reduce suavemente desde un valor inicial de **0.2512** hasta **0.1958**.

#### 3. Interpretación de la Red Base

Podemos notar discrepancia entre la pérdida inicial de NumPy ($0.77$) y Keras ($0.25$) radica principalmente en el esquema de inicialización de pesos. Mientras NumPy utiliza una distribución aleatoria no optimizada, Keras probablemente aplique por defecto inicializadores avanzados que posicionen a la red en un punto de partida más cercano al mínimo local.
Además, después de las primeras 100 epocas Keras logra reducir un $13\%$ adicional de pérdida general respecto a NumPy, probablemente debido a la optimización interna al usar tensores vectorizados.

---

## 2. Evaluación de Redes Profundas ($4 \times 3 \times 3 \times 3 \times 3$)

Para evaluar el impacto del incremento de profundidad, se agregaron dos capas ocultas intermedias de 3 neuronas cada una, manteniendo constantes el número de entradas ($4$), salidas ($3$), la tasa de aprendizaje ($\eta = 0.03$), las épocas ($500$) y la función de activación (sigmoide).

### 2.1. Implementación Manual (NumPy)

Se adaptaron las matrices de pesos, los cálculos de *forward* y la cadena de gradientes ($\delta$) en el ciclo de retropropagación para procesar las 4 capas.

![Curva de Error Multilayer Perceptron Profunda](./05_Images/02_Curva_de_error_deep_multilayer_perceptrón.PNG)

* **Comportamiento:** Muestra un error inicial de **0.86** que desciende de forma no lineal e inestable (con oscilaciones y picos visibles) hasta alcanzar **0.11** al final de las 500 épocas.

### 2.2. Implementación Framework (Keras / TensorFlow)

Se agregaron dos capas `Dense` adicionales previo a la capa de salida:

```python
model = keras.Sequential([
    layers.Dense(3, activation="sigmoid", name="layer1", input_shape=(4,)),
    layers.Dense(3, activation="sigmoid", name="layer2"),
    layers.Dense(3, activation="sigmoid", name="layer3"),
    layers.Dense(3, activation="sigmoid", name="layer4")
])

```

![Keras Deep Model Summary](./05_Images/05_deep_model_summary.PNG)

* **Parámetros entrenables:** Incremento de 27 a **51 parámetros**.
* **Curva de pérdida:**

![Keras Deep Model Loss Curve](./05_Images/06_deep_model_loss_curve.PNG)

* **Comportamiento:** Muestra un estancamiento severo. La pérdida inicia en **0.2480** y apenas logra reducirse a **0.2310** al término de las 500 épocas, mostrando una pendiente casi plana.

### 2.3. Interpretación de la Red Profunda

Al encadenar 4 capas con activación sigmoide, la derivada utilizada en el backpropagation hace que el gradiente se desvanezca, provocando que la actualización de pesos en las capas iniciales sea prácticamente nula.
Además, el dataset Iris es un problema con baja dimensión (150 muestras, casi linealmente separable). Introducir más capas no aporta capacidad de representación útil y, en presencia de funciones sigmoides + $MSE$, dificulta drásticamente la convergencia.

---

## 3. Resumen Comparativo de Resultados

| Experimento | Arquitectura (Topología) | Parámetros | Loss/Error Inicial | Loss/Error Final | Comportamiento del Aprendizaje |
| --- | --- | --- | --- | --- | --- |
| **NumPy Base** | $4 \times 3 \times 3$ | 27 | 0.7700 | 0.3400 | Caída rápida inicial y estabilización a partir de la época 100. |
| **Keras Base** | $4 \times 3 \times 3$ | 27 | 0.2512 | 0.1958 | Descenso suave y sostenido; óptimo balance de aprendizaje. |
| **NumPy Profunda** | $4 \times 3 \times 3 \times 3 \times 3$ | 51 | 0.8600 | 0.1100 | Descenso inestable con picos; mayor reducción al final. |
| **Keras Profunda** | $4 \times 3 \times 3 \times 3 \times 3$ | 51 | 0.2480 | 0.2310 | **Estancamiento (Flattish):** Gradiente desvanecido limita el ajuste. |

---

## 4. Respuestas al Cuestionario Técnico

### 1. ¿Baja más el error al añadir dos capas, o se estancó / empeoró? ¿Igual en NumPy y en Keras?

* En **Keras**, el aprendizaje se estancó. El error final empeoró pasando de **0.1958** en la red base a **0.2310** en la red profunda.
* En **NumPy**, el valor numérico final del error fue menor (**0.11**), pero la curva mostró una alta inestabilidad durante el entrenamiento, requiriendo más épocas para asentarse.

### 2. ¿Las curvas de NumPy y Keras se parecen con la misma topología? ¿Qué diferencias lo explican?

No se parecen. Las diferencias principales surgen por la inicializacion de pesos, Keras parte de pérdidas bajas ($0.25$), mientras que NumPy utiliza valores iniciales aleatorios lo que provoca un error inicial de ($0.77$), y; Keras probablemente gestiona operaciones matriciales optimizadas, mientras que la implementación manual en NumPy utiliza operaciones en bucle simple sujetas a diferencias en la acumulación de gradientes.

### 3. Con sigmoides apiladas y MSE, ¿tiene sentido que una red más profunda no aprenda mejor en Iris?

Sí, apilar múltiples funciones sigmoides causa el **desvanecimiento del gradiente**, ya que las derivadas se vuelven exponencialmente pequeñas conforme se retropropaga hacia las primeras capas. Además, el problema de Iris es simple y no requiere abstraer características complejas; sobrecargar la red con capas ocultas innecesarias dificulta la optimización cuando se combina con la función de pérdida $MSE$.

---

## 5. Evidencias de Ejecución en Google Colab

A continuación se adjuntan las ligas de los notebook utilizados que acreditan el entrenamiento y las inferencias ejecutadas:

### 5.1 Multilayer perceptron
* **Github:** [Github 13 YOLO ultralytics.ipynb](https://github.com/RaulLopez1903/MIA_Raul_P./blob/main/Introduccion_a_la_IA/Ejercicios/Perceptr%C3%B3n%20multicapa/04%20Multilayer%20perceptron.ipynb)
* **Colab:** [Colab 13 YOLO ultralytics.ipynb](https://colab.research.google.com/github/RaulLopez1903/MIA_Raul_P./blob/main/Introduccion_a_la_IA/Ejercicios/Perceptr%C3%B3n%20multicapa/04%20Multilayer%20perceptron.ipynb)

### 5.2 Keras - Multilayer perceptron
* **Github:** [Github 13 YOLO ultralytics.ipynb](
https://github.com/RaulLopez1903/MIA_Raul_P./blob/main/Introduccion_a_la_IA/Ejercicios/Perceptr%C3%B3n%20multicapa/05%20Keras%20-%20multilayer%20perceptron%20-%20iris.ipynb)
* **Colab:** [Colab 13 YOLO ultralytics.ipynb](https://colab.research.google.com/github/RaulLopez1903/MIA_Raul_P./blob/main/Introduccion_a_la_IA/Ejercicios/Perceptr%C3%B3n%20multicapa/05%20Keras%20-%20multilayer%20perceptron%20-%20iris.ipynb)

