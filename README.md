# Actividad 2 - Sistema de Colas Consultorio Odontológico

**Programación 2** - Universidad de Manizales (2026-2)  
**Estudiante:** Nicolas David Solano Plazas  
**Código:** 106202524246  
**Fecha:** Octubre 2026  

---

## Descripción del proyecto

Para esta segunda actividad hice el sistema de atención de pacientes para el consultorio odontológico utilizando **colas de atención** (FIFO: el primero que llega es el primero en ser atendido). Tomé como base lo que trabajé en el primer taller y lo adapté para manejar la sala de espera diaria con `deque` de la librería `collections` de Python, que fue la estructura que nos explicó el profesor en clase.

El programa maneja dos colas: una para pacientes con citas normales de la agenda y otra para urgencias (como las extracciones dentales prioritarias). Para evitar que los pacientes normales se queden esperando todo el día si no paran de llegar urgencias (el problema de inanición o *starvation* que vimos en clase), le puse una regla de rotación sencilla: si hay pacientes en ambas colas, atiende dos urgencias seguidas y luego atiende obligatoriamente a uno de la cola general para mantener el equilibrio.

---

## Estructura de los archivos

Para mantener el código organizado y fácil de revisar, lo separé en módulos claros:

* **`cliente.py`**: Es la clase que guarda los datos del paciente (cédula, nombre, teléfono, afiliación, tratamiento, prioridad, fecha y hora). Aquí se calcula cuánto debe pagar según las tarifas (particular, EPS o prepagada), asegurando que el total sea un número decimal (`float`) y nunca negativo.
* **`cola_atencion.py`**: Es donde se maneja la lógica de las colas con `deque`. Tiene las funciones para encolar al paciente, atender al siguiente sacándolo con `popleft()`, mirar quién sigue sin sacarlo de la cola, y mostrar el estado de las colas con el conteo de personas y la plata total acumulada.
* **`utilidades.py`**: Aquí están las funciones que piden y validan datos por consola (que el documento y teléfono sean números, que las cantidades sean mayores a cero, que no dejen textos vacíos) y la función para cargar datos de prueba.
* **`main.py`**: Es el archivo principal que corre el menú en la consola con todas las opciones para interactuar con el sistema.

---

## Carga aleatoria de pacientes de prueba (`random`)

Para no tener que digitar paciente por paciente cada vez que se abre el programa a probar, le agregué una opción para cargar datos de prueba generados de forma aleatoria usando el módulo `random` de Python.

Cada vez que se usa esta opción, el sistema genera pacientes con nombres diferentes, cédulas únicas, distintos procedimientos, horas y prioridades combinadas (urgentes y normales). De esta forma se puede probar el programa varias veces seguidas y ver cómo se comportan las colas y los turnos con diferentes casos de prueba.

---

## Qué se puede hacer en el programa

1. **Registrar y encolar nuevo paciente**: Pide los datos por teclado, liquida el valor automáticamente y lo manda a la cola de urgencias o a la cola general según la prioridad.
2. **Atender siguiente paciente en turno**: Llama al paciente que le toca según la rotación de turnos, lo saca de la cola y genera su ticket detallado con el cobro.
3. **Consultar próximo paciente en turno**: Muestra quién es el siguiente en la fila sin sacarlo de la cola.
4. **Consultar todas las colas**: Imprime las tablas de urgencias y general, mostrando cuántos pacientes hay en espera y el monto total en dinero acumulado.
5. **Cargar agenda de pacientes de prueba**: Genera y encola 10 pacientes aleatorios para pruebas rápidas.
6. **Ver reporte de pacientes atendidos hoy**: Muestra el historial de los pacientes que ya pasaron por consulta en el día y el recaudo total en dinero.

---

## Cómo ejecutar el programa

1. Abrir la terminal o consola en la carpeta del proyecto:
   `Consultorio Odontologico`
2. Ejecutar el archivo principal:
   ```bash
   python main.py
   ```
   O en Windows:
   ```bash
   py main.py
   ```
3. Al iniciar, el programa te pregunta si quiere cargar los datos de prueba aleatorios para empezar a probar.
