#!/usr/bin/env python3
"""Construye la página web del curso.

Lee el texto de sitio/contenido.toml y busca los materiales en el repositorio:
  - presentación de la sesión N:  Sesion_N/SesionN-*.pdf
  - notebooks de la sesión N:     Sesion_N/*.ipynb
Genera index.html, copia la hoja de estilo y los archivos enlazados en la carpeta de salida.

Uso (desde cualquier carpeta):
    python3 sitio/construir.py                 # genera _site/ en la raíz del repositorio
    python3 sitio/construir.py --salida DIR    # otra carpeta de salida

Para revisar el resultado, abrir _site/index.html en el navegador.
En GitHub, el flujo .github/workflows/pagina.yml ejecuta este script y publica _site/.
Sólo usa la biblioteca estándar de Python (3.11 o posterior).
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import quote

SITIO = Path(__file__).resolve().parent
RAIZ = SITIO.parent
COLORES = {"u0", "u1", "u2", "u3"}


# ----------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------
def en_linea(texto):
    """Marcado ligero -> HTML: `código`, **negrita**, *cursiva*, [texto](url)."""
    t = html.escape(texto.strip(), quote=False)
    codigos = []

    def guardar(m):
        codigos.append(m.group(1))
        return f"\x00{len(codigos) - 1}\x00"

    t = re.sub(r"`([^`]+)`", guardar, t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: f'<a href="{m.group(2).replace(chr(34), "&quot;")}">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codigos[int(m.group(1))]}</code>", t)


def ruta_url(ruta):
    """Ruta relativa a la raíz del repositorio, codificada para usarse en un href."""
    return quote(ruta.relative_to(RAIZ).as_posix())


def en_git(ruta):
    """True si el archivo está registrado en git (sólo los registrados se publican en GitHub)."""
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", str(ruta)], cwd=RAIZ,
                           capture_output=True, check=False)
        return r.returncode == 0
    except FileNotFoundError:
        return True


class Error(Exception):
    pass


# ----------------------------------------------------------------------
# Materiales de cada sesión
# ----------------------------------------------------------------------
def materiales(sesion):
    n = sesion["numero"]
    carpeta = RAIZ / f"Sesion_{n}"
    if "presentacion" in sesion:
        pres = RAIZ / sesion["presentacion"]
        if not pres.is_file():
            raise Error(f"Sesión {n}: no existe la presentación indicada {sesion['presentacion']}")
    else:
        candidatos = sorted(carpeta.glob(f"Sesion{n}-*.pdf")) if carpeta.is_dir() else []
        pres = candidatos[0] if candidatos else None
    notebooks = sorted(carpeta.glob("*.ipynb")) if carpeta.is_dir() else []
    return pres, notebooks


# ----------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------
def boton(texto, href=None, secundario=False, extra=""):
    clase = "boton sec" if secundario else "boton"
    if href is None:
        return f'<a class="{clase}" aria-disabled="true">{texto}</a>'
    return f'<a class="{clase}" href="{href}"{extra}>{texto}</a>'


def tarjeta_sesion(s, unidad, pres, notebooks, curso):
    n = s["numero"]
    insignia = f' <span class="entrega">{en_linea(s["insignia"])}</span>' if s.get("insignia") else ""
    temas = "\n".join(f"          <li>{en_linea(t)}</li>" for t in s.get("temas", []))
    botones = []
    if pres:
        botones.append(boton("Presentación (PDF)", ruta_url(pres)))
    else:
        botones.append(boton("Presentación: próximamente"))
    for nb in notebooks:
        nombre = html.escape(nb.stem.replace("_", " "))
        botones.append(boton(f"Notebook: {nombre}", ruta_url(nb), True, " download"))
        colab = (f"https://colab.research.google.com/github/{curso['repositorio']}/blob/"
                 f"{curso['rama']}/{ruta_url(nb)}")
        botones.append(boton("Abrir en Colab", colab, True, ' target="_blank" rel="noopener"'))
    notas = ""
    if s.get("laboratorio"):
        notas += f'\n        <p class="nota"><b>Laboratorio:</b> {en_linea(s["laboratorio"])}</p>'
    if s.get("entrega"):
        notas += f'\n        <p class="nota"><b>Entrega:</b> {en_linea(s["entrega"])}</p>'
    return f"""
    <article class="sesion {unidad['color']}" id="sesion{n}">
      <header><span class="num">Sesión {n}</span><h3>{en_linea(s['titulo'])}{insignia}</h3></header>
      <div class="cuerpo">
        <p><b>Temas:</b></p>
        <ul>
{temas}
        </ul>
        <div class="botones">{''.join(botones)}</div>{notas}
      </div>
    </article>"""


def lista(elementos, clase=""):
    atributo = f' class="{clase}"' if clase else ""
    items = "\n".join(f"    <li>{en_linea(e)}</li>" for e in elementos)
    return f"<ul{atributo}>\n{items}\n  </ul>"


def pagina(datos, tarjetas_por_unidad):
    c = datos["curso"]
    unidades = datos["unidades"]
    nav = "\n".join([
        '    <a href="#curso">Curso</a>',
        '    <a href="#evaluacion">Evaluación</a>',
        *[f'    <a href="#{u["id"]}">{html.escape(u["nombre"])}</a>' for u in unidades],
        '    <a href="#recursos">Recursos</a>',
    ])
    tarjetas_datos = "\n".join(
        f'    <div class="dato"><b>{en_linea(d["titulo"])}</b><span>{en_linea(d["texto"])}</span></div>'
        for d in datos.get("datos", []))
    filas_eval = "\n".join(
        f'      <tr><td>{en_linea(e["elemento"])}</td><td>{en_linea(e["entrega"])}</td>'
        f'<td class="num">{en_linea(e["peso"])}</td></tr>'
        for e in datos.get("evaluacion", []))
    mapa = "\n".join(
        f'    <a class="{u["color"]}" href="#{u["id"]}"><b>{html.escape(u["nombre"])}</b>'
        f'<span>{en_linea(u["mapa"])}</span></a>'
        for u in unidades)
    bloques = "\n".join(f"""
  <section class="bloque {u['color']}" id="{u['id']}">
    <h2>{en_linea(u['titulo'])}</h2>
    <p>{en_linea(u['resumen'])}</p>{''.join(tarjetas_por_unidad[u['id']])}
  </section>""" for u in unidades)
    r = datos.get("recursos", {})
    planeacion = quote(c["planeacion_pdf"])

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(c['titulo'])}</title>
<meta name="description" content="Materiales del curso {html.escape(c['titulo'])}: planeación didáctica y presentaciones de las sesiones.">
<link rel="stylesheet" href="estilo.css">
</head>
<body>
<!-- Archivo generado por sitio/construir.py a partir de sitio/contenido.toml. No editar a mano. -->

<header class="portada">
  <div class="contenedor">
    <span class="etiqueta">{en_linea(c['etiqueta'])}</span>
    <h1>{html.escape(c['titulo'])}</h1>
    <p>{en_linea(c['subtitulo'])}</p>
  </div>
</header>

<nav class="indice" aria-label="Secciones">
  <div class="contenedor">
{nav}
  </div>
</nav>

<main class="contenedor">

  <h2 id="curso">Sobre el curso</h2>
  <p>{en_linea(c['descripcion'])}</p>
  <div class="cuadricula">
{tarjetas_datos}
  </div>
  <p class="competencia"><b>Competencia de la asignatura.</b> {en_linea(c['competencia'])}</p>
  <p><b>Requisitos recomendados:</b> {en_linea(c['requisitos'])}</p>
  <div class="botones">
    {boton("Planeación didáctica (PDF)", planeacion)}
  </div>

  <h2 id="evaluacion">Evaluación</h2>
  <table class="tabla">
    <thead><tr><th>Elemento de evaluación</th><th>Entrega</th><th style="text-align:right">Peso</th></tr></thead>
    <tbody>
{filas_eval}
    </tbody>
  </table>

  <h2>Sesiones</h2>
  <div class="mapa">
{mapa}
  </div>
{bloques}

  <h2 id="recursos">Software y recursos</h2>
  <div class="recursos">
    <section>
      <h3>Software</h3>
  {lista(r.get('software', []))}
    </section>
    <section>
      <h3>Documentación y datos</h3>
  {lista(r.get('documentacion', []))}
    </section>
  </div>

  <h3>Bibliografía básica</h3>
  {lista(r.get('bibliografia_basica', []), 'bibliografia')}
  <h3>Bibliografía complementaria</h3>
  {lista(r.get('bibliografia_complementaria', []), 'bibliografia')}
</main>

<footer>
  <div class="contenedor">{en_linea(c['pie'])}</div>
</footer>

</body>
</html>
"""


# ----------------------------------------------------------------------
# Construcción
# ----------------------------------------------------------------------
REQUERIDOS = {
    "curso": ["titulo", "etiqueta", "subtitulo", "descripcion", "competencia", "requisitos",
              "planeacion_pdf", "pie", "repositorio", "rama"],
    "unidades": ["id", "nombre", "titulo", "resumen", "mapa", "color"],
    "sesiones": ["numero", "unidad", "titulo", "temas"],
    "evaluacion": ["elemento", "entrega", "peso"],
    "datos": ["titulo", "texto"],
}


def leer_contenido():
    """Lee contenido.toml y revisa que tenga los campos necesarios."""
    try:
        with open(SITIO / "contenido.toml", "rb") as f:
            datos = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise Error(f"sitio/contenido.toml tiene un error de sintaxis: {e}. "
                    "Revisar comillas, comas y corchetes en esa línea.")
    if "curso" not in datos:
        raise Error("sitio/contenido.toml: falta la sección [curso]")
    for campo in REQUERIDOS["curso"]:
        if campo not in datos["curso"]:
            raise Error(f"sitio/contenido.toml: falta el campo «{campo}» en [curso]")
    for seccion in ("unidades", "sesiones"):
        if not datos.get(seccion):
            raise Error(f"sitio/contenido.toml: no hay ninguna entrada [[{seccion}]]")
    for seccion in ("unidades", "sesiones", "evaluacion", "datos"):
        for i, entrada in enumerate(datos.get(seccion, []), start=1):
            for campo in REQUERIDOS[seccion]:
                if campo not in entrada:
                    donde = (f"la sesión {entrada['numero']}" if "numero" in entrada
                             else f"la entrada {i} de [[{seccion}]]")
                    raise Error(f"sitio/contenido.toml: falta el campo «{campo}» en {donde}")
    return datos


def construir(salida):
    datos = leer_contenido()
    curso = datos["curso"]
    unidades = {u["id"]: u for u in datos["unidades"]}
    for u in unidades.values():
        if u["color"] not in COLORES:
            raise Error(f"Unidad {u['id']}: color {u['color']!r} no válido (usar {sorted(COLORES)})")

    planeacion = RAIZ / curso["planeacion_pdf"]
    if not planeacion.is_file():
        raise Error(f"No existe la planeación {curso['planeacion_pdf']}")

    numeros = [s["numero"] for s in datos["sesiones"]]
    if len(numeros) != len(set(numeros)):
        raise Error("Hay números de sesión repetidos en contenido.toml")

    a_copiar = [planeacion]
    tarjetas = {uid: [] for uid in unidades}
    resumen, avisos = [], []
    for s in sorted(datos["sesiones"], key=lambda s: s["numero"]):
        if s["unidad"] not in unidades:
            raise Error(f"Sesión {s['numero']}: la unidad {s['unidad']!r} no existe")
        pres, notebooks = materiales(s)
        for archivo in ([pres] if pres else []) + notebooks:
            a_copiar.append(archivo)
            if not en_git(archivo):
                avisos.append(f"{archivo.relative_to(RAIZ)} no está en git: no se publicará hasta hacer commit")
        tarjetas[s["unidad"]].append(tarjeta_sesion(s, unidades[s["unidad"]], pres, notebooks, curso))
        resumen.append((s["numero"], pres.relative_to(RAIZ).as_posix() if pres else "—", len(notebooks)))

    # Carpeta de salida limpia. Sólo se borra si la generó este script (archivo marcador)
    # o si está vacía, para no borrar por error una carpeta con otro contenido.
    marcador = salida / ".generado-por-construir"
    if salida.exists():
        if not (marcador.exists() or not any(salida.iterdir())):
            raise Error(f"{salida} ya existe y no la generó este script; elegir otra carpeta de salida")
        shutil.rmtree(salida)
    salida.mkdir(parents=True)
    marcador.touch()
    (salida / "index.html").write_text(pagina(datos, tarjetas), encoding="utf-8")
    shutil.copy2(SITIO / "estilo.css", salida / "estilo.css")
    (salida / ".nojekyll").touch()
    for archivo in a_copiar:
        destino = salida / archivo.relative_to(RAIZ)
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(archivo, destino)

    print(f"Página generada en {salida}/index.html")
    print(f"{'Sesión':>7}  {'Presentación':<38} Notebooks")
    for n, p, nb in resumen:
        print(f"{n:>7}  {p:<38} {nb}")
    for a in avisos:
        print(f"Aviso: {a}")


def main():
    ap = argparse.ArgumentParser(description="Construye la página web del curso.")
    ap.add_argument("--salida", type=Path, default=RAIZ / "_site",
                    help="carpeta de salida (por omisión, _site/ en la raíz del repositorio)")
    args = ap.parse_args()
    salida = args.salida.resolve()
    if salida == RAIZ or RAIZ.is_relative_to(salida) or salida == SITIO:
        sys.exit("La carpeta de salida no puede ser la raíz del repositorio ni sitio/")
    try:
        construir(salida)
    except Error as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
