"""Genera las figuras de la presentación de la Sesión 3 (agrupamiento jerárquico).

Uso: python3 generar_figuras.py   (requiere numpy, scipy, matplotlib y scikit-learn)
Las figuras se guardan en PDF junto a este script.
"""
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage, set_link_color_palette
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import load_iris, make_blobs, make_moons

OUT = Path(__file__).resolve().parent

MARINO, AZUL, NARANJA, VERDE, ROJO, GRIS = "#1F3864", "#2E75B6", "#E07B22", "#5B9A3C", "#C0392B", "#7F7F7F"
PALETA = np.array([AZUL, NARANJA, VERDE, "#8E44AD", ROJO, "#16A085"])
set_link_color_palette([AZUL, NARANJA, VERDE, "#8E44AD"])
COLOR_ESPECIE = np.array([VERDE, AZUL, ROJO])           # setosa, versicolor, virginica

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlecolor": MARINO,
    "savefig.bbox": "tight",
})


def guardar(fig, nombre):
    fig.savefig(OUT / f"{nombre}.pdf")
    plt.close(fig)
    print("ok", nombre)


def sin_ejes(ax):
    ax.set_xticks([]); ax.set_yticks([])


# ------------------------------------------------------------------
# Problema detonador
# ------------------------------------------------------------------
def iris_dendrograma():
    """Dendrograma de Ward de las 150 flores: estructura a dos escalas."""
    X = load_iris().data
    Z = linkage(X, "ward")
    fig, ax = plt.subplots(figsize=(8, 3.6))
    dendrogram(Z, ax=ax, no_labels=True, color_threshold=10, above_threshold_color=GRIS)
    for h, k, c in [(20, 2, ROJO), (9, 3, NARANJA)]:
        ax.axhline(h, ls="--", color=c, lw=1.2)
        ax.text(ax.get_xlim()[1] * 0.995, h + 0.6, f"corte: {k} grupos", color=c, ha="right", fontsize=9)
    ax.set_ylabel("Altura de fusión")
    ax.set_title("Iris: dendrograma (enlace de Ward)")
    guardar(fig, "iris_dendrograma")


# ------------------------------------------------------------------
# Ejemplo en una dimensión con tres enlaces
# ------------------------------------------------------------------
def ejemplo_1d():
    x = np.array([1, 2, 4, 7, 11.0]).reshape(-1, 1)
    etiquetas = [str(int(v)) for v in x.ravel()]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), sharey=True)
    for ax, m, t in zip(axes, ["single", "complete", "average"], ["Simple", "Completo", "Promedio"]):
        Z = linkage(x, m)
        dendrogram(Z, ax=ax, labels=etiquetas, color_threshold=0, above_threshold_color=MARINO)
        ax.set_title(f"Enlace {t.lower()}")
        for _, _, h, _ in Z:
            ax.axhline(h, color=GRIS, lw=0.4, ls=":")
    axes[0].set_ylabel("Altura de fusión")
    guardar(fig, "ejemplo_1d")


# ------------------------------------------------------------------
# Enlaces en formas difíciles
# ------------------------------------------------------------------
def enlaces():
    Xm, _ = make_moons(300, noise=0.05, random_state=1)
    Xb, _ = make_blobs(300, centers=[[-1, -1], [1.5, 1.5]], cluster_std=[0.4, 0.9], random_state=3)
    Xb = np.r_[Xb, np.c_[np.linspace(-0.5, 1.0, 12), np.linspace(-0.5, 1.0, 12)]]  # puente
    fig, axes = plt.subplots(2, 4, figsize=(12, 5.6))
    for fila, X in enumerate([Xm, Xb]):
        for ax, enl, t in zip(axes[fila], ["single", "complete", "average", "ward"],
                              ["Simple", "Completo", "Promedio", "Ward"]):
            z = AgglomerativeClustering(2, linkage=enl).fit_predict(X)
            ax.scatter(X[:, 0], X[:, 1], c=list(PALETA[z]), s=6)
            sin_ejes(ax)
            if fila == 0:
                ax.set_title(t)
    guardar(fig, "enlaces")


def arbol_minimo():
    """El enlace simple equivale a cortar las aristas más largas del árbol de expansión mínima."""
    rng = np.random.default_rng(2)
    X = np.r_[rng.normal([0, 0], 0.5, (18, 2)), rng.normal([3.5, 1.5], 0.5, (18, 2))]
    T = minimum_spanning_tree(squareform(pdist(X))).tocoo()
    larga = np.argmax(T.data)
    z = fcluster(linkage(X, "single"), 2, "maxclust") - 1
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    for e, (i, j) in enumerate(zip(T.row, T.col)):
        estilo = dict(color=ROJO, lw=2.2, ls="--") if e == larga else dict(color=GRIS, lw=1)
        ax.plot(*X[[i, j]].T, **estilo, zorder=1)
    ax.scatter(X[:, 0], X[:, 1], c=list(PALETA[z]), s=28, zorder=2)
    ax.set_title("Árbol de expansión mínima")
    ax.text(0.02, 0.02, "-- arista más larga: se corta", color=ROJO, transform=ax.transAxes, fontsize=9)
    sin_ejes(ax)
    guardar(fig, "arbol_minimo")


# ------------------------------------------------------------------
# Dendrograma y corte
# ------------------------------------------------------------------
def dendrograma_corte():
    X, _ = make_blobs(20, centers=3, cluster_std=0.9, random_state=4)
    Z = linkage(X, "ward")
    z = fcluster(Z, 3, "maxclust") - 1
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1, 1.5]})
    axes[0].scatter(X[:, 0], X[:, 1], c=list(PALETA[z]), s=26)
    for i, (a, b) in enumerate(X):
        axes[0].text(a + 0.15, b + 0.1, str(i), fontsize=8, color=GRIS)
    axes[0].set_title("Datos (20 puntos)"); sin_ejes(axes[0])
    corte = (Z[-3, 2] + Z[-2, 2]) / 2
    dendrogram(Z, ax=axes[1], color_threshold=corte, above_threshold_color=GRIS)
    axes[1].axhline(corte, ls="--", color=ROJO)
    axes[1].text(axes[1].get_xlim()[1] * 0.98, corte + 0.4, "corte: 3 grupos", color=ROJO, ha="right", fontsize=9)
    axes[1].set_title("Dendrograma (enlace de Ward)")
    axes[1].set_ylabel("Altura de fusión")
    guardar(fig, "dendrograma_corte")


def escalabilidad():
    """Tiempo medido de scipy.cluster.hierarchy.linkage (Ward) y memoria de la matriz de distancias."""
    ns = [1000, 2000, 4000, 8000, 12000]
    tiempos = []
    for n in ns:
        X = np.random.default_rng(0).normal(size=(n, 4))
        t0 = time.perf_counter(); linkage(X, "ward"); tiempos.append(time.perf_counter() - t0)
    n_mem = np.array([1e3, 1e4, 5e4, 1e5])
    memoria = n_mem * (n_mem - 1) / 2 * 8 / 1e9
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    axes[0].plot(ns, tiempos, "o-", color=AZUL, lw=2)
    axes[0].set_xlabel("n (puntos, d = 4)"); axes[0].set_ylabel("Segundos")
    axes[0].set_title("Tiempo de linkage (Ward)")
    axes[1].bar([f"{int(n):,}".replace(",", " ") for n in n_mem], memoria, color=NARANJA)
    for i, m in enumerate(memoria):
        axes[1].text(i, m, f"{m:.3g} GB", ha="center", va="bottom", fontsize=9)
    axes[1].set_xlabel("n (puntos)"); axes[1].set_ylabel("GB")
    axes[1].set_title("Memoria de las distancias")
    guardar(fig, "escalabilidad")


# ------------------------------------------------------------------
# Laboratorio con Iris
# ------------------------------------------------------------------
def iris_alturas():
    X = load_iris().data
    alturas = linkage(X, "ward")[::-1, 2][:10]
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(range(1, 11), alturas, "o-", color=AZUL, lw=2)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Número de grupos k (antes de la fusión)")
    ax.set_xticklabels([str(k) for k in range(2, 12)])
    ax.set_ylabel("Altura de la fusión")
    ax.set_title("Alturas de las últimas fusiones (Ward)")
    guardar(fig, "iris_alturas")


def iris_dendrograma_30():
    """Dendrograma de 30 flores, con la especie en cada hoja (sólo para interpretar)."""
    iris = load_iris()
    rng = np.random.default_rng(0)
    idx = np.sort(np.concatenate([rng.choice(np.where(iris.target == e)[0], 10, replace=False) for e in range(3)]))
    X, y = iris.data[idx], iris.target[idx]
    nombres = np.array(["set", "ver", "vir"])
    etiquetas = [f"{nombres[e]}{i}" for i, e in zip(idx, y)]
    Z = linkage(X, "ward")
    fig, ax = plt.subplots(figsize=(10, 3.6))
    dendrogram(Z, ax=ax, labels=etiquetas, leaf_font_size=8, color_threshold=Z[-3, 2] + 0.1,
               above_threshold_color=GRIS)
    for t in ax.get_xticklabels():
        t.set_color(COLOR_ESPECIE[list(nombres).index(t.get_text()[:3])])
    ax.set_ylabel("Altura de fusión")
    ax.set_title("30 flores de Iris (Ward); hojas coloreadas por especie")
    guardar(fig, "iris_dendrograma_30")


def iris_enlaces():
    """Los cuatro enlaces con k = 3, en el plano de los pétalos."""
    iris = load_iris()
    X, y = iris.data, iris.target
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.0), sharey=True)
    for ax, m, t in zip(axes, ["single", "complete", "average", "ward"], ["Simple", "Completo", "Promedio", "Ward"]):
        z = fcluster(linkage(X, m), 3, "maxclust") - 1
        # grupos ordenados por largo medio del pétalo: verde < azul < rojo (como las especies)
        orden = np.argsort([X[z == g, 2].mean() for g in range(3)])
        rango = np.empty(3, int); rango[orden] = np.arange(3)
        ax.scatter(X[:, 2], X[:, 3], c=list(COLOR_ESPECIE[rango[z]]), s=10)
        tam = sorted(np.bincount(z, minlength=3), reverse=True)
        ax.text(0.97, 0.04, "tamaños: " + ", ".join(map(str, tam)), transform=ax.transAxes,
                ha="right", fontsize=8, color=GRIS)
        ax.set_title(f"{t} (k = 3)")
        ax.set_xlabel("Largo del pétalo (cm)")
    axes[0].set_ylabel("Ancho del pétalo (cm)")
    guardar(fig, "iris_enlaces")


if __name__ == "__main__":
    iris_dendrograma(); ejemplo_1d(); enlaces(); arbol_minimo(); dendrograma_corte(); escalabilidad()
    iris_alturas(); iris_dendrograma_30(); iris_enlaces()
