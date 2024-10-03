
---

# 🚀 Space Shooter - Juego de Disparos en el Espacio

Este es un juego de disparos en el espacio desarrollado con **Pygame**. En el juego, controlas una nave espacial que debe esquivar meteoritos y destruirlos con tus disparos. El objetivo principal es sobrevivir el mayor tiempo posible, mientras acumulas puntos al destruir meteoritos. ¡Ten cuidado, si un meteorito choca contigo, el juego terminará!

## 📋 Contenido

- [Características](#características)
- [Instalación](#instalación)
- [Cómo Jugar](#cómo-jugar)
- [Estructura del Código](#estructura-del-código)
- [Puntajes](#puntajes)
- [Control del Jugador](#control-del-jugador)
- [Créditos](#créditos)

## 🌟 Características

- Control de la nave espacial para moverse y disparar.
- Meteoritos que caen aleatoriamente.
- Disparos láser para destruir los meteoritos.
- Sistema de puntajes que se guarda automáticamente.
- Menú de inicio con opciones para comenzar, ver el top 10 de puntajes y salir.
- Pantalla de "Game Over" con opción para reiniciar el juego o salir.
- Los puntajes más altos se guardan en un archivo `scores.json` y se pueden consultar en el menú principal.

## ⚙️ Instalación

### Requisitos

Este juego requiere que tengas instalado **Python** y la biblioteca **Pygame**. Si no tienes `pygame`, puedes instalarlo con el siguiente comando:

```bash
pip install pygame
```

### Ejecución del Juego

1. Clona este repositorio o descarga el código fuente en tu computadora.
2. Asegúrate de tener la carpeta `assets` en el mismo directorio donde se encuentra el archivo `game.py`. Esta carpeta debe contener las imágenes necesarias para los meteoritos y las estrellas.
3. Ejecuta el juego con el siguiente comando desde el terminal o línea de comandos:

```bash
python game.py
```

Esto abrirá la ventana del juego.

## 🎮 Cómo Jugar

### Controles:

- Usa las **flechas del teclado** para mover tu nave espacial en cualquier dirección:
  - **Izquierda**: Flecha izquierda
  - **Derecha**: Flecha derecha
  - **Arriba**: Flecha arriba
  - **Abajo**: Flecha abajo
- **Disparar**: Usa la tecla **Espacio** para disparar a los meteoritos.

### Objetivo del Juego

El objetivo es **sobrevivir** el mayor tiempo posible evitando los meteoritos y disparando para destruirlos. Obtienes puntos por cada meteorito destruido. Si uno de ellos choca contigo, el juego termina.

### Menús

1. **Menú principal**:
   - **1. Iniciar Juego**: Comienza una nueva partida.
   - **2. Ver top 10**: Muestra los 10 mejores puntajes guardados en un archivo JSON.
   - **3. Salir**: Cierra el juego.

2. **Menú de Game Over**:
   - **1. Reiniciar**: Comienza una nueva partida desde cero.
   - **2. Salir**: Cierra el juego.

### Sistema de Puntajes

El puntaje se calcula en función del número de meteoritos destruidos. Al final de la partida:
- El puntaje se guarda automáticamente en el archivo `scores.json`.
- Se mantiene una lista de los **10 mejores puntajes** que se puede consultar desde el menú principal.

### Guardado de Puntajes
- Los puntajes se almacenan en un archivo `scores.json` en el mismo directorio donde se ejecuta el juego.
- Si el archivo no existe, se creará automáticamente cuando se guarde el primer puntaje.
- El top 10 de puntajes se ordena de mayor a menor, mostrando los jugadores más hábiles.

## 🛠️ Estructura del Código

El código del juego está organizado de la siguiente manera:

- **game.py**: Archivo principal que contiene toda la lógica del juego y el ciclo principal.
- **player.py**: Módulo donde se define la clase `Player` que representa al jugador (la nave espacial).
- **meteor.py**: Módulo donde se define la clase `Meteor`, responsable de la lógica de los meteoritos enemigos.
- **star.py**: Módulo para las estrellas que sirven como fondo decorativo en el juego.
- **settings.py**: Archivo que contiene las constantes principales del juego, como el tamaño de la ventana (`WINDOW_WIDTH` y `WINDOW_HEIGHT`).
- **assets**: Carpeta que contiene los recursos gráficos, como imágenes de meteoritos y estrellas.

### Estructura de carpetas:

```
|-- src/
|   |-- game.py
|   |-- player.py
|   |-- meteor.py
|   |-- star.py
|   |-- settings.py
|-- assets/
|   |-- images/
|       |-- meteor.png
|       |-- star.png
|-- scores.json
```

### Detalles Importantes:
- **Meteor**: Los meteoros se generan de manera aleatoria desde la parte superior de la pantalla y caen hacia abajo.
- **Player**: El jugador controla una nave espacial que se mueve en todas las direcciones y dispara láseres.

## 🏆 Puntajes

El juego guarda los 10 mejores puntajes en el archivo `scores.json`. Este archivo se actualiza automáticamente cuando el jugador obtiene un puntaje que entra en el top 10.

El formato del archivo es simple:
```json
[100, 90, 85, 70, 60, 50, 45, 40, 35, 30]
```
Los puntajes están ordenados de mayor a menor.

## 🔄 Control del Jugador

El jugador puede moverse en las 4 direcciones usando las teclas de flecha del teclado y disparar usando la tecla `Espacio`. El juego detecta colisiones entre el jugador y los meteoritos usando máscaras para asegurarse de que las colisiones sean precisas.

---
