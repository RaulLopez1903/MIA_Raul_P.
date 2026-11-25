# Cómo actualizar la página web del curso

Página: https://cursosfmat.github.io/Aprendizaje_No_Supervisado/

La página se publica **sola** cada vez que haces `git push` a `main` con cambios en
`Sesion_*/`, `sitio/` o en el PDF de la planeación. No hay que editar HTML.

Todos los comandos se escriben desde la raíz del repositorio:

```
cd ~/docs/Docencia/Aprendizaje_No_Supervisado-MIA/Aprendizaje_No_Supervisado
```

---

## Resumen rápido

```
# 1. Compilar la presentación de la sesión N (queda como Sesion_N/SesionN-Tema.pdf)
cd Sesion_3 && latexmk -pdf Sesion3-Jerarquico.tex && cd ..

# 2. (Opcional) Revisar la página en local y abrir _site/index.html
python3 sitio/construir.py

# 3. Subir los cambios
git add Sesion_3
git commit -m "Agrega la presentación de la Sesión 3"
git push

# 4. (Opcional) Seguir la publicación
gh run watch
```

En uno o dos minutos la página muestra el botón «Presentación (PDF)» de la sesión.

---

## 1. Publicar la presentación de una sesión

1. Trabajar la presentación en la carpeta `Sesion_N/`. El PDF debe llamarse
   **`SesionN-Algo.pdf`**: la palabra `Sesion`, el número **sin guion bajo**, un guion y un nombre.

   | Correcto | No se detecta |
   | --- | --- |
   | `Sesion_3/Sesion3-Jerarquico.pdf` | `Sesion_3/Sesion_3-Jerarquico.pdf` |
   | `Sesion_10/Sesion10-VariablesLatentes.pdf` | `Sesion_3/presentacion.pdf` |

   Si prefieres otro nombre, indícalo en `sitio/contenido.toml` dentro de la sesión
   (ver la sección 3): `presentacion = "Sesion_3/presentacion.pdf"`.

2. Compilar:
   ```
   cd Sesion_3
   latexmk -pdf Sesion3-Jerarquico.tex
   cd ..
   ```
   Los archivos auxiliares de LaTeX (`.aux`, `.log`, `.nav`…) están en `.gitignore`: no se suben.

3. (Opcional) Revisar en local, como se explica en la sección 5.

4. Subir los cambios (incluye el `.tex`, el PDF y las figuras):
   ```
   git add Sesion_3
   git commit -m "Agrega la presentación de la Sesión 3"
   git push
   ```

5. Comprobar la publicación (sección 6).

Para **corregir** una presentación ya publicada se sigue el mismo proceso: recompilar,
`git add`, `git commit` y `git push`. La página enlaza siempre la última versión del PDF.

---

## 2. Publicar notebooks

Cualquier archivo `.ipynb` dentro de `Sesion_N/` agrega a la tarjeta de la sesión dos botones:
«Notebook: nombre» (descarga) y «Abrir en Colab».

```
git add Sesion_3/demostracion_dendrogramas.ipynb
git commit -m "Agrega el notebook de la Sesión 3"
git push
```

- El nombre del botón sale del nombre del archivo (los guiones bajos se muestran como espacios).
- «Abrir en Colab» sólo funciona cuando el notebook ya está en GitHub (después del push).
- Conviene guardar los notebooks **ya ejecutados** si se quiere que muestren resultados sin correrlos.

---

## 3. Cambiar textos: temas, títulos, laboratorios, evaluación

Todo el texto está en **`sitio/contenido.toml`**. Cada sesión es un bloque como este:

```toml
[[sesiones]]
numero = 3
unidad = "unidad1"
titulo = "Agrupamiento jerárquico"
temas = [
  "Enfoques aglomerativo y divisivo.",
  "Criterios de enlace: simple, completo, promedio y Ward.",
]
laboratorio = "agrupamiento jerárquico con SciPy e interpretación de dendrogramas."
```

Campos opcionales de una sesión:

| Campo | Efecto |
| --- | --- |
| `laboratorio = "…"` | Nota «Laboratorio: …» bajo los botones. |
| `entrega = "…"` | Nota «Entrega: …». |
| `insignia = "Miniproyecto 1"` | Etiqueta naranja junto al título. |
| `presentacion = "ruta.pdf"` | PDF con un nombre que no sigue la regla `SesionN-*.pdf`. |

Marcado permitido en los textos: `` `código` ``, `*cursiva*`, `**negrita**`, `[texto](https://…)`.

Otras secciones del mismo archivo: `[curso]` (descripción, competencia, requisitos),
`[[datos]]` (tarjetas), `[[evaluacion]]` (tabla de pesos), `[[unidades]]` y `[recursos]`.

Después de editar:
```
python3 sitio/construir.py        # comprueba que no haya errores
git add sitio/contenido.toml
git commit -m "Actualiza los temas de la Sesión 3 en la página"
git push
```

> **Importante:** la página no lee la planeación didáctica. Si cambias temas, títulos o
> pesos en `Planeacion_Didactica-Aprendizaje_No_Supervisado.tex`, haz el mismo cambio en
> `sitio/contenido.toml`.

---

## 4. Actualizar la planeación didáctica

```
latexmk -pdf Planeacion_Didactica-Aprendizaje_No_Supervisado.tex
git add Planeacion_Didactica-Aprendizaje_No_Supervisado.tex Planeacion_Didactica-Aprendizaje_No_Supervisado.pdf
git commit -m "Actualiza la planeación didáctica"
git push
```

El botón «Planeación didáctica (PDF)» enlaza siempre al PDF de la raíz del repositorio.
Si cambias el **nombre** del PDF, actualízalo en dos lugares: `planeacion_pdf` en
`sitio/contenido.toml` y la lista `paths` de `.github/workflows/pagina.yml`.

---

## 5. Revisar la página en local antes de publicar

```
python3 sitio/construir.py
```

Luego abrir `_site/index.html` en el navegador (por ejemplo, `xdg-open _site/index.html`).
El script imprime qué sesiones tienen presentación y notebooks:

```
 Sesión  Presentación                           Notebooks
      1  Sesion_1/Sesion1-Introduccion.pdf      0
      2  Sesion_2/Sesion2-KMedias.pdf           0
      3  —                                      0
```

Si escribe `Aviso: … no está en git`, ese archivo se ve en local pero **no se publicará**
hasta hacer `git add` y `git commit`.

La carpeta `_site/` es sólo para revisar; está en `.gitignore` y no se sube.
Requiere Python 3.11 o posterior.

---

## 6. Comprobar que se publicó

- En la terminal:
  ```
  gh run list --workflow pagina.yml --limit 3   # últimas publicaciones
  gh run watch                                  # seguir la que está en curso
  ```
- En el navegador: pestaña **Actions** del repositorio, flujo «Página del curso».
  Un círculo verde indica que se publicó.

La página puede tardar unos minutos en mostrar los cambios por la caché del navegador:
recargar con **Ctrl + Shift + R**.

---

## 7. Si algo sale mal

| Problema | Qué hacer |
| --- | --- |
| La página no cambió y no hubo publicación | El push no tocó `Sesion_*/`, `sitio/` ni la planeación. Publicar a mano: `gh workflow run pagina.yml`. |
| La publicación falló (círculo rojo) | Ver el error: `gh run view --log-failed`. Corregir, hacer commit y push. |
| Error de sintaxis en `contenido.toml` | Revisar comillas, comas entre temas y corchetes. `python3 sitio/construir.py` indica la línea. |
| `Error: Sesión N: no existe la presentación indicada` | La ruta de `presentacion = "…"` está mal escrita o el PDF no se subió. |
| `Error: No existe la planeación …` | Se renombró o borró el PDF de la planeación (ver sección 4). |
| El botón de una sesión sigue en «próximamente» | El PDF no sigue la regla `Sesion_N/SesionN-*.pdf` o no está en git. |
| `gh` pide iniciar sesión | `gh auth status` para revisar; `gh auth login` para volver a entrar. |
| La página muestra el README en lugar del curso | En GitHub: Settings → Pages → Source debe ser **GitHub Actions**. |

---

## Archivos involucrados

| Archivo | Qué contiene |
| --- | --- |
| `sitio/contenido.toml` | Texto de la página (lo que normalmente se edita). |
| `sitio/estilo.css` | Diseño: colores, tipografía, tarjetas. |
| `sitio/construir.py` | Genera la página y detecta los materiales. |
| `.github/workflows/pagina.yml` | Construye y publica la página en GitHub Pages en cada push a `main`. |
| `_site/` | Página generada en local (no se sube a git). |
