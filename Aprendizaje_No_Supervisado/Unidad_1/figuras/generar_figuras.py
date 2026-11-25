"""Genera las figuras de la presentación de la Unidad 1 (Algoritmos de agrupamiento).

Uso: python3 generar_figuras.py
Requiere numpy, scipy, matplotlib y scikit-learn >= 1.3 (por HDBSCAN).
Las figuras se guardan en PDF junto a este script.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import DBSCAN, HDBSCAN, AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_samples, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(0)

MARINO, AZUL, NARANJA, VERDE, ROJO, GRIS = "#1F3864", "#2E75B6", "#E07B22", "#5B9A3C", "#C0392B", "#7F7F7F"
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


def colores(etiquetas):
    """Color por grupo; el ruido (-1) en gris claro."""
    c = PALETA[np.mod(etiquetas, len(PALETA))].astype(object)
    c[etiquetas == -1] = "#CCCCCC"
    return list(c)


def sin_ejes(ax):
    ax.set_xticks([]); ax.set_yticks([])


# ------------------------------------------------------------------
# S2: k-medias
# ------------------------------------------------------------------
def lloyd_iteraciones():
    X, _ = make_blobs(300, centers=3, cluster_std=1.0, random_state=7)
    C = np.array([[-2.0, 9.0], [-1.0, 8.5], [0.0, 9.5]])  # mala inicialización a propósito
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.2))
    paso = 0
    for ax in axes:
        d = ((X[:, None, :] - C[None]) ** 2).sum(-1)
        z = d.argmin(1)
        ax.scatter(X[:, 0], X[:, 1], c=colores(z), s=8)
        ax.scatter(C[:, 0], C[:, 1], marker="X", s=180, c="k", edgecolors="white", linewidths=1.5)
        J = d.min(1).sum()
        ax.set_title(f"Iteración {paso}  (J = {J:,.0f})".replace(",", " "))
        sin_ejes(ax)
        C = np.array([X[z == k].mean(0) for k in range(3)])
        paso += 1
    guardar(fig, "lloyd_iteraciones")


def inicializacion():
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
    ks = range(2, 11)
    inercia, sil = [], []
    for k in ks:
        km = KMeans(k, n_init=10, random_state=0).fit(X)
        inercia.append(km.inertia_)
        sil.append(silhouette_score(X, km.labels_))
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    axes[0].plot(list(ks), inercia, "o-", color=AZUL, lw=2)
    axes[0].axvline(4, ls="--", color=GRIS)
    axes[0].set_xlabel("k"); axes[0].set_ylabel("Inercia J"); axes[0].set_title("Método del codo")
    axes[1].plot(list(ks), sil, "o-", color=NARANJA, lw=2)
    axes[1].axvline(4, ls="--", color=GRIS)
    axes[1].set_xlabel("k"); axes[1].set_ylabel("Silueta promedio"); axes[1].set_title("Coeficiente de silueta")
    guardar(fig, "codo_silueta")


def limitaciones_kmeans():
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
    guardar(fig, "limitaciones_kmeans")


# ------------------------------------------------------------------
# S3: agrupamiento jerárquico
# ------------------------------------------------------------------
def dendrograma():
    X, _ = make_blobs(20, centers=3, cluster_std=0.9, random_state=4)
    Z = linkage(X, "ward")
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1, 1.5]})
    axes[0].scatter(X[:, 0], X[:, 1], color=MARINO, s=20)
    for i, (x, y) in enumerate(X):
        axes[0].text(x + 0.15, y + 0.1, str(i), fontsize=8, color=GRIS)
    axes[0].set_title("Datos"); sin_ejes(axes[0])
    dendrogram(Z, ax=axes[1], color_threshold=8, above_threshold_color=GRIS)
    axes[1].axhline(8, ls="--", color=ROJO)
    axes[1].text(axes[1].get_xlim()[1] * 0.98, 8.3, "corte: 3 grupos", color=ROJO, ha="right", fontsize=9)
    axes[1].set_title("Dendrograma (enlace de Ward)")
    axes[1].set_ylabel("Distancia de fusión")
    guardar(fig, "dendrograma")


def enlaces():
    Xm, _ = make_moons(300, noise=0.05, random_state=1)
    Xb, _ = make_blobs(300, centers=[[-1, -1], [1.5, 1.5]], cluster_std=[0.4, 0.9], random_state=3)
    Xb = np.r_[Xb, np.c_[np.linspace(-0.5, 1.0, 12), np.linspace(-0.5, 1.0, 12)]]  # puente
    fig, axes = plt.subplots(2, 4, figsize=(12, 5.6))
    for fila, X in enumerate([Xm, Xb]):
        for ax, enl in zip(axes[fila], ["single", "complete", "average", "ward"]):
            z = AgglomerativeClustering(2, linkage=enl).fit_predict(X)
            ax.scatter(X[:, 0], X[:, 1], c=colores(z), s=6)
            sin_ejes(ax)
            if fila == 0:
                ax.set_title({"single": "Simple", "complete": "Completo",
                              "average": "Promedio", "ward": "Ward"}[enl])
    guardar(fig, "enlaces")


# ------------------------------------------------------------------
# S4: mezclas gaussianas
# ------------------------------------------------------------------
def dibujar_elipses(ax, gmm):
    for k in range(gmm.n_components):
        cov = gmm.covariances_[k]
        vals, vecs = np.linalg.eigh(cov)
        ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
        for n in (1, 2):
            ax.add_patch(Ellipse(gmm.means_[k], 2 * n * np.sqrt(vals[1]), 2 * n * np.sqrt(vals[0]),
                                 angle=ang, fill=False, color=PALETA[k], lw=1.5, alpha=0.9 / n))


def gmm_vs_kmeans():
    # Tres grupos alargados y paralelos: k-medias los corta mal
    cov = np.array([[6.0, 0.0], [0.0, 0.12]])
    rng = np.random.default_rng(0)
    X = np.r_[rng.multivariate_normal([0, 0], cov, 200),
              rng.multivariate_normal([0, 1.6], cov, 200),
              rng.multivariate_normal([0, 3.2], cov, 200)]
    zk = KMeans(3, n_init=10, random_state=0).fit_predict(X)
    # La inicialización por defecto (k-medias) hereda el error; se inicializa desde los datos
    gmm = GaussianMixture(3, covariance_type="full", init_params="random_from_data",
                          n_init=10, random_state=0).fit(X)
    zg = gmm.predict(X)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].scatter(X[:, 0], X[:, 1], c=colores(zk), s=6); axes[0].set_title("k-medias")
    axes[1].scatter(X[:, 0], X[:, 1], c=colores(zg), s=6); axes[1].set_title("GMM (covarianza completa)")
    dibujar_elipses(axes[1], gmm)
    for a in axes:
        sin_ejes(a)
    guardar(fig, "gmm_vs_kmeans")


def asignacion_suave():
    X, _ = make_blobs(400, centers=[[0, 0], [2.5, 0]], cluster_std=0.9, random_state=2)
    gmm = GaussianMixture(2, random_state=0).fit(X)
    p = gmm.predict_proba(X)[:, 0]
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    sc = ax.scatter(X[:, 0], X[:, 1], c=p, cmap="coolwarm", s=10)
    cb = fig.colorbar(sc, ax=ax); cb.set_label(r"$\gamma_{i1}$")
    ax.set_title("Responsabilidades del componente 1"); sin_ejes(ax)
    guardar(fig, "asignacion_suave")


def gmm_bic():
    X, _ = make_blobs(600, centers=4, random_state=5)
    X = X @ np.array([[1.0, 0.6], [0.0, 0.7]])
    ks = range(1, 9)
    fig, ax = plt.subplots(figsize=(6, 3.4))
    for tipo, c in zip(["spherical", "diag", "tied", "full"], [GRIS, VERDE, NARANJA, AZUL]):
        bic = [GaussianMixture(k, covariance_type=tipo, random_state=0, n_init=3).fit(X).bic(X) for k in ks]
        ax.plot(list(ks), bic, "o-", color=c, label=tipo, ms=4)
    ax.set_xlabel("Número de componentes k"); ax.set_ylabel("BIC (menor es mejor)")
    ax.set_title("Selección de modelo con BIC"); ax.legend(title="covariance_type", fontsize=8)
    guardar(fig, "gmm_bic")


# ------------------------------------------------------------------
# S5: densidad y espectral
# ------------------------------------------------------------------
def dbscan_tipos():
    X, _ = make_moons(250, noise=0.08, random_state=3)
    X = np.r_[X, RNG.uniform([-1.2, -0.7], [2.2, 1.2], (25, 2))]
    db = DBSCAN(eps=0.15, min_samples=6).fit(X)
    nucleo = np.zeros(len(X), bool); nucleo[db.core_sample_indices_] = True
    ruido = db.labels_ == -1
    frontera = ~nucleo & ~ruido
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.scatter(*X[nucleo].T, c=colores(db.labels_[nucleo]), s=14, label="Núcleo")
    ax.scatter(*X[frontera].T, facecolors="none", edgecolors=list(colores(db.labels_[frontera])),
               s=30, linewidths=1.3, label="Frontera")
    ax.scatter(*X[ruido].T, c="k", marker="x", s=20, label="Ruido")
    ax.set_title(r"DBSCAN ($\varepsilon$ = 0.15, min_samples = 6)"); sin_ejes(ax)
    ax.legend(fontsize=8, loc="lower left")
    guardar(fig, "dbscan_tipos")


def k_distancia():
    X, _ = make_moons(400, noise=0.07, random_state=3)
    X = np.r_[X, RNG.uniform([-1.2, -0.7], [2.2, 1.2], (30, 2))]
    k = 6
    d, _ = NearestNeighbors(n_neighbors=k).fit(X).kneighbors(X)
    dk = np.sort(d[:, -1])
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(dk, color=AZUL, lw=2)
    ax.axhline(0.13, ls="--", color=ROJO)
    ax.text(15, 0.15, r"codo: $\varepsilon \approx 0.13$", color=ROJO)
    ax.set_xlabel("Puntos ordenados"); ax.set_ylabel(f"Distancia al {k}.º vecino")
    ax.set_title("Gráfico de k-distancia")
    guardar(fig, "k_distancia")


def comparacion_densidad():
    n = 500
    X1, _ = make_moons(n, noise=0.06, random_state=0)
    X2, _ = make_circles(n, factor=0.45, noise=0.05, random_state=0)
    X3, _ = make_blobs(n, centers=[[0, 0], [4, 0], [2, 3]], cluster_std=[0.25, 0.9, 0.5], random_state=8)
    X3 = np.r_[X3, RNG.uniform([-2, -3], [6.5, 5], (40, 2))]
    datos = [(X1, 2), (X2, 2), (X3, 3)]
    nombres = ["k-medias", "DBSCAN", "HDBSCAN", "Espectral"]
    fig, axes = plt.subplots(3, 4, figsize=(11, 7.6))
    for i, (X, k) in enumerate(datos):
        Xs = StandardScaler().fit_transform(X)
        modelos = [KMeans(k, n_init=10, random_state=0),
                   DBSCAN(eps=0.25, min_samples=8),
                   HDBSCAN(min_cluster_size=20),
                   SpectralClustering(k, affinity="nearest_neighbors", n_neighbors=10, random_state=0)]
        for j, m in enumerate(modelos):
            z = m.fit_predict(Xs)
            ax = axes[i, j]
            ax.scatter(Xs[:, 0], Xs[:, 1], c=colores(z), s=4)
            sin_ejes(ax)
            if i == 0:
                ax.set_title(nombres[j])
    guardar(fig, "comparacion_densidad")


def espectral_eigen():
    X, _ = make_circles(300, factor=0.4, noise=0.04, random_state=1)
    from sklearn.neighbors import kneighbors_graph
    W = kneighbors_graph(X, 10, include_self=False)
    W = 0.5 * (W + W.T).toarray()
    d = W.sum(1)
    Dm = np.diag(1 / np.sqrt(d))
    L = np.eye(len(X)) - Dm @ W @ Dm
    vals, vecs = np.linalg.eigh(L)
    U = vecs[:, :2]
    U = U / np.linalg.norm(U, axis=1, keepdims=True)
    z = KMeans(2, n_init=10, random_state=0).fit_predict(U)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
    axes[0].scatter(X[:, 0], X[:, 1], c=GRIS, s=6); axes[0].set_title("Datos"); sin_ejes(axes[0])
    axes[1].plot(vals[:10], "o-", color=AZUL); axes[1].set_title("10 eigenvalores menores de L")
    axes[1].set_xlabel("índice")
    axes[2].scatter(X[:, 0], X[:, 1], c=colores(z), s=6); axes[2].set_title("k-medias sobre eigenvectores")
    sin_ejes(axes[2])
    guardar(fig, "espectral_eigen")


# ------------------------------------------------------------------
# S6: validación
# ------------------------------------------------------------------
def diagrama_silueta():
    X, _ = make_blobs(500, centers=4, cluster_std=[1.0, 1.0, 1.6, 0.6], random_state=1)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
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


def indices_internos():
    X, _ = make_blobs(600, centers=4, cluster_std=1.0, random_state=3)
    ks = list(range(2, 10))
    sil, db, ch = [], [], []
    for k in ks:
        z = KMeans(k, n_init=10, random_state=0).fit_predict(X)
        sil.append(silhouette_score(X, z)); db.append(davies_bouldin_score(X, z)); ch.append(calinski_harabasz_score(X, z))
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    fig.subplots_adjust(wspace=0.3)
    for ax, v, t, c in zip(axes, [sil, db, ch],
                           ["Silueta (↑)", "Davies-Bouldin (↓)", "Calinski-Harabasz (↑)"],
                           [AZUL, NARANJA, VERDE]):
        ax.plot(ks, v, "o-", color=c, lw=2); ax.axvline(4, ls="--", color=GRIS)
        ax.set_title(t); ax.set_xlabel("k")
    guardar(fig, "indices_internos")


if __name__ == "__main__":
    lloyd_iteraciones(); inicializacion(); codo_silueta(); limitaciones_kmeans()
    dendrograma(); enlaces()
    gmm_vs_kmeans(); asignacion_suave(); gmm_bic()
    dbscan_tipos(); k_distancia(); comparacion_densidad(); espectral_eigen()
    diagrama_silueta(); indices_internos()
