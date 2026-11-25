# Distribución temática.

## Introducción

### Sesión 1: Fundamentos
* Introducción al aprendizaje no supervisado
* Aprendizaje supervisado vs.\ no supervisado; tipos de problemas
* Preprocesamiento: valores faltantes, escalamiento y estandarización
* Medidas de distancia y similitud (euclidiana, Manhattan, coseno, Mahalanobis)
* La maldición de la dimensionalidad
* Actividad: Configuración del entorno; exploración de un conjunto de datos sin etiquetas

## Unidad 1: Algoritmos de agrupamiento

### Sesión 2: k-medias (*k-means*)
* Algoritmo de Lloyd y función objetivo (inercia)
* Inicialización k-means++ y múltiples reinicios
* Elección de $k$: método del codo y coeficiente de silueta
* Limitaciones: forma esférica, escala y valores atípicos
* Actividad: Segmentación de clientes con k-medias


### Sesión 3: Agrupamiento jerárquico
* Enfoques aglomerativo y divisivo
* Criterios de enlace: simple, completo, promedio y Ward
* Dendrogramas y corte del árbol
* Complejidad computacional y escalabilidad
* Actividad: Agrupamiento jerárquico con SciPy e interpretación de dendrogramas


### Sesión 4: Modelos de mezclas gaussianas (GMM)
* Agrupamiento probabilístico y asignaciones suaves
* Algoritmo de esperanza-maximización (EM)
* Tipos de matriz de covarianza
* Selección de modelo con BIC y AIC
* Actividad: Comparación de GMM y k-medias en datos con grupos elípticos

### Sesión 5: Agrupamiento por densidad y espectral
* DBSCAN: puntos núcleo, frontera y ruido; parámetros $\varepsilon$ y ```min_samples```
* HDBSCAN y OPTICS
* Agrupamiento espectral: grafo de similitud y laplaciano
* Grupos no convexos y de densidad variable
* Actividad: Comparación de DBSCAN, HDBSCAN y agrupamiento espectral en formas no convexas


### Sesión 6: Validación e interpretación de agrupamientos
* Índices internos: silueta, Davies-Bouldin, Calinski-Harabasz
* Índices externos: ARI, información mutua normalizada
* Estabilidad de los agrupamientos (remuestreo)
* Perfilado de grupos y comunicación de resultados
* Actividad: Entrega del miniproyecto 1

## Unidad 2: Reducción de dimensionalidad 

### Sesión 7: Análisis de componentes principales (PCA)
* Varianza, covarianza y direcciones de máxima varianza
* Eigendescomposición de la matriz de covarianza
* Descomposición en valores singulares (SVD)
* PCA como minimización del error de reconstrucción
* Actividad: Implementación de PCA desde cero con NumPy

### Sesión 8: PCA en la práctica y PCA con kernel
* Varianza explicada, gráfico de sedimentación y elección de componentes
* Interpretación de cargas y biplots
* PCA con kernel para estructuras no lineales
* PCA incremental y aleatorizado para datos grandes
* Actividad: PCA con scikit-learn sobre imágenes de dígitos y Fashion-MNIST


### Sesión 9: Aprendizaje de variedades (*manifold learning*)
* Escalamiento multidimensional (MDS) e Isomap
* t-SNE: similitudes probabilísticas y perplejidad
* Riesgos al interpretar proyecciones no lineales
* Actividad: Comparación visual de PCA, MDS, Isomap y t-SNE sobre Fashion-MNIST

### Sesión 10: Modelos de variables latentes y autoencoders
* Análisis factorial y PCA probabilístico
* Análisis de componentes independientes (ICA)
* Autoencoders: codificador, decodificador y espacio latente
* Comparación de métodos lineales y no lineales
* Actividad: Entrega del miniproyecto 2

## Unidad 3: Detección de anomalías 

### Sesión 11: Enfoques estadísticos y basados en densidad
* Tipos de anomalías: puntuales, contextuales y colectivas
* Puntuación $z$, IQR y distancia de Mahalanobis
* Estimación de densidad con kernels y GMM
* Factor de valor atípico local (LOF)
* Actividad: planteamiento del miniproyecto 3: Detección de anomalías en conjuntos de ODDS.


### Sesión 12: Métodos basados en modelos y su evaluación (I)
* Bosque de aislamiento (*Isolation Forest*) 
* SVM de una clase (*One-Class SVM*)
* Actividad: Comparativa de detectores con PyOD en un conjunto de fraude con tarjetas


### Sesión 13: Métodos basados en modelos y su evaluación (II)
* Error de reconstrucción con PCA y autoencoders 
* Evaluación con pocas etiquetas: precisión@k, curva PR, ROC-AUC
* Actividad: Comparativa de detectores con PyOD en un conjunto de fraude con tarjetas

### Sesión 14: Flujo integrador y cierre del curso
* Diseño del flujo completo: preparación, reducción, agrupamiento y anomalías
* Selección e interpretación de métricas
* Impacto de los resultados en la toma de decisiones
* Ética y sesgos en el análisis no supervisado 
* Síntesis del curso y temas avanzados
* Actividad: Entrega del miniproyecto 3