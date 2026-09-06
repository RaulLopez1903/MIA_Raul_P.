# Ejercicio 2 — Descripción PEAS de agentes inteligentes

**Curso:** Maestría en Inteligencia Artificial  
**Alumno:** Raúl Alejandro Pérez López  
**Asignatura:** Introducción a la IA  

---

## Descripciones PEAS por Aplicación

### 1. Asistente virtual de voz
*(p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente)*

- **Performance:** Comprender y ejecutar las tareas solicitadas de manera precisa, minimizando el tiempo de respuesta.
- **Environment:** Interior de una casa u oficina con ruido ambiental, presencia de personas y conexión a internet.
- **Actuators:** Altavoz (bocina), envío de instrucciones a otros aparatos inteligentes conectados.
- **Sensors:** Micrófono, botones físicos de interacción.

> **Justificación del entorno:** Es parcialmente observable porque no conoce por completo la casa y secuencial porque las respuestas anteriores afectan las respuestas futuras.

---

### 2. Robot aspirador doméstico
*(p. ej. Roomba u otro robot que limpia pisos de un departamento)*

- **Performance:** Maximizar la cobertura de limpieza del área, reduciendo el tiempo de trabajo y el consumo de energía.
- **Environment:** Interior de una casa con muebles, mascotas y personas en movimiento.
- **Actuators:** Motor de succión, ruedas de tracción, cepillos de limpieza, emisor de sonidos/alertas de proximidad.
- **Sensors:** Sensor de temperatura/calor, cámara, sensores de proximidad e impacto, botones de comandos.

> **Justificación del entorno:** Es parcialmente observable debido a que no detecta cosas fuera de su campo de visión, dinámico y estocástico porque las personas, mascotas y objetos se mueven constantemente.

---

### 3. Sistema de recomendación de streaming
*(p. ej. Netflix o Spotify que sugiere películas o canciones)*

- **Performance:** Lograr la aceptación de las recomendaciones en el menor tiempo de procesamiento posible.
- **Environment:** Catálogo de opciones disponibles en la plataforma y usuarios.
- **Actuators:** Autocompletar en el buscador, vista previa de la recomendación, reproducción automática, añadir o eliminar posibles sugerencias de la memoria.
- **Sensors:** Historial de reproducción del usuario, búsquedas recientes, métricas de similitud entre títulos, registro del comportamiento del usuario (omisiones/*skips*, sugerencias rechazadas o aceptadas).

> **Justificación del entorno:** Es estocástico porque la preferencia de un usuario es variable; secuencial ya que cada interacción o recomendación aceptada/rechazada modifica el futuro; y discreto debido a que opera sobre un catálogo definido de títulos.

---

### 4. Vehículo autónomo en ciudad
*(conducción sin conductor en calles urbanas con tráfico y peatones)*

- **Performance:** Garantizar la seguridad, la comodidad de los pasajeros, la velocidad adecuada y el cumplimiento de las leyes de tránsito.
- **Environment:** Calles y avenidas de la ciudad con tráfico vehicular, peatones y señales de tránsito.
- **Actuators:** Acelerador, freno, dirección (volante/llantas), claxon (bocina).
- **Sensors:** Mapas y detalles de la ruta, sensores térmicos/de calor, sensores de proximidad, cámaras, sensores eléctricos internos de diagnóstico, GPS.

> **Justificación del entorno:** Es estocástico y dinámico debido al comportamiento impredecible de peatones y otros conductores en tiempo real; parcialmente observable por los puntos ciegos; y continuo en aceleración y distancia.

---

### 5. Agente de trading algorítmico en bolsa
*(compra y venta automática de acciones en mercados financieros)*

- **Performance:** Maximizar las ganancias financieras y minimizar las pérdidas.
- **Environment:** Mercado de valores en línea con precios de acciones cambiantes e incertidumbre sobre el futuro, billetera (*wallet*) del usuario.
- **Actuators:** Ordenar compras o ventas de activos, solicitar retiro de efectivo, enviar notificaciones al usuario, generar estados de cuenta, mostrar el comportamiento del portafolio, sugerir operaciones de compra o venta.
- **Sensors:** Historial del comportamiento de las acciones, perfil de riesgo del usuario, noticias del mercado financiero y de las empresas.

> **Justificación del entorno:** Es estocástico porque los precios y eventos macroeconómicos futuros son inciertos y secuencial dado que una transacción altera la liquidez y el capital disponible para decisiones posteriores.

---

### 6. Sistema de diagnóstico médico asistido por IA
*(apoya a un médico a interpretar síntomas e imágenes clínicas)*

- **Performance:** Realizar diagnósticos correctos con rapidez, procurando el bienestar del paciente y minimizando los costos de los estudios o medicamentos.
- **Environment:** Sintomas del paciente, historial médico, base de datos médica de enfermedades y síntomas.
- **Actuators:** Generar y mostrar propuestas de diagnóstico, generar y mostrar sugerencias de recetas médicas, recomendar análisis o estudios médicos adicionales.
- **Sensors:** Teclado (entrada de datos), cámara (captura de imágenes clínicas), sensor de temperatura/calor.

> **Justificación del entorno:** Es parcialmente observable debido a que no todos los sintomas son observables (dolor); secuencial porque un diagnóstico o prueba inicial determina los pasos a seguir; y estocástico por las distintas reacciones de cada paciente.

---

### 7. Dron de inspección de infraestructura
*(revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas)*

- **Performance:** Optimizar la velocidad y la estabilidad del vuelo, lograr diagnósticos acertados, maximizar el alcance de la inspección y reducir el consumo de energía.
- **Environment:** Entornos exteriores a gran altura con estructuras fijas, clima variable, presencia de personas, automóviles, animales y situaciones extraordinarias.
- **Actuators:** Propulsores/aspas, altavoz para emisión de sonidos de ubicación o recuperación, envío de informes técnicos en tiempo real.
- **Sensors:** Cámara visual, sensor de calor/térmico, escáner, GPS.

> **Justificación del entorno:** Es estocástico y dinámico por los cambios en el clima (viento, lluvia) e imprevistos en el entorno; parcialmente observable al no poder visualizar la estructura completa desde un solo punto de vista; y continuo en velodidad o aceleración.

---

### 8. Agente jugador de ajedrez
*(programa que compite contra un humano u otro agente en partidas completas)*

- **Performance:** Maximizar el número de partidas ganadas, priorizar movimientos brillantes, minimizar errores y reducir el tiempo de pensamiento.
- **Environment:** Tablero con piezas de ajedrez en constante cambio de posición, reloj con tiempo restante definido y el oponente.
- **Actuators:** Mover piezas en el tablero, analizar posiciones de juego, rendirse.
- **Sensors:** Sensor/lector de los movimientos realizados por el rival, lector del tiempo restante en el reloj de juego.

> **Justificación del entorno:** Es totalmente observable porque el estado completo del tablero está siempre a la vista; discreto debido a que existe un número finito de casillas, piezas y turnos; y secuencial porque cada jugada condiciona las posiciones y estrategias del resto de la partida.
