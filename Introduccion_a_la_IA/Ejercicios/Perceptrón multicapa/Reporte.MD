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

* **Diferencia de valores iniciales:** La discrepancia entre la pérdida inicial de NumPy ($0.77$) y Keras ($0.25$) radica principalmente en el esquema de inicialización de pesos. Mientras NumPy utiliza una distribución aleatoria no optimizada, Keras aplica por defecto inicializadores avanzados (como *Glorot Uniform* / *Xavier*), lo cual posiciona la red en un punto de partida mucho más cercano al mínimo local.
* **Dinámica de aprendizaje:** Keras logra reducir un $13\%$ adicional de pérdida general respecto a NumPy debido a la optimización interna en la precisión decimal de los tensores vectorizados durante el ajuste por Descenso de Gradiente Estocástico ($SGD$).

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

* **Desvanecimiento del Gradiente (*Vanishing Gradient*):** Al encadenar 4 capas con activación sigmoide ($\sigma(x)$), la derivada utilizada en el backpropagation ($\sigma'(x) = \sigma(x)(1 - \sigma(x))$) toma valores máximos de $0.25$. Al aplicar la regla de la cadena para actualizar los pesos de las primeras capas:

$$\delta^{(l)} = \Big(\prod_{k=l}^{L-1} W^{(k+1)T} \delta^{(k+1)}\Big) \odot \sigma'(z^{(l)})$$

El gradiente se multiplica por valores inferiores a $0.25$ en cada capa retrocedida, provocando que la actualización de pesos en las capas iniciales sea prácticamente nula ($\Delta W \approx 0$).
* **Complejidad del Dataset vs. Arquitectura:** El dataset Iris es un problema con baja dimensión (150 muestras, casi linealmente separable). Introducir más capas no aporta capacidad de representación útil y, en presencia de funciones sigmoides + $MSE$, dificulta drásticamente la convergencia.

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

No se parecen. Las diferencias principales surgen por:

1. **Inicialización de pesos:** Keras utiliza inicialización *Glorot/Xavier*, partiendo de pérdidas bajas ($0.25$). NumPy utiliza valores aleatorios no escalados ($0.77$).
2. **Optimizador y procesamiento:** Keras gestiona operaciones matriciales optimizadas sobre tensores de bajo nivel en TensorFlow, mientras que la implementación manual en NumPy utiliza operaciones en bucle simple sujetas a diferencias en la acumulación de gradientes.

### 3. Con sigmoides apiladas y MSE, ¿tiene sentido que una red más profunda no aprenda mejor en Iris?

Sí, tiene total sentido teórico. Apilar múltiples funciones sigmoides causa el **desvanecimiento del gradiente**, ya que las derivadas se vuelven exponencialmente pequeñas conforme se retropropaga hacia las primeras capas. Además, el problema de Iris es simple y no requiere abstraer características complejas; sobrecargar la red con capas ocultas innecesarias dificulta la optimización cuando se combina con la función de pérdida $MSE$.
