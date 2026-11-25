# Página web del curso

Página publicada en https://cursosfmat.github.io/Aprendizaje_No_Supervisado/

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| `contenido.toml` | Texto de la página: datos del curso, evaluación, unidades, temas de cada sesión, recursos. |
| `estilo.css` | Diseño de la página. |
| `construir.py` | Genera la página en `_site/` a partir de `contenido.toml` y de los materiales del repositorio. |
| `../.github/workflows/pagina.yml` | Publica la página en GitHub Pages en cada push a `main`. |

La carpeta `_site/` se genera y no se guarda en git.

## Cómo se detectan los materiales

No hay que anotar las presentaciones en ningún lado. El script las busca:

- **Presentación de la sesión N**: `Sesion_N/SesionN-*.pdf`, por ejemplo `Sesion_3/Sesion3-Jerarquico.pdf`.
  Si existe, el botón «Presentación (PDF)» se activa; si no, aparece «Presentación: próximamente».
- **Notebooks de la sesión N**: cualquier `Sesion_N/*.ipynb`. Cada uno agrega los botones
  «Notebook» y «Abrir en Colab».

Si un PDF tiene otro nombre, se indica en la sesión con `presentacion = "ruta/al/archivo.pdf"`.

## Actualizar la página

Ver la guía paso a paso: **[Como_actualizar_la_pagina.md](Como_actualizar_la_pagina.md)**.

En resumen: compilar el PDF como `Sesion_N/SesionN-Tema.pdf`, hacer commit y push a `main`.
La página se reconstruye y publica sola en uno o dos minutos.

## Configuración

GitHub Pages está configurado con **Settings → Pages → Source: GitHub Actions** (ya hecho).
