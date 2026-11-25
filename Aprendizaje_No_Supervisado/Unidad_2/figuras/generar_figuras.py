"""Genera las figuras de la presentación de la Unidad 2 (Reducción de dimensionalidad).

Uso (desde cualquier carpeta):
    python3 generar_figuras.py

Las figuras se guardan en PDF junto a este script. Requiere numpy, matplotlib y
scikit-learn (todos los conjuntos de datos vienen incluidos en scikit-learn).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits, load_wine, make_circles, make_swiss_roll
from sklearn.decomposition import PCA, FastICA, KernelPCA
from sklearn.manifold import MDS, TSNE, Isomap
from sklearn.preprocessing import StandardScaler

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(0)

MARINO = "#1F3864"
AZUL = "#2E75B6"
NARANJA = "#E07B22"
GRIS = "#7F7F7F"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlecolor": MARINO,
    "savefig.bbox": "tight",
})


def guardar(fig, nombre):
    fig.savefig(OUT / f"{nombre}.pdf")
    plt.close(fig)
    print("ok", nombre)


# ------------------------------------------------------------------
# 1. Maldición de la dimensionalidad: concentración de distancias
# ------------------------------------------------------------------
def concentracion_distancias():
    dims = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    razones = []
    for d in dims:
        X = RNG.uniform(size=(500, d))
        q = RNG.uniform(size=d)
        dist = np.linalg.norm(X - q, axis=1)
        razones.append((dist.max() - dist.min()) / dist.min())
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.loglog(dims, razones, "o-", color=AZUL, lw=2)
    ax.set_xlabel("Dimensión $d$")
    ax.set_ylabel(r"$(d_{\max}-d_{\min})/d_{\min}$")
    ax.set_title("Contraste relativo de distancias")
    ax.grid(alpha=0.3, which="both")
    guardar(fig, "maldicion_dimensionalidad")


# ------------------------------------------------------------------
# 2. Idea geométrica de PCA
# ------------------------------------------------------------------
def pca_geometria():
    cov = np.array([[3.0, 1.6], [1.6, 1.2]])
    X = RNG.multivariate_normal([0, 0], cov, size=250)
    pca = PCA(2).fit(X)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))

    ax = axes[0]
    ax.scatter(X[:, 0], X[:, 1], s=10, color=GRIS, alpha=0.35)
    for comp, var, col, lab in zip(pca.components_, pca.explained_variance_,
                                   [NARANJA, AZUL], ["CP1", "CP2"]):
        v = comp * 2.5 * np.sqrt(var)
        ax.annotate("", xy=v, xytext=(0, 0), zorder=5,
                    arrowprops=dict(arrowstyle="-|>", lw=3, color=col))
        ax.text(*(v * 1.12), lab, color=col, fontweight="bold", ha="center")
    ax.set_aspect("equal")
    ax.set_title("Direcciones de máxima varianza")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")

    ax = axes[1]
    u = pca.components_[0]
    proy = np.outer(X @ u, u)
    idx = RNG.choice(len(X), 40, replace=False)
    for i in idx:
        ax.plot([X[i, 0], proy[i, 0]], [X[i, 1], proy[i, 1]], color=GRIS, lw=0.7)
    ax.scatter(X[idx, 0], X[idx, 1], s=14, color=GRIS)
    ax.scatter(proy[idx, 0], proy[idx, 1], s=14, color=NARANJA, zorder=3)
    t = np.linspace(-5, 5, 2)
    ax.plot(t * u[0], t * u[1], color=NARANJA, lw=2)
    ax.set_aspect("equal")
    ax.set_title("Proyección = mínimo error de reconstrucción")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    guardar(fig, "pca_geometria")


# ------------------------------------------------------------------
# 3. Varianza explicada y proyección de dígitos
# ------------------------------------------------------------------
def pca_digitos():
    digits = load_digits()
    X, y = digits.data, digits.target
    pca = PCA().fit(X)
    r = pca.explained_variance_ratio_
    acum = np.cumsum(r)

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    k = np.arange(1, 31)
    ax.bar(k, r[:30], color=AZUL, label="Individual")
    ax2 = ax.twinx()
    ax2.plot(k, acum[:30], "o-", color=NARANJA, ms=3, label="Acumulada")
    ax2.axhline(0.9, ls="--", color=GRIS, lw=1)
    k90 = int(np.searchsorted(acum, 0.9) + 1)
    ax2.annotate(f"90 % con k = {k90}", xy=(k90, 0.9), xytext=(k90 + 2, 0.62),
                 arrowprops=dict(arrowstyle="->", color=GRIS), color=MARINO)
    ax.set_xlabel("Número de componente")
    ax.set_ylabel("Proporción de varianza", color=AZUL)
    ax2.set_ylabel("Varianza acumulada", color=NARANJA)
    ax2.set_ylim(0, 1.02)
    ax2.spines["right"].set_visible(True)
    ax.set_title("Dígitos 8×8 (64 variables)")
    guardar(fig, "scree_digitos")

    Z = PCA(2).fit_transform(X)
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    sc = ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="tab10", s=6)
    ax.set_xlabel("CP1")
    ax.set_ylabel("CP2")
    ax.set_title("Dígitos proyectados en 2 componentes")
    cb = fig.colorbar(sc, ax=ax, ticks=range(10))
    cb.set_label("Dígito")
    guardar(fig, "digitos_pca2")

    # Reconstrucción con k componentes
    ks = [2, 5, 10, 20, 40]
    muestras = [0, 1, 2, 3, 4]
    fig, axes = plt.subplots(len(muestras), len(ks) + 1, figsize=(6.4, 5.6))
    for j, k in enumerate([64] + ks):
        p = PCA(k).fit(X)
        Xr = p.inverse_transform(p.transform(X[muestras]))
        for i in range(len(muestras)):
            a = axes[i, j]
            a.imshow(Xr[i].reshape(8, 8), cmap="gray_r")
            a.set_xticks([])
            a.set_yticks([])
            if i == 0:
                a.set_title("Original" if k == 64 else f"k = {k}", fontsize=10)
    fig.suptitle("Reconstrucción con k componentes", color=MARINO, fontweight="bold")
    guardar(fig, "reconstruccion_digitos")


# ------------------------------------------------------------------
# 4. Biplot (vinos)
# ------------------------------------------------------------------
def biplot_vinos():
    wine = load_wine()
    X = StandardScaler().fit_transform(wine.data)
    pca = PCA(2).fit(X)
    Z = pca.transform(X)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    colores = [AZUL, NARANJA, "#5B9A3C"]
    for c in range(3):
        ax.scatter(Z[wine.target == c, 0], Z[wine.target == c, 1], s=12,
                   color=colores[c], alpha=0.6, label=f"Cultivar {c}")
    escala = 6.0
    nombres = {"alcohol": "alcohol", "malic_acid": "ác. málico",
               "flavanoids": "flavonoides", "color_intensity": "int. color",
               "proline": "prolina", "hue": "tono", "total_phenols": "fenoles",
               "od280/od315_of_diluted_wines": "OD280/OD315"}
    for i, nom in enumerate(wine.feature_names):
        if nom not in nombres:
            continue
        v = pca.components_[:, i] * escala
        ax.annotate("", xy=v, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=MARINO, lw=1.3))
        ax.text(v[0] * 1.13, v[1] * 1.13, nombres[nom], fontsize=8.5,
                color=MARINO, ha="center")
    r = pca.explained_variance_ratio_
    ax.set_xlabel(f"CP1 ({r[0]:.0%})")
    ax.set_ylabel(f"CP2 ({r[1]:.0%})")
    ax.set_title("Biplot: observaciones y cargas")
    ax.legend(fontsize=8, loc="lower left")
    guardar(fig, "biplot_vinos")


# ------------------------------------------------------------------
# 5. PCA con kernel en círculos concéntricos
# ------------------------------------------------------------------
def kernel_pca():
    X, y = make_circles(n_samples=500, factor=0.35, noise=0.06, random_state=0)
    Zl = PCA(2).fit_transform(X)
    Zk = KernelPCA(2, kernel="rbf", gamma=4).fit_transform(X)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    for ax, Z, tit in zip(axes, [X, Zl, Zk],
                          ["Datos originales", "PCA lineal", "PCA con kernel RBF"]):
        ax.scatter(Z[y == 0, 0], Z[y == 0, 1], s=8, color=AZUL)
        ax.scatter(Z[y == 1, 0], Z[y == 1, 1], s=8, color=NARANJA)
        ax.set_title(tit)
        ax.set_xticks([])
        ax.set_yticks([])
    guardar(fig, "kernel_pca_circulos")


# ------------------------------------------------------------------
# 6. Rollo suizo: PCA vs Isomap
# ------------------------------------------------------------------
def rollo_suizo():
    X, t = make_swiss_roll(n_samples=1500, noise=0.05, random_state=0)
    fig = plt.figure(figsize=(10, 3.4))
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=t, cmap="viridis", s=4)
    ax.set_title("Rollo suizo en $\\mathbb{R}^3$")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.view_init(10, -70)
    for k, (mod, tit) in enumerate([(PCA(2), "PCA (lineal)"),
                                    (Isomap(n_neighbors=10, n_components=2), "Isomap (geodésico)")]):
        Z = mod.fit_transform(X)
        a = fig.add_subplot(1, 3, k + 2)
        a.scatter(Z[:, 0], Z[:, 1], c=t, cmap="viridis", s=4)
        a.set_title(tit)
        a.set_xticks([]); a.set_yticks([])
    guardar(fig, "rollo_suizo")


# ------------------------------------------------------------------
# 7. Comparación de métodos en dígitos y perplejidad de t-SNE
# ------------------------------------------------------------------
def manifold_digitos():
    digits = load_digits()
    idx = RNG.choice(len(digits.data), 800, replace=False)
    X, y = digits.data[idx], digits.target[idx]
    X = StandardScaler().fit_transform(X)
    metodos = [
        ("PCA", PCA(2)),
        ("MDS métrico", MDS(2, n_init=1, random_state=0, normalized_stress="auto")),
        ("Isomap", Isomap(n_neighbors=10, n_components=2)),
        ("t-SNE", TSNE(2, perplexity=30, init="pca", random_state=0)),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
    for ax, (nom, m) in zip(axes, metodos):
        Z = m.fit_transform(X)
        ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="tab10", s=5)
        ax.set_title(nom)
        ax.set_xticks([]); ax.set_yticks([])
    guardar(fig, "manifold_digitos")

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
    for ax, perp in zip(axes, [3, 30, 150]):
        Z = TSNE(2, perplexity=perp, init="pca", random_state=0).fit_transform(X)
        ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="tab10", s=5)
        ax.set_title(f"Perplejidad = {perp}")
        ax.set_xticks([]); ax.set_yticks([])
    guardar(fig, "tsne_perplejidad")


# ------------------------------------------------------------------
# 8. ICA: problema de la fiesta de cóctel
# ------------------------------------------------------------------
def ica_coctel():
    t = np.linspace(0, 8, 2000)
    S = np.c_[np.sin(2 * t), np.sign(np.sin(3 * t)), ((2 * t) % 2) - 1]
    S += 0.05 * RNG.normal(size=S.shape)
    S /= S.std(axis=0)
    A = np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])
    X = S @ A.T
    S_ica = FastICA(3, whiten="unit-variance", random_state=0).fit_transform(X)
    S_pca = PCA(3).fit_transform(X)
    paneles = [("Fuentes reales", S), ("Mezclas observadas", X),
               ("PCA", S_pca), ("ICA (FastICA)", S_ica)]
    colores = [AZUL, NARANJA, "#5B9A3C"]
    fig, axes = plt.subplots(4, 1, figsize=(7, 6.4), sharex=True)
    fig.subplots_adjust(hspace=0.45)
    for ax, (tit, M) in zip(axes, paneles):
        for j in range(3):
            m = M[:, j] / np.abs(M[:, j]).max()
            ax.plot(t, m + 2.4 * j, color=colores[j], lw=1)
        ax.set_title(tit, loc="left", fontsize=10)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
    axes[-1].set_xlabel("tiempo")
    guardar(fig, "ica_coctel")


if __name__ == "__main__":
    concentracion_distancias()
    pca_geometria()
    pca_digitos()
    biplot_vinos()
    kernel_pca()
    rollo_suizo()
    manifold_digitos()
    ica_coctel()
