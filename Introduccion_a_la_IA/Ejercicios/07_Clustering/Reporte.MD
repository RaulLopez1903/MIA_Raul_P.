# Reporte

**Asignatura:** Introducción a la inteligencia artificial  
**Alumno:** Raul Alejandro Perez Lopez  
**Tema:** Clustering  
**Ejercicio:** Separar los blobs y volver a elegir \(k\)  

---

## 1. Definición del problema

El presente ejercicio tiene como objetivo analizar el comportamiento del algoritmo **K-means** ante diferentes distribuciones de datos y estudiar cómo la separación de los grupos influye en la elección del número de clusters \(k\).

La notebook ``01 K-medias.ipynb`` genera inicialmente cinco blobs mediante `make_blobs`, utilizando los parámetros definidos originalmente en el ejercicio. Posteriormente, se aplica K-means con diferentes valores de \(k\), utilizando principalmente dos herramientas para determinar un número adecuado de clusters:

- **Método del codo**, mediante el análisis de la inercia.
- **Coeficiente de silueta**, como medida de qué tan bien separados se encuentran los clusters.

En la configuración original, aunque `make_blobs` genera cinco centros, algunos de ellos se encuentran muy próximos entre sí, provocando que ciertas nubes se mezclen. Por esta razón, el número de clusters sugerido por las métricas puede no coincidir con el número de centros utilizados para generar los datos.

En este ejercicio solo se cambiaron los centros y desviaciones estándar, por lo que los demás parámetros se mantienen en ambas ejecuciones.

```python
n_samples = 2000
random_state = 7
```

---

## 2. Ejecución base

Para la primera ejecución se utilizaron los parámetros originales.

```python
blob_centers = np.array(
    [[ 0.2,  2.3],
     [-1.5 ,  2.3],
     [-2.8,  1.8],
     [-2.8,  2.8],
     [-2.8,  1.3]])

blob_std = np.array([0.4, 0.3, 0.1, 0.1, 0.1])
```

Los datos simulados con estas especificaciones se muestran en el siguiente gráfico:

![Original Blobs Plot](./07_Images/02_blobs_plot.png)

En la distribución original se observan cinco centros, pero los dos grupos ubicados en la zona inferior izquierda y los dos grupos en la zona superior derecha presentan una separación reducida entre sí. Esto provoca que sus observaciones se encuentren relativamente próximas y exista cierto grado de solapamiento.

2.1 Diagrama de Voronoi con (k=5)


![Original Voronoi Plot](./07_Images/05_voronoi_plot.png)

El diagrama permite observar las regiones asignadas por K-means a cada centroide. Aunque se utilizan cinco clusters, la cercanía entre algunos grupos hace que las fronteras entre determinadas regiones no se reconozcan, mientras que en otras regiones se asignen fronteras por defecto.

Esto permite visualizar que establecer (k=5) no garantiza que los cinco clusters correspondan a grupos claramente separados en los datos.


2.2 Método del codo

El método del codo se utiliza para analizar la relación entre el número de clusters (k) y la inercia del modelo.

La inercia representa la suma de las distancias cuadráticas de las observaciones respecto al centroide de su cluster. Al incrementar (k), la inercia disminuye, por lo que el objetivo no es seleccionar simplemente el valor mínimo, sino identificar un punto a partir del cual las mejoras comienzan a ser menores.

![Original Inertia vs K Plot](./07_Images/03_inertia_vs_k_plot.png)

A partir de la gráfica se identifica el codo aproximadamente en:

\[
k = 4
\]

En este caso, el codo puede encontrarse en un valor diferente de cinco debido a que algunos de los blobs se encuentran suficientemente próximos como para que K-means pueda representar parte de su estructura mediante un mismo cluster sin generar un incremento considerable de la inercia.

2.3 Coeficiente de silueta

El coeficiente de silueta permite evaluar qué tan adecuadamente se encuentra cada observación dentro de su cluster considerando tanto la distancia respecto a su propio grupo como la distancia respecto a los demás grupos.

Valores cercanos a (1) indican una mayor separación entre clusters, mientras que valores cercanos a (0) indican observaciones próximas a las fronteras entre grupos.

![Original Shilhouette Plot](./07_Images/04_silhouette_score_vs_k.png)

El valor máximo del coeficiente de silueta se obtiene para:

\[
k = 4
\]

con un coeficiente de:

\[
S = 0.68
\]

El resultado indica que, de acuerdo con el coeficiente de silueta, la configuración con (k=4) presenta la mejor separación relativa entre los clusters evaluados. Lo que coincide con el método del codo.

---

## 3. Ejecución modificada

Después de analizar la configuración original, se modificaron los parámetros correspondientes a la ubicación de los centros y las desviaciones estándar.

El objetivo de esta modificación fue lograr que los cinco blobs presentaran una separación visual más clara, sin modificar el número de muestras ni los parámetros principales del algoritmo.

3.1 Nueva Configuración 

```python
blob_centers = np.array(
    [[ 0.2,  2.1],
     [-2.5 ,  2.7],
     [-1.6,  1.5],
     [-1.0,  2.8],
     [-2.8,  1.7]])
blob_std = np.array([0.2, 0.2, 0.1, 0.1, 0.1])
```

3.2. Distribución de los blobs separados

![Modified Blobs Plot](./07_Images/06_blobs_plot_modified.png)

Después de realizar la modificación, se observan grupos de datos claramente acumulados en nubes separadas, esto debido a que, a comparación de la configuración base, definimos esta nueva configuración exactamente para observar que sucede cuando los blobs son de este estilo.

3.3 Diagrama de Voronoi con (k=5)

![Modified Voronoi Plot](./07_Images/09_voronoi_plot_modified.png)

El diagrama muestra la distribución de las regiones correspondientes a los cinco centroides después de modificar los datos.
En este caso podemos observar una separación clara en los grupos de datos y sin solapamientos.

---

5.3 Método del codo después de la modificación

![Modified Inertia Plot](./07_Images/07_inertia_vs_k_plot_modified.png)

El codo se identifica aproximadamente en:

\[
k = 5
\]

Después de modificar la distribución de los datos, el comportamiento de la inercia presenta un codo muy claro con un aplanado después de k=5, mientras que la configuración base generó un codo en k=4 y además la inercia seguía con pequeñas reducciones después de dicho codo.

---

5.4 Coeficiente de silueta después de la modificación

![Modified Shilhouette Plot](./07_Images/08_silhouette_score_vs_k_modified.png)

El valor máximo del coeficiente de silueta se obtiene para:

\[
k = 5
\]

con un valor de:

\[
S = 0.9
\]


Al comparar este resultado con la configuración original

---

## 4. Conclusiones de resultados

A partir de los experimentos realizados, se puede concluir que:

[CONCLUSIÓN 1: EXPLICAR EL RESULTADO OBTENIDO CON LOS DATOS ORIGINALES.]

[CONCLUSIÓN 2: EXPLICAR POR QUÉ EL NÚMERO DE CENTROS UTILIZADOS PARA GENERAR LOS DATOS NO NECESARIAMENTE COINCIDE CON EL (k) SUGERIDO POR LAS MÉTRICAS.]

[CONCLUSIÓN 3: EXPLICAR QUÉ EFECTO TUVO LA SEPARACIÓN DE LOS CINCO BLOBS.]

[CONCLUSIÓN 4: INDICAR QUÉ OCURRIÓ CON EL CODO Y LA SILUETA DESPUÉS DE LA MODIFICACIÓN.]

[CONCLUSIÓN 5: EXPLICAR QUÉ SE OBSERVÓ SOBRE LA RELACIÓN ENTRE LA DISTANCIA ENTRE CENTROS, blob_std Y LA SEPARACIÓN DE LOS CLUSTERS.]

En términos generales, el experimento permitió observar que la selección de (k) mediante K-means depende de la estructura y distribución de los datos, y no únicamente del número de grupos con el que fueron generados originalmente.

---

5. Enlaces y evidencia de ejecución

GitHub

[PEGAR AQUÍ EL ENLACE AL REPOSITORIO O AL ARCHIVO .ipynb]

Google Colab

[PEGAR AQUÍ EL ENLACE DE COLAB]

Evidencia de ejecución

![Original Shilhouette Plot](./07_Images/10_entorno_de_ejecucion.png)
