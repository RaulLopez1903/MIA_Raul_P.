# Ejercicio 2 — Descripción PEAS de agentes inteligentes

## Contexto

En el capítulo 2 de *Artificial Intelligence: A Modern Approach* (Russell & Norvig), un agente se entiende mejor cuando se especifica su **entorno de tarea**. Una forma estándar de hacerlo es la descripción **PEAS**:

| Letra | Significado | Pregunta guía |
|---|---|---|
| **P** | *Performance* (medida de desempeño) | ¿Cómo se evalúa el éxito del agente? |
| **E** | *Environment* (entorno) | ¿En qué mundo opera? ¿Quién más actúa ahí? |
| **A** | *Actuators* (actuadores) | ¿Qué acciones puede ejecutar? |
| **S** | *Sensors* (sensores) | ¿Qué información puede percibir? |

Este ejercicio **no requiere programar**. Consiste en analizar distintos tipos de aplicaciones reales y describir cada una con el esquema PEAS.

## Objetivo

Para cada una de las **8 aplicaciones** listadas abajo, redacta una descripción PEAS completa y coherente. Debes pensar como diseñador del agente: qué optimiza, dónde actúa, con qué puede mover o modificar el mundo, y qué puede observar.

## Aplicaciones a analizar

### 1. Asistente virtual de voz
*(p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente)*

- **Performance:** Comprender y ejecutar las tareas solicitadas de manera precisa y con el menor tiempo de respuesta posible.
- **Environment:** Casa u oficina con ruido, personas, internet (parcialmente observable).
- **Actuators:** Bocina, envio de instrucciones a otros aparatos.
- **Sensors:** Micrófono, botones.
---

### 2. Robot aspirador doméstico
*(p. ej. Roomba u otro robot que limpia pisos de un departamento)*

- **Performance:** Mayor alcance de limpieza con menor tiempo y consumo de energía.
- **Environment:** Interior de una vivienda con presencia de personas, mascotas y muebles (parcialmente observable).
- **Actuators:** Motor de succión, ruedas giratorias, bocina de sonido de proximidad, cepillos giratorios.
- **Sensors:** Sensor de calor, cámara, sensor de proximidad, botones de comandos.

---

### 3. Sistema de recomendación de streaming
*(p. ej. Netflix o Spotify que sugiere películas o canciones)*

- **Performance:** Recomendaciones aceptadas en menor tiempo de procesamiento.
- **Environment:** Opciones disponibles en la plataforma, usuarios (estocástico).
- **Actuators:** Autocompletar en el buscador, preview de la recomendación, reproducción automática, añadir o eliminar de memoria posibles sugerencias.
- **Sensors:** Historial de reproducción del usuario, búsquedas recientes, sistema de `similitud` entre títulos, comportamiento del usuario (skips, sugerencias rechazadas o aceptadas).

---

### 4. Vehículo autónomo en ciudad
*(conducción sin conductor en calles urbanas con tráfico y peatones)*

- **Performance:** Comodidad, velocidad, cumplimiento de leyes de tránsito, seguridad.
- **Environment:** Calles y avenidas de la ciudad con tráfico, peatones y señales de tránsito (estocástico).
- **Actuators:** Acelerador, freno, llantas, volante, bocinas.
- **Sensors:** Detalles de la ruta, sensores de calor, sensores de proximidad, cámaras, sensores eléctricos internos, GPS.

---

### 5. Agente de trading algorítmico en bolsa
*(compra y venta automática de acciones en mercados financieros)*

- **Performance:** Minimizar pérdidas y maximizar ganancias.
- **Environment:** Mercado de valores en línea, con acciones de precios cambiantes e incertidumbre del futuro, wallet del usuario (estocástico).
- **Actuators:** Ordenar compras o ventas, retiro de efectivo, notificaciones al usuario, generar estado de cuenta, mostrar comportamiento del portafolio, sugerir compras o ventas.
- **Sensors:** Historial de comportamiento de las acciones, perfil de riesgo del usuario, noticias del mercado o empresas.

---

### 6. Sistema de diagnóstico médico asistido por IA
*(apoya a un médico a interpretar síntomas e imágenes clínicas)*

- **Performance:** Realizar diagnósticos correctos, rapidez, bienestar del paciente, minimizar costos al paciente.
- **Environment:** Paciente, historial médico del paciente, base de datos médica (enfermedad-síntomas) (parcialmente observable).
- **Actuators:** Generar y mostrar diagnóstico, generar y mostrar receta médica, sugerir análisis médicos.
- **Sensors:** Teclado, cámara, sensor de calor.

---

### 7. Dron de inspección de infraestructura
*(revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas)*

- **Performance:** Velocidad, diagnósticos acertados, maximizar alcance de inspección, menor consumo de energía, estabilidad.
- **Environment:** Alturas exteriores con estructuras fijas, clima variable, personas, autos, animales y situaciones extraordinarias (estocástico).
- **Actuators:** Aspas, bocina para sonidos de recuperación, envío de informes en tiempo real.
- **Sensors:** Cámara, sensor de calor, escáner, GPS.

---

### 8. Agente jugador de ajedrez
*(programa que compite contra un humano u otro agente en partidas completas)*

- **Performance:** Partidas ganadas, maximizar movimientos brillantes, minimizar movimientos de error, minimizar tiempo de pensamiento.
- **Environment:** Tablero con piezas de ajedrez en constante movimiento y reloj con tiempo de juego restante definido, rival (totalmente observable).
- **Actuators:** Mover pieza, analizar posición, rendirse.
- **Sensors:** Sensor de movimientos del rival y lector de reloj con tiempo restante de juego.

---

## Instrucciones

Para **cada** aplicación entrega una sección con este formato:

```markdown
### N. Nombre de la aplicación

- **Performance:** ...
- **Environment:** ...
- **Actuators:** ...
- **Sensors:** ...
