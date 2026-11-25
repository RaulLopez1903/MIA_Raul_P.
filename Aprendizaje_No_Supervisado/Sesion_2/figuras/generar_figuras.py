"""Genera las figuras de la presentación de la Sesión 2 (k-medias).

Uso: python3 generar_figuras.py   (requiere numpy, matplotlib y scikit-learn)
Las figuras se guardan en PDF junto a este script.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris, make_blobs, make_moons
from sklearn.metrics import silhouette_samples, silhouette_score

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(0)

MARINO, AZUL, NARANJA, VERDE, ROJO, GRIS = "#1F3864", "#2E75B6", "#E07B22", "#5B9A3C", "#C0392B", "#7F7F7F"
NOMBRES_IRIS = ["Largo del sépalo (cm)", "Ancho del sépalo (cm)",
                "Largo del pétalo (cm)", "Ancho del pétalo (cm)"]
PALETA = np.array([AZUL, NARANJA, VERDE, "#8E44AD", ROJO, "#16A085", "#D4AC0D", "#34495E"])

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


def colores(z):
    return list(PALETA[np.mod(z, len(PALETA))])


def sin_ejes(ax):
    ax.set_xticks([]); ax.set_yticks([])


def lloyd_iteraciones():
    """Cuatro iteraciones de Lloyd desde una mala inicialización."""
    X, _ = make_blobs(300, centers=3, cluster_std=1.0, random_state=7)
    C = np.array([[-2.0, 9.0], [-1.0, 8.5], [0.0, 9.5]])
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
    for paso, ax in enumerate(axes):
        d = ((X[:, None, :] - C[None]) ** 2).sum(-1)
        z = d.argmin(1)
        ax.scatter(X[:, 0], X[:, 1], c=colores(z), s=8)
        ax.scatter(C[:, 0], C[:, 1], marker="X", s=180, c="k", edgecolors="white", linewidths=1.5)
        ax.set_title(f"Iteración {paso}  (J = {d.min(1).sum():.0f})")
        sin_ejes(ax)
        C = np.array([X[z == k].mean(0) for k in range(3)])
    guardar(fig, "lloyd_iteraciones")


def voronoi():
    """Regiones de asignación: celdas de Voronoi de los centros."""
    X, _ = make_blobs(300, centers=4, cluster_std=1.0, random_state=3)
    km = KMeans(4, n_init=10, random_state=0).fit(X)
    x0, x1 = X[:, 0].min() - 1, X[:, 0].max() + 1
    y0, y1 = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x0, x1, 400), np.linspace(y0, y1, 400))
    zz = km.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(5, 4))
    from matplotlib.colors import ListedColormap
    ax.contourf(xx, yy, zz, levels=np.arange(-0.5, 4), cmap=ListedColormap(PALETA[:4]), alpha=0.15)
    ax.contour(xx, yy, zz, levels=np.arange(0.5, 3), colors=GRIS, linewidths=1)
    ax.scatter(X[:, 0], X[:, 1], c=colores(km.labels_), s=8)
    C = km.cluster_centers_
    ax.scatter(C[:, 0], C[:, 1], marker="X", s=180, c="k", edgecolors="white", linewidths=1.5)
    ax.set_title("Regiones de asignación (Voronoi)")
    sin_ejes(ax)
    guardar(fig, "voronoi")


def inicializacion():
    """Inercia final con inicialización aleatoria vs. k-means++."""
    X, _ = make_blobs(1000, centers=8, cluster_std=0.7, random_state=3)
    rnd = [KMeans(8, init="random", n_init=1, random_state=s).fit(X).inertia_ for s in range(200)]
    pp = [KMeans(8, init="k-means++", n_init=1, random_state=s).fit(X).inertia_ for s in range(200)]
    fig, ax = plt.subplots(figsize=(6, 3.3))
    bins = np.linspace(min(rnd + pp), max(rnd + pp), 40)
    ax.hist(rnd, bins=bins, color=NARANJA, alpha=0.7, label="Aleatoria")
    ax.hist(pp, bins=bins, color=AZUL, alpha=0.7, label="k-means++")
    ax.set_xlabel("Inercia final J (menor es mejor)")
    ax.set_ylabel("Ejecuciones")
    ax.set_title("200 ejecuciones con una sola inicialización")
    ax.legend()
    guardar(fig, "inicializacion")


def codo_silueta():
    X, _ = make_blobs(600, centers=4, cluster_std=1.0, random_state=3)
    ks = list(range(2, 11))
    inercia, sil = [], []
    for k in ks:
        km = KMeans(k, n_init=10, random_state=0).fit(X)
        inercia.append(km.inertia_)
        sil.append(silhouette_score(X, km.labels_))
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    axes[0].plot(ks, inercia, "o-", color=AZUL, lw=2)
    axes[0].axvline(4, ls="--", color=GRIS)
    axes[0].set_xlabel("k"); axes[0].set_ylabel("Inercia J"); axes[0].set_title("Método del codo")
    axes[1].plot(ks, sil, "o-", color=NARANJA, lw=2)
    axes[1].axvline(4, ls="--", color=GRIS)
    axes[1].set_xlabel("k"); axes[1].set_ylabel("Silueta promedio"); axes[1].set_title("Coeficiente de silueta")
    guardar(fig, "codo_silueta")


def diagrama_silueta():
    X, _ = make_blobs(500, centers=4, cluster_std=[1.0, 1.0, 1.6, 0.6], random_state=1)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4))
    for ax, k in zip(axes, [3, 4]):
        z = KMeans(k, n_init=10, random_state=0).fit_predict(X)
        s = silhouette_samples(X, z)
        y0 = 0
        for c in range(k):
            sc = np.sort(s[z == c])
            ax.fill_betweenx(np.arange(y0, y0 + len(sc)), 0, sc, color=PALETA[c], alpha=0.8)
            y0 += len(sc) + 10
        ax.axvline(s.mean(), ls="--", color=ROJO)
        ax.set_title(f"k = {k}: silueta promedio = {s.mean():.2f}")
        ax.set_xlabel("s(i)"); ax.set_yticks([])
    guardar(fig, "diagrama_silueta")


def limitaciones():
    Xa, _ = make_blobs(450, centers=3, random_state=170)
    Xa = Xa @ np.array([[0.6, -0.64], [-0.4, 0.85]])
    Xb, _ = make_blobs(450, centers=3, cluster_std=[1.0, 2.5, 0.4], random_state=170)
    Xc, _ = make_moons(400, noise=0.06, random_state=0)
    Xd = np.r_[RNG.normal(0, 1, (300, 2)), RNG.normal([6, 0], 0.5, (30, 2))]
    casos = [(Xa, 3, "Grupos anisotrópicos"), (Xb, 3, "Varianzas distintas"),
             (Xc, 2, "Formas no convexas"), (Xd, 2, "Tamaños muy distintos")]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.1))
    for ax, (X, k, t) in zip(axes, casos):
        z = KMeans(k, n_init=10, random_state=0).fit_predict(X)
        ax.scatter(X[:, 0], X[:, 1], c=colores(z), s=6)
        ax.set_title(t); sin_ejes(ax)
    guardar(fig, "limitaciones")


def atipicos():
    """Un pequeño grupo de atípicos se lleva un centro completo."""
    rng = np.random.default_rng(4)
    X = np.r_[rng.normal([0, 0], 0.6, (150, 2)), rng.normal([4, 0], 0.6, (150, 2)),
              rng.normal([2, 3.5], 0.6, (150, 2))]
    Xo = np.r_[X, rng.normal([20, 15], 0.4, (6, 2))]
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, D, t in zip(axes, [X, Xo], ["Sin atípicos", "Con 6 atípicos (1 %)"]):
        km = KMeans(3, n_init=10, random_state=0).fit(D)
        ax.scatter(D[:, 0], D[:, 1], c=colores(km.labels_), s=8)
        C = km.cluster_centers_
        ax.scatter(C[:, 0], C[:, 1], marker="X", s=160, c="k", edgecolors="white", linewidths=1.5)
        ax.set_title(f"{t}, k = 3"); sin_ejes(ax)
    guardar(fig, "atipicos")


# ------------------------------------------------------------------
# Iris: problema detonador y laboratorio
# ------------------------------------------------------------------
def iris_detonador():
    """Las flores sin la etiqueta de especie: ¿cuántos tipos hay?"""
    iris = load_iris()
    X = iris.data
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, (i, j) in zip(axes, [(0, 1), (2, 3)]):
        ax.scatter(X[:, i], X[:, j], s=14, color=GRIS, alpha=0.7)
        ax.set_xlabel(NOMBRES_IRIS[i]); ax.set_ylabel(NOMBRES_IRIS[j])
    axes[0].set_title("Sépalos"); axes[1].set_title("Pétalos")
    guardar(fig, "iris_detonador")


def iris_codo_silueta():
    X = load_iris().data
    ks = list(range(2, 9))
    inercia, sil = [], []
    for k in ks:
        km = KMeans(k, n_init=10, random_state=0).fit(X)
        inercia.append(km.inertia_)
        sil.append(silhouette_score(X, km.labels_))
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    axes[0].plot(ks, inercia, "o-", color=AZUL, lw=2)
    axes[0].set_xlabel("k"); axes[0].set_ylabel("Inercia J"); axes[0].set_title("Método del codo (Iris)")
    axes[1].plot(ks, sil, "o-", color=NARANJA, lw=2)
    axes[1].set_xlabel("k"); axes[1].set_ylabel("Silueta promedio"); axes[1].set_title("Silueta (Iris)")
    guardar(fig, "iris_codo_silueta")


def iris_resultado():
    """Grupos de k-medias (k = 3) frente a las especies reales, en el plano de los pétalos."""
    iris = load_iris()
    X, y = iris.data, iris.target
    km = KMeans(3, n_init=10, random_state=0).fit(X)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    # Color de cada grupo = color de la especie mayoritaria (solo para comparar)
    col_especie = np.array([VERDE, AZUL, ROJO])
    mayoritaria = np.array([np.bincount(y[km.labels_ == g], minlength=3).argmax() for g in range(3)])
    axes[0].scatter(X[:, 2], X[:, 3], c=list(col_especie[mayoritaria[km.labels_]]), s=14)
    C = km.cluster_centers_
    axes[0].scatter(C[:, 2], C[:, 3], marker="X", s=160, c="k", edgecolors="white", linewidths=1.5)
    axes[0].set_title("k-medias, k = 3 (sin etiquetas)")
    for e, c in zip(range(3), [VERDE, AZUL, ROJO]):
        axes[1].scatter(X[y == e, 2], X[y == e, 3], color=c, s=14, label=iris.target_names[e])
    axes[1].set_title("Especies reales"); axes[1].legend(fontsize=8, loc="upper left")
    for ax in axes:
        ax.set_xlabel(NOMBRES_IRIS[2]); ax.set_ylabel(NOMBRES_IRIS[3])
    guardar(fig, "iris_resultado")


if __name__ == "__main__":
    lloyd_iteraciones(); voronoi(); inicializacion(); codo_silueta()
    diagrama_silueta(); limitaciones(); atipicos()
    iris_detonador(); iris_codo_silueta(); iris_resultado()
