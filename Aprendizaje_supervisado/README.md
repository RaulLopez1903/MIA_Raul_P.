# Aprendizaje Supervisado: materiales del curso

Sitio del curso (GitHub Pages): presentaciones en PDF y notebooks de las actividades.

## Estructura
- `index.html`, `assets/`: la página del curso.
- `modulo1/`: presentación de repaso de las Unidades 1–3, notebook del examen (sin solución) y entrega del examen (botón del formulario: variable `FORM_URL` en `index.html`).
- `curso/`: planeación didáctica (PDF).
- `unidad1/`, `unidad2/`, `unidad3/`: presentación, notebook y solución de cada unidad.
- `sincronizar.sh`: copia los materiales más recientes desde la carpeta de trabajo.
- `publicar.sh`: sincroniza, hace commit y sube a GitHub.

## Publicar por primera vez
1. Crea en GitHub un repositorio **vacío** (por ejemplo `supervised-learning`), sin README.
2. En esta carpeta: `./publicar.sh https://github.com/USUARIO/supervised-learning.git`
3. En GitHub: *Settings → Pages → Deploy from a branch → `main` / `(root)`*.
4. El sitio queda en `https://USUARIO.github.io/supervised-learning/`.

## Actualizar
Después de agregar materiales nuevos: `./publicar.sh`

Se publican las soluciones de las actividades de las Unidades 1–3 (`unidadN/solucion_*.ipynb`) y el examen del Módulo 1 sin solución. La solución del examen y cualquier otro solucionario están en `.gitignore`, y `publicar.sh` se detiene si detecta uno.
