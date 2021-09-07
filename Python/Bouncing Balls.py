"""Animación de pelotas rebotando

Basada en los tutoriales creados por TokyoEdTech en Youtube:
    Canal - https://www.youtube.com/c/tokyoedtech
    Playlist del tutorial - https://www.youtube.com/playlist?list=PLlEgNdBJEO-mRsbxRND_Cu805SCrXoOZB

Por Salvador Bravo Garnica el 01 de septiembre de 2021"""

import random
import time
import turtle

# Configurar la librería para aceptar valores de RGB
turtle.colormode(255)

# Crear una ventana
ventana = turtle.Screen()

# Añadir un título a la ventana
ventana.title('Pelotas por SalvadorBG')

# Poner el color de fondo de la ventana en negro
ventana.bgcolor((0, 0, 0))

# Ajustar las dimensiones de la ventana (pixeles x pixeles)
ventana.setup(610, 610)

# La ventana no se actualizará automáticamente, de esta forma creamos resultados más fluidos
ventana.tracer(0)

# Crear todas las pelotas de la animación
pelotas = [turtle.Turtle() for _ in range(25)]

# Configurar las características de cada pelota
for pelota in pelotas:

    # Hacer que las pelotas tengan forma de círculo
    pelota.shape('circle')

    # Seleccionar los valores de RGB de la pelota aleatoriamente
    R = random.randint(0, 255)
    B = random.randint(0, 255)
    G = random.randint(0, 255)

    # Darle el color a la pelota
    pelota.color((R, G, B))

    # Esta línea es para que la pelota no deje su rastro dibujado
    pelota.penup()

    # Seleccionar los valores de la posición inicial de la pelota al azar
    x = random.randint(-280, 280)
    y = random.randint(-200, 280)

    # Desactivar las animaciones de movimiento de la pelota (más fluidez)
    pelota.speed(0)

    # Darle la posición a la pelota
    pelota.goto(x, y)

    # Qué tanto se moverá la pelota en el eje y en el siguiente fotograma
    pelota.dy = 0

    # Que tanto se moverá la pelota en el eje x en el siguiente fotograma
    pelota.dx = random.randint(-5, 5)

# Gravedad aplicada a las pelotas, se usa para hacer que las pelotas caigan al suelo
gravedad = 0.1

# Cuántos segundos debe durar como mínimo cada fotograma (1 / [fotogramas máximos])
segundos_por_fotograma = 1 / 120

# Ciclo principal de la animación
while True:

    # El tiempo exacto donde iniciaron los cálculos del fotograma
    inicio_fotograma = time.time()

    # Iterar sobre cada pelota
    for pelota in pelotas:
        # Añadir el efecto de la gravedad a su movimiento en y
        pelota.dy -= gravedad

        # Mover la pelota a su nueva posición en y
        pelota.sety(pelota.ycor() + pelota.dy)

        # Mover la pelota a su nueva posición en x
        pelota.setx(pelota.xcor() + pelota.dx)

        # Checar que la pelota siempre se encuentre dentro del área visible de la ventana
        if not -290 < pelota.xcor() < 290:
            # Si no es así, invertir el sentido del movimiento en el eje x
            pelota.dx *= -1

        # Checar si la pelota tiene colisión con el piso (que "rebote")
        if pelota.ycor() < -290:
            # Esta línea elimina el bug donde las pelotas se quedan atoradas debajo del piso
            pelota.sety(-290)

            # Invertir el sentido del movimiento en el eje y ("rebote")
            pelota.dy *= -1

    # El tiempo exacto donde finalizaron los cálculos del fotograma
    fin_fotograma = time.time()

    # Tiempo total que tardaron en hacerse los cálculos del fotograma
    total_fotograma = fin_fotograma - inicio_fotograma

    # Checar si tardamos menos tiempo del que tenemos marcado por los segundos_por_fotograma
    if total_fotograma < segundos_por_fotograma:
        # Si es así, esperar el tiempo restante
        time.sleep(segundos_por_fotograma - total_fotograma)

    # Actualizar la ventana (dibujar el nuevo fotograma en pantalla)
    ventana.update()
