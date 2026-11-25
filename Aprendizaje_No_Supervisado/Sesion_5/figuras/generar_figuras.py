"""Genera las figuras de la presentación de la Sesión 5 (agrupamiento por densidad y espectral).

Uso: python3 generar_figuras.py   (requiere numpy, scipy, matplotlib y scikit-learn >= 1.3)
Las figuras se guardan en PDF junto a este script; los números que se citan en las
láminas se imprimen en la consola.
"""
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csgraph
from sklearn.cluster import DBSCAN, HDBSCAN, OPTICS, KMeans, SpectralClustering
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.metrics import adjusted_rand_score
from sklearn.neighbors import NearestNeighbors, kneighbors_graph

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent

MARINO, AZUL, NARANJA, VERDE, ROJO, GRIS = "#1F3864", "#2E75B6", "#E07B22", "#5B9A3C", "#C0392B", "#7F7F7F"
PALETA = np.array([AZUL, NARANJA, VERDE, "#8E44AD", ROJO, "#16A085", "#B7950B", "#5D6D7E", "#D35400", "#1ABC9C"])
COLOR_RUIDO = "#BBBBBB"

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


def colores(z):
    """Color por grupo; el ruido (-1) en gris claro."""
    return [COLOR_RUIDO if g < 0 else PALETA[g % len(PALETA)] for g in z]


def dibujar(ax, X, z, titulo, s=6):
    ax.scatter(X[:, 0], X[:, 1], c=colores(z), s=s)
    ax.set_title(titulo, fontsize=11); sin_ejes(ax); ax.set_aspect("equal")


def n_grupos(z):
    return len(set(z)) - (1 if -1 in z else 0)


# ------------------------------------------------------------------
# Conjuntos de datos (los mismos del laboratorio)
# ------------------------------------------------------------------
def conjuntos():
    Xm, ym = make_moons(500, noise=0.07, random_state=0)
    Xc, yc = make_circles(500, factor=0.45, noise=0.05, random_state=0)
    Xb, yb = make_blobs([150, 150, 250], centers=[[0, 0], [1.3, 0], [4.5, 3]],
                        cluster_std=[0.2, 0.2, 1.0], random_state=0)
    ruido = np.random.default_rng(0).uniform([-2, -2], [8, 7], (50, 2))
    Xd, yd = np.r_[Xb, ruido], np.r_[yb, -np.ones(50, int)]      # el ruido tiene etiqueta -1
    return {"Lunas": (Xm, ym), "Círculos": (Xc, yc), "Densidades": (Xd, yd)}


# ------------------------------------------------------------------
# Problema detonador
# ------------------------------------------------------------------
def detonador():
    C = conjuntos()
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 5.4))
    for fila, nombre in enumerate(["Lunas", "Círculos"]):
        X, y = C[nombre]
        z_km = KMeans(2, n_init=10, random_state=0).fit_predict(X)
        z_db = DBSCAN(eps=0.2, min_samples=10).fit_predict(X)
        dibujar(axes[fila, 0], X, z_km, f"k-medias (ARI {round(adjusted_rand_score(y, z_km), 2) + 0.0:.2f})")
        dibujar(axes[fila, 1], X, z_db, f"DBSCAN (ARI {adjusted_rand_score(y, z_db):.2f})")
    guardar(fig, "detonador")


# ------------------------------------------------------------------
# DBSCAN
# ------------------------------------------------------------------
def dbscan_puntos():
    """Puntos núcleo, frontera y ruido en un ejemplo pequeño (eps = 1, min_samples = 4)."""
    X = np.array([[0, 0], [0.7, 0.3], [0.2, 0.8], [-0.5, 0.4], [0.9, 1.0], [1.5, 0.6],
                  [2.4, 0.9], [-0.6, -0.6], [3.6, 0.2], [3.3, 2.4]])
    eps, m = 1.0, 4
    db = DBSCAN(eps=eps, min_samples=m).fit(X)
    nucleo = np.zeros(len(X), bool); nucleo[db.core_sample_indices_] = True
    ruido = db.labels_ == -1
    frontera = ~nucleo & ~ruido
    print(f"ejemplo DBSCAN: {nucleo.sum()} núcleo, {frontera.sum()} frontera, {ruido.sum()} ruido")
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    for p in X[nucleo]:
        ax.add_patch(plt.Circle(p, eps, color=AZUL, alpha=0.08))
    for p in X[frontera | ruido]:
        ax.add_patch(plt.Circle(p, eps, fill=False, color=GRIS, ls=":", lw=0.8))
    ax.scatter(*X[nucleo].T, s=70, color=AZUL, label="núcleo", zorder=3)
    ax.scatter(*X[frontera].T, s=70, color=NARANJA, label="frontera", zorder=3)
    ax.scatter(*X[ruido].T, s=70, color="white", edgecolors=ROJO, lw=1.5, label="ruido", zorder=3)
    ax.set_aspect("equal"); sin_ejes(ax)
    ax.set_xlim(-1.8, 4.8); ax.set_ylim(-1.8, 3.5)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_title(f"$\\varepsilon = {eps:g}$, min_samples = {m}")
    guardar(fig, "dbscan_puntos")


def k_distancia():
    X, _ = conjuntos()["Lunas"]
    d = np.sort(NearestNeighbors(n_neighbors=10).fit(X).kneighbors(X)[0][:, -1])
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(d, color=AZUL, lw=2)
    ax.axhline(0.2, ls="--", color=NARANJA)
    ax.text(10, 0.21, "$\\varepsilon = 0.2$", color=NARANJA)
    ax.set_xlabel("Puntos ordenados"); ax.set_ylabel("Distancia al 10.º vecino")
    ax.set_title("Gráfica de k-distancia (lunas)")
    guardar(fig, "k_distancia")


def dbscan_eps():
    X, y = conjuntos()["Lunas"]
    fig, axes = plt.subplots(1, 3, figsize=(10, 2.8))
    for ax, eps in zip(axes, [0.1, 0.2, 0.4]):
        z = DBSCAN(eps=eps, min_samples=10).fit_predict(X)
        print(f"lunas eps={eps}: {n_grupos(z)} grupos, {(z == -1).sum()} ruido")
        dibujar(ax, X, z, f"$\\varepsilon = {eps}$: {n_grupos(z)} grupos, {(z == -1).sum()} ruido")
    guardar(fig, "dbscan_eps")


# ------------------------------------------------------------------
# Densidad variable: DBSCAN, OPTICS y HDBSCAN
# ------------------------------------------------------------------
def densidad_variable():
    X, y = conjuntos()["Densidades"]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))
    for ax, eps in zip(axes[:2], [0.2, 0.6]):
        z = DBSCAN(eps=eps, min_samples=10).fit_predict(X)
        print(f"densidades DBSCAN eps={eps}: {n_grupos(z)} grupos, {(z == -1).sum()} ruido, ARI {adjusted_rand_score(y, z):.2f}")
        dibujar(ax, X, z, f"DBSCAN, $\\varepsilon={eps}$\n{n_grupos(z)} grupos, {(z == -1).sum()} de ruido", s=5)
    z = HDBSCAN(min_cluster_size=15).fit_predict(X)
    print(f"densidades HDBSCAN: {n_grupos(z)} grupos, {(z == -1).sum()} ruido, ARI {adjusted_rand_score(y, z):.2f}")
    dibujar(axes[2], X, z, f"HDBSCAN\n{n_grupos(z)} grupos, {(z == -1).sum()} de ruido", s=5)
    guardar(fig, "densidad_variable")


def optics_alcanzabilidad():
    X, y = conjuntos()["Densidades"]
    op = OPTICS(min_samples=10).fit(X)
    r = op.reachability_[op.ordering_]
    r[np.isinf(r)] = np.nan
    z = HDBSCAN(min_cluster_size=15).fit_predict(X)[op.ordering_]
    fig, ax = plt.subplots(figsize=(9, 2.9))
    ax.bar(np.arange(len(r)), r, width=1.0, color=colores(z))
    for h, c in [(0.2, NARANJA), (0.6, ROJO)]:
        ax.axhline(h, ls="--", color=c, lw=1.2)
        ax.text(len(r) * 1.005, h, f"$\\varepsilon={h}$", color=c, va="center", fontsize=9)
    ax.set_ylim(0, 1.5)
    ax.set_xlabel("Puntos en el orden de OPTICS"); ax.set_ylabel("Distancia de alcanzabilidad")
    ax.set_title("Gráfica de alcanzabilidad (colores: grupos de HDBSCAN)")
    guardar(fig, "optics_alcanzabilidad")


# ------------------------------------------------------------------
# Agrupamiento espectral
# ------------------------------------------------------------------
def espectral():
    X, y = conjuntos()["Círculos"]
    W = kneighbors_graph(X, 10, include_self=False)
    W = 0.5 * (W + W.T)                                   # grafo simétrico de 10 vecinos
    L = csgraph.laplacian(W, normed=True).toarray()
    val, vec = np.linalg.eigh(L)
    n_comp, _ = csgraph.connected_components(W)
    print("espectral: componentes conexas del grafo =", n_comp, "| primeros valores propios:", val[:5].round(4))
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.4), gridspec_kw={"width_ratios": [1, 1, 1.1]})
    Wc = W.tocoo()
    for i, j in zip(Wc.row, Wc.col):
        if i < j:
            axes[0].plot(*X[[i, j]].T, color=GRIS, lw=0.3, zorder=1)
    axes[0].scatter(X[:, 0], X[:, 1], c=list(PALETA[y]), s=5, zorder=2)
    axes[0].set_title("Grafo de 10 vecinos"); sin_ejes(axes[0]); axes[0].set_aspect("equal")
    rng = np.random.default_rng(0)
    U = vec[:, :2]
    axes[1].scatter(U[:, 0], U[:, 1] + rng.normal(0, 0.002, len(U)), c=list(PALETA[y]), s=6)
    axes[1].set_xlabel("vector propio 1"); axes[1].set_ylabel("vector propio 2")
    axes[1].set_title("Representación espectral"); axes[1].set_xticks([]); axes[1].set_yticks([])
    axes[2].plot(range(1, 11), val[:10], "o-", color=AZUL, lw=2)
    axes[2].set_xlabel("índice"); axes[2].set_ylabel("valor propio de $L_{sym}$")
    axes[2].set_title("Espectro: brecha después de 2"); axes[2].set_xticks(range(1, 11))
    guardar(fig, "espectral")


# ------------------------------------------------------------------
# Laboratorio
# ------------------------------------------------------------------
def lab_datos():
    C = conjuntos()
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.0))
    for ax, (nombre, (X, y)) in zip(axes, C.items()):
        dibujar(ax, X, y, f"{nombre} ({len(X)} puntos)", s=5)
    guardar(fig, "lab_datos")


def lab_k_distancia():
    C = conjuntos()
    fig, axes = plt.subplots(1, 3, figsize=(11, 2.8))
    for ax, (nombre, (X, _)) in zip(axes, C.items()):
        d = np.sort(NearestNeighbors(n_neighbors=10).fit(X).kneighbors(X)[0][:, -1])
        ax.plot(d, color=AZUL, lw=2); ax.set_title(nombre, fontsize=11)
        ax.axhline(0.2, ls="--", color=NARANJA, lw=1)
        ax.set_xlabel("Puntos ordenados")
        if nombre == "Densidades":
            ax.set_ylim(0, 2)
    axes[0].set_ylabel("Distancia al 10.º vecino")
    guardar(fig, "lab_k_distancia")


def lab_barrido():
    X, y = conjuntos()["Densidades"]
    epsilons = np.round(np.arange(0.1, 1.01, 0.05), 2)
    ari = [adjusted_rand_score(y, DBSCAN(eps=e, min_samples=10).fit_predict(X)) for e in epsilons]
    z_h = HDBSCAN(min_cluster_size=15).fit_predict(X)
    a_h = adjusted_rand_score(y, z_h)
    print("barrido DBSCAN densidades: mejor ARI", round(max(ari), 2), "en eps =", epsilons[int(np.argmax(ari))],
          "| HDBSCAN", round(a_h, 2))
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    ax.plot(epsilons, ari, "o-", color=AZUL, lw=2, ms=4, label="DBSCAN")
    ax.axhline(a_h, ls="--", color=VERDE, lw=1.8, label="HDBSCAN")
    ax.set_xlabel("$\\varepsilon$"); ax.set_ylabel("ARI"); ax.set_ylim(0, 1)
    ax.legend(frameon=False, loc="lower right"); ax.set_title("Densidades: ningún $\\varepsilon$ basta")
    guardar(fig, "lab_barrido")


def lab_comparacion():
    C = conjuntos()
    fig, axes = plt.subplots(3, 4, figsize=(11, 8.2))
    for fila, (nombre, (X, y)) in enumerate(C.items()):
        k = n_grupos(y)
        modelos = [("k-medias", KMeans(k, n_init=10, random_state=0)),
                   ("DBSCAN", DBSCAN(eps=0.2, min_samples=10)),
                   ("HDBSCAN", HDBSCAN(min_cluster_size=15)),
                   ("Espectral", SpectralClustering(k, affinity="nearest_neighbors", n_neighbors=10,
                                                    random_state=0))]
        for col, (t, mod) in enumerate(modelos):
            z = mod.fit_predict(X)
            a = round(adjusted_rand_score(y, z), 2) + 0.0     # evita "-0.00"
            print(f"{nombre:10s} {t:10s} ARI {a:.2f}  grupos {n_grupos(z)}  ruido {(z == -1).sum()}")
            dibujar(axes[fila, col], X, z, f"{t}: ARI {a:.2f}", s=4)
        axes[fila, 0].set_ylabel(nombre, fontsize=12, color=MARINO)
    guardar(fig, "lab_comparacion")


if __name__ == "__main__":
    detonador(); dbscan_puntos(); k_distancia(); dbscan_eps(); densidad_variable(); optics_alcanzabilidad()
    espectral(); lab_datos(); lab_k_distancia(); lab_barrido(); lab_comparacion()
