"""Genera las figuras de la presentación de la Sesión 4 (modelos de mezclas gaussianas).

Uso: python3 generar_figuras.py   (requiere numpy, scipy, matplotlib y scikit-learn)
Las figuras se guardan en PDF junto a este script; los números que se citan en las
láminas se imprimen en la consola.
"""
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
from scipy.stats import norm
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture

warnings.filterwarnings("ignore", category=ConvergenceWarning)
OUT = Path(__file__).resolve().parent

MARINO, AZUL, NARANJA, VERDE, ROJO, GRIS = "#1F3864", "#2E75B6", "#E07B22", "#5B9A3C", "#C0392B", "#7F7F7F"
PALETA = np.array([AZUL, NARANJA, VERDE, "#8E44AD", ROJO, "#16A085"])
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


def elipses(ax, medias, covs, color=MARINO):
    """Dibuja las elipses de 1 y 2 desviaciones estándar de cada componente."""
    for m, S in zip(medias, covs):
        val, vec = np.linalg.eigh(S)
        ang = np.degrees(np.arctan2(vec[1, 1], vec[0, 1]))
        for r in (1, 2):
            ax.add_patch(Ellipse(m, 2 * r * np.sqrt(val[1]), 2 * r * np.sqrt(val[0]), angle=ang,
                                 fill=False, color=color, lw=1.3 if r == 1 else 0.8, ls="-" if r == 1 else "--"))
        ax.plot(*m, "x", color=color, ms=8, mew=2)


def covarianzas_completas(g):
    """Convierte covariances_ de cualquier tipo a matrices completas (2 x 2)."""
    d = g.means_.shape[1]
    if g.covariance_type == "full":
        return g.covariances_
    if g.covariance_type == "tied":
        return np.repeat(g.covariances_[None], g.n_components, 0)
    if g.covariance_type == "diag":
        return np.array([np.diag(c) for c in g.covariances_])
    return np.array([c * np.eye(d) for c in g.covariances_])


# ------------------------------------------------------------------
# Datos sintéticos: tres grupos elípticos de forma, tamaño y orientación distintos
# ------------------------------------------------------------------
def rot(t, s1, s2):
    R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    return R @ np.diag([s1 ** 2, s2 ** 2]) @ R.T


def datos_elipticos():
    rng = np.random.default_rng(1)
    comps = [((0, 0), rot(np.pi / 5, 2.2, 0.35), 250),
             ((2.2, 3.0), rot(-np.pi / 6, 1.8, 0.3), 200),
             ((4.5, -0.5), rot(0, 0.5, 0.5), 150)]
    X = np.vstack([rng.multivariate_normal(m, S, n) for m, S, n in comps])
    y = np.repeat([0, 1, 2], [c[2] for c in comps])
    return X, y


def detonador():
    X, y = datos_elipticos()
    z_km = KMeans(3, n_init=10, random_state=0).fit_predict(X)
    g = GaussianMixture(3, n_init=5, random_state=0).fit(X)
    z_g = g.predict(X)
    a_km, a_g = adjusted_rand_score(y, z_km), adjusted_rand_score(y, z_g)
    print(f"detonador: ARI k-medias = {a_km:.2f}, ARI GMM = {a_g:.2f}")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)
    axes[0].scatter(X[:, 0], X[:, 1], c=list(PALETA[z_km]), s=7)
    km = KMeans(3, n_init=10, random_state=0).fit(X)
    axes[0].plot(*km.cluster_centers_.T, "x", color=MARINO, ms=9, mew=2.5)
    axes[0].set_title(f"k-medias (ARI = {a_km:.2f})")
    axes[1].scatter(X[:, 0], X[:, 1], c=list(PALETA[z_g]), s=7)
    elipses(axes[1], g.means_, g.covariances_)
    axes[1].set_title(f"Mezcla gaussiana (ARI = {a_g:.2f})")
    for ax in axes:
        sin_ejes(ax); ax.set_aspect("equal")
    guardar(fig, "detonador")


def gaussianas_2d():
    """Contornos de tres gaussianas: covarianza esférica, diagonal y completa."""
    casos = [("Esférica: $\\sigma^2 I$", np.eye(2)),
             ("Diagonal", np.diag([2.5, 0.4])),
             ("Completa", rot(np.pi / 4, 1.7, 0.5))]
    xx, yy = np.meshgrid(np.linspace(-4, 4, 200), np.linspace(-4, 4, 200))
    P = np.dstack([xx, yy])
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
    for ax, (t, S) in zip(axes, casos):
        Si = np.linalg.inv(S)
        dens = np.exp(-0.5 * np.einsum("...i,ij,...j", P, Si, P))
        ax.contourf(xx, yy, dens, levels=8, cmap="Blues")
        val, vec = np.linalg.eigh(S)
        for v, u in zip(val, vec.T):
            ax.annotate("", xy=np.sqrt(v) * u * 1.6, xytext=(0, 0),
                        arrowprops=dict(arrowstyle="->", color=NARANJA, lw=2))
        ax.set_title(t); ax.set_aspect("equal"); sin_ejes(ax)
    guardar(fig, "gaussianas_2d")


def asignacion_suave():
    """Mezcla en 1D: densidades ponderadas y responsabilidad del componente 1."""
    pi, mu, sd = np.array([0.5, 0.5]), np.array([0.0, 4.0]), np.array([1.0, 2.0])
    x = np.linspace(-4, 10, 500)
    p = pi[:, None] * norm.pdf(x[None], mu[:, None], sd[:, None])
    gamma = p[0] / p.sum(0)
    a, b = pi * norm.pdf(2, mu, sd)
    print(f"ejemplo 1D en x=2: {a:.4f}, {b:.4f}, gamma1 = {a / (a + b):.3f}")
    fig, axes = plt.subplots(2, 1, figsize=(7, 4.2), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
    axes[0].plot(x, p[0], color=AZUL, lw=2, label="$\\pi_1\\,\\mathcal{N}(x\\mid 0,1)$")
    axes[0].plot(x, p[1], color=NARANJA, lw=2, label="$\\pi_2\\,\\mathcal{N}(x\\mid 4,2^2)$")
    axes[0].plot(x, p.sum(0), color=MARINO, lw=1.2, ls="--", label="$p(x)$")
    axes[0].axvline(2, color=GRIS, lw=0.8, ls=":")
    axes[0].legend(fontsize=9, frameon=False); axes[0].set_ylabel("densidad")
    axes[1].plot(x, gamma, color=AZUL, lw=2)
    axes[1].plot(x, 1 - gamma, color=NARANJA, lw=2)
    axes[1].axvline(2, color=GRIS, lw=0.8, ls=":")
    axes[1].plot(2, a / (a + b), "o", color=AZUL)
    axes[1].text(2.2, a / (a + b), f"$\\gamma_1(2) = {a / (a + b):.2f}$", va="center", fontsize=9, color=AZUL)
    axes[1].set_ylabel("responsabilidad"); axes[1].set_xlabel("$x$")
    guardar(fig, "asignacion_suave")


SEMILLA_EM = 6          # inicialización que tarda en converger (89 iteraciones)


def em_iteraciones():
    """EM desde una inicialización aleatoria: estado tras algunas iteraciones."""
    X, _ = datos_elipticos()
    def ajuste(it):
        return GaussianMixture(3, max_iter=it, init_params="random_from_data", random_state=SEMILLA_EM,
                               tol=1e-10).fit(X)
    pasos = [1, 50, 80, 90]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.3), sharex=True, sharey=True)
    for ax, it in zip(axes, pasos):
        g = ajuste(it)
        R = g.predict_proba(X)
        colores = R @ np.array([matplotlib.colors.to_rgb(c) for c in PALETA[:3]])
        ax.scatter(X[:, 0], X[:, 1], c=np.clip(colores, 0, 1), s=5)
        elipses(ax, g.means_, g.covariances_)
        ax.set_title(f"iteración {it}"); sin_ejes(ax); ax.set_aspect("equal")
    guardar(fig, "em_iteraciones")
    its = np.arange(1, 101)
    ll = [ajuste(i).score(X) for i in its]
    print(f"EM: log-verosimilitud media {ll[0]:.3f} -> {ll[-1]:.3f}; monótona: {np.all(np.diff(ll) >= -1e-9)}")
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(its, ll, "-", color=AZUL, lw=2)
    ax.set_xlabel("Iteración"); ax.set_ylabel("log-verosimilitud media")
    ax.set_title("EM nunca disminuye la verosimilitud")
    guardar(fig, "em_verosimilitud")


def optimos_locales():
    """Dos inicializaciones de EM: un óptimo local y la mejor solución."""
    X, y = datos_elipticos()
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4), sharex=True, sharey=True)
    for ax, s in zip(axes, [5, SEMILLA_EM]):
        g = GaussianMixture(3, max_iter=500, tol=1e-6, init_params="random_from_data", random_state=s).fit(X)
        z = g.predict(X)
        ax.scatter(X[:, 0], X[:, 1], c=list(PALETA[z]), s=5)
        elipses(ax, g.means_, g.covariances_)
        print(f"óptimo semilla {s}: log-verosimilitud media {g.score(X):.3f}, ARI {adjusted_rand_score(y, z):.2f}")
        ax.set_title(f"log-verosimilitud media {g.score(X):.2f}", fontsize=11)
        sin_ejes(ax); ax.set_aspect("equal")
    guardar(fig, "optimos_locales")


def tipos_covarianza():
    X, y = datos_elipticos()
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.3), sharex=True, sharey=True)
    for ax, ct in zip(axes, ["spherical", "diag", "tied", "full"]):
        g = GaussianMixture(3, covariance_type=ct, n_init=5, random_state=0).fit(X)
        z = g.predict(X)
        ax.scatter(X[:, 0], X[:, 1], c=list(PALETA[z]), s=5)
        elipses(ax, g.means_, covarianzas_completas(g))
        a = adjusted_rand_score(y, z)
        print(f"tipo {ct}: ARI = {a:.2f}, BIC = {g.bic(X):.0f}, parámetros = {g._n_parameters()}")
        ax.set_title(f'"{ct}"\nARI {a:.2f}, BIC {g.bic(X):.0f}', fontsize=11); sin_ejes(ax); ax.set_aspect("equal")
    guardar(fig, "tipos_covarianza")


def bic_sintetico():
    X, _ = datos_elipticos()
    ks = range(1, 8)
    bic, aic = [], []
    for k in ks:
        g = GaussianMixture(k, n_init=5, random_state=0).fit(X)
        bic.append(g.bic(X)); aic.append(g.aic(X))
    print("sintético BIC:", np.round(bic), "mín en k =", ks[int(np.argmin(bic))])
    print("sintético AIC:", np.round(aic), "mín en k =", ks[int(np.argmin(aic))])
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(ks, bic, "o-", color=AZUL, lw=2, label="BIC")
    ax.plot(ks, aic, "s--", color=NARANJA, lw=2, label="AIC")
    ax.axvline(3, color=GRIS, lw=0.8, ls=":")
    ax.set_xlabel("Número de componentes k"); ax.set_ylabel("Criterio (menor es mejor)")
    ax.legend(frameon=False); ax.set_title("Datos sintéticos, covarianza completa")
    guardar(fig, "bic_sintetico")


# ------------------------------------------------------------------
# Laboratorio con Iris
# ------------------------------------------------------------------
def iris_gmm():
    """k-medias contra GMM en el plano de los pétalos; se marcan las flores inciertas."""
    iris = load_iris()
    X, y = iris.data, iris.target
    z_km = KMeans(3, n_init=10, random_state=0).fit_predict(X)
    g = GaussianMixture(3, covariance_type="full", n_init=10, random_state=0).fit(X)
    z_g, P = g.predict(X), g.predict_proba(X)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for ax, z, t in [(axes[0], z_km, "k-medias"), (axes[1], z_g, "GMM (full)")]:
        orden = np.argsort([X[z == c, 2].mean() for c in range(3)])
        rango = np.empty(3, int); rango[orden] = np.arange(3)
        ax.scatter(X[:, 2], X[:, 3], c=list(COLOR_ESPECIE[rango[z]]), s=12)
        mal = rango[z] != y
        ax.scatter(X[mal, 2], X[mal, 3], facecolors="none", edgecolors="k", s=50, lw=0.8)
        ax.set_title(f"{t}: {mal.sum()} errores")
        print(f"iris {t}: {mal.sum()} flores fuera de su especie")
        ax.set_xlabel("Largo del pétalo (cm)")
    m = P.max(1) < 0.9
    axes[1].scatter(X[m, 2], X[m, 3], marker="*", color=NARANJA, s=140, edgecolors="k", lw=0.5,
                    label="probabilidad máx. < 0.9")
    axes[1].legend(fontsize=8, loc="upper left", frameon=False)
    elipses(axes[1], g.means_[:, 2:], g.covariances_[:, 2:, 2:], color=GRIS)
    axes[0].set_ylabel("Ancho del pétalo (cm)")
    guardar(fig, "iris_gmm")


def iris_bic():
    X = load_iris().data
    ks = range(1, 7)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharex=True)
    marcas = {"full": "o-", "tied": "s-", "diag": "^-", "spherical": "d-"}
    for ct, c in zip(marcas, [AZUL, NARANJA, VERDE, "#8E44AD"]):
        gs = [GaussianMixture(k, covariance_type=ct, n_init=10, random_state=0).fit(X) for k in ks]
        axes[0].plot(ks, [g.bic(X) for g in gs], marcas[ct], color=c, label=ct, lw=1.8)
        axes[1].plot(ks, [g.aic(X) for g in gs], marcas[ct], color=c, label=ct, lw=1.8)
    axes[0].set_title("BIC"); axes[1].set_title("AIC")
    for ax in axes:
        ax.set_xlabel("Número de componentes k"); ax.set_ylim(350, 1100)
    axes[0].set_ylabel("Criterio (menor es mejor)")
    axes[1].legend(frameon=False, fontsize=9, ncol=2)
    guardar(fig, "iris_bic")


if __name__ == "__main__":
    detonador(); gaussianas_2d(); asignacion_suave(); em_iteraciones(); optimos_locales(); tipos_covarianza(); bic_sintetico()
    iris_gmm(); iris_bic()
