# La Encomienda de Oro

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Graphics](https://img.shields.io/badge/Graphics-Turtle-green.svg)](https://docs.python.org/3/library/turtle.html)


**La Encomienda de Oro** es un juego en la terminal por turnos desarrollado en Python. Mezcla el diseño de mecánicas sistémicas con una narrativa estilo *Visual Novel* y un entorno gráfico vectorial renderizado en tiempo real mediante `turtle`.

El juego sitúa al usuario ante un dilema clásico de optimización de recursos y gestión del estrés: cruzar una metrópolis caótica en hora punta para recuperar una frágil y valiosa caja de música para las **Bodas de Oro** (50º aniversario) de sus abuelos antes de que la tienda de antigüedades eche el cierre definitivo.

---

## Mecánicas del Juego
**La Encomienda de Oro** cuenta con diversas mecánicas que hacen la aventura se sienta viva:

* **Motor de Notificaciones:** El protagonista tiene acceso a su teléfono. El juego implementa un motor de mensajes con un ratio de aparición balanceado que inyecta hilos de conversación.
* **El Reloj del Silencio:** Ignorar los mensajes urgentes de tu pareja tiene consecuencias (como en la vida real). Cuenta con una máquina de estados que, de llegar a su límite, provoca una mutación geométrica del mapa urbano.
* **Encuentros RPG:** Al cruzar las calles, el mapa puede pausarse para sumergir al jugador en árboles de diálogo ramificados de múltiple elección con NPCs, donde cada decisión altera el Tiempo, el Ánimo y el Karma.

---


## Cómo Jugar

### Requisitos Previos
* Python 3.11 o superior instalado.

### Instalación y Ejecución
1.  Clona este repositorio o descarga el archivo `main.py` de la Gigathon.
2.  Ejecuta el script principal desde tu terminal:
    ```bash
    python main.py
    ```

### Controles de la Consola
* `[1]` **Desplazar Personaje:**
    * **Controles de dirección:** `W` (Norte), `S` (Sur), `A` (Oeste), `D` (Este) y diagonales compuestas (`WD`, `WA`, `SD`, `SA`).
    * **Velocidades de zancada:** `1` (Normal), `2` (Prisa: drena ánimo), `3` (Sprint: drena mucho ánimo, bloqueado si estás lesionado).
* `[2]` **Sacar Teléfono Móvil:** Pausa el mapa para ver las aplicaciones. Navega usando las opciones numéricas para responder chats pendientes, mirar el radar con rumbo preciso o consumir ítems de la mochila.

---


## Autor

**Carlos Andrés Angulo Rosales** 
