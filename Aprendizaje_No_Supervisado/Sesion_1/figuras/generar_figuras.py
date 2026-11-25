"""Genera las figuras de la presentación de la Sesión 1 (Introducción).

Uso: python3 generar_figuras.py   (requiere numpy, matplotlib y scikit-learn)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(1)
MARINO, AZUL, NARANJA, VERDE, GRIS = "#1F3864", "#2E75B6", "#E07B22", "#5B9A3C", "#7F7F7F"
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


def supervisado_vs_no():
    X, y = make_blobs(300, centers=3, cluster_std=1.1, random_state=4)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    cols = np.array([AZUL, NARANJA, VERDE])
    axes[0].scatter(X[:, 0], X[:, 1], c=cols[y], s=12)
    axes[0].set_title("Supervisado: datos $(x_i, y_i)$")
    axes[1].scatter(X[:, 0], X[:, 1], c=GRIS, s=12)
    axes[1].set_title("No supervisado: sólo $x_i$")
    for a in axes:
        a.set_xticks([]); a.set_yticks([])
    guardar(fig, "supervisado_vs_no")


def efecto_escala():
    # Dos grupos que se distinguen por la edad, pero el ingreso tiene escala enorme
    n = 150
    edad = np.r_[RNG.normal(25, 3, n), RNG.normal(55, 3, n)]
    ingreso = RNG.normal(30000, 9000, 2 * n)
    X = np.c_[edad, ingreso]
    verdad = np.r_[np.zeros(n), np.ones(n)].astype(int)
    km_crudo = KMeans(2, n_init=10, random_state=0).fit_predict(X)
    Xs = StandardScaler().fit_transform(X)
    km_esc = KMeans(2, n_init=10, random_state=0).fit_predict(Xs)
    cols = np.array([AZUL, NARANJA])
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].scatter(X[:, 0], X[:, 1], c=cols[km_crudo], s=10)
    axes[0].set_title("k-medias sin escalar")
    axes[0].set_xlabel("Edad (años)"); axes[0].set_ylabel("Ingreso ($)")
    axes[1].scatter(Xs[:, 0], Xs[:, 1], c=cols[km_esc], s=10)
    axes[1].set_title("k-medias con estandarización")
    axes[1].set_xlabel("Edad (z)"); axes[1].set_ylabel("Ingreso (z)")
    guardar(fig, "efecto_escala")


def escaladores():
    x = np.r_[RNG.normal(50, 10, 200), [150, 170, 200]]  # con atípicos
    datos = [("Original", x),
             ("StandardScaler", StandardScaler().fit_transform(x[:, None]).ravel()),
             ("MinMaxScaler", MinMaxScaler().fit_transform(x[:, None]).ravel()),
             ("RobustScaler", RobustScaler().fit_transform(x[:, None]).ravel())]
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.8))
    for a, (t, v) in zip(axes, datos):
        a.hist(v, bins=30, color=AZUL)
        a.hist(v[-3:], bins=30, range=(v.min(), v.max()), color=NARANJA)
        a.set_title(t); a.set_yticks([])
    guardar(fig, "escaladores")


def mahalanobis():
    cov = np.array([[4.0, 3.0], [3.0, 4.0]])
    X = RNG.multivariate_normal([0, 0], cov, 400)
    A, B = np.array([2.2, 2.2]), np.array([2.2, -2.2])
    Si = np.linalg.inv(cov)
    dm = lambda p: np.sqrt(p @ Si @ p)
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.scatter(X[:, 0], X[:, 1], s=8, color=GRIS, alpha=0.5)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(3.1 * np.cos(t), 3.1 * np.sin(t), "--", color=AZUL, label="Euclidiana constante")
    L = np.linalg.cholesky(cov)
    for r in [1, 2, 3]:
        e = (L @ np.vstack([np.cos(t), np.sin(t)])) * r
        ax.plot(e[0], e[1], color=NARANJA, lw=1.2, label="Mahalanobis constante" if r == 1 else None)
    for p, nom in [(A, "A"), (B, "B")]:
        ax.scatter(*p, s=60, color=MARINO, zorder=5)
        ax.text(p[0] + 0.3, p[1], f"{nom}: $d_E$={np.linalg.norm(p):.1f}, $d_M$={dm(p):.1f}",
                color=MARINO, fontsize=9)
    ax.set_aspect("equal"); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Euclidiana vs. Mahalanobis")
    guardar(fig, "mahalanobis")


def maldicion():
    dims = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    r = []
    for d in dims:
        X = RNG.uniform(size=(500, d)); q = RNG.uniform(size=d)
        dist = np.linalg.norm(X - q, axis=1)
        r.append((dist.max() - dist.min()) / dist.min())
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.3))
    axes[0].loglog(dims, r, "o-", color=AZUL, lw=2)
    axes[0].set_xlabel("Dimensión $d$"); axes[0].set_ylabel(r"$(d_{\max}-d_{\min})/d_{\min}$")
    axes[0].set_title("Concentración de distancias"); axes[0].grid(alpha=0.3, which="both")
    d = np.arange(1, 51)
    axes[1].plot(d, 1 - 0.9 ** d, color=NARANJA, lw=2)
    axes[1].set_xlabel("Dimensión $d$"); axes[1].set_ylabel("Fracción del volumen")
    axes[1].set_title("Volumen en la cáscara exterior (10 %)")
    guardar(fig, "maldicion")


if __name__ == "__main__":
    supervisado_vs_no(); efecto_escala(); escaladores(); mahalanobis(); maldicion()
