import pygame
import sys
import random

# Inicia los módulos de pygame.
pygame.init()

# Configuración de variables.
ANCHO, ALTO = 800, 600
ancho_nave, alto_nave = 40, 40
ancho_bala, alto_bala = 10, 20
ancho_enemigo, alto_enemigo = 40, 40
velocidad_nave = 5
velocidad_bala = 10
velocidad_enemigo = 3
vidas_maximas = 3

# Creación de la ventana.
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Naves")

# Colores seleccionados.
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

# Estado del juego interno.
nave_x = ANCHO // 2 - ancho_nave // 2
nave_y = ALTO - alto_nave
balas = [[0, 0]] * 10  
enemigos = [[0, 0]] * 5  
vidas = vidas_maximas
puntuacion = 0

# Lista de jugadores.
class Jugador:
    def _init_(self, nombre, puntuacion):
        self.nombre = nombre
        self.puntuacion = puntuacion

    def _repr_(self):
        return f"{self.nombre}: {self.puntuacion}"

# Lista de puntuaciones.
registros = []

# Menu y nombre del jugador.
def solicitar_nombre():
    global jugador
    nombre = input("Introduce el nombre del jugador: ")
    jugador = Jugador(nombre, 0)

# Restablece el juego.
def reiniciar_juego():
    global nave_x, nave_y, balas, enemigos, vidas, puntuacion
    nave_x = ANCHO // 2 - ancho_nave // 2
    nave_y = ALTO - alto_nave
    balas = []
    enemigos = []
    vidas = vidas_maximas
    puntuacion = 0
    for _ in range(5):
        enemigos.append(crear_enemigo())

# Creación enemigo en posición aleatoria.
def crear_enemigo():
    x = random.randint(0, ANCHO - ancho_enemigo)
    y = -alto_enemigo
    return [x, y]

# Muestra la puntuación y las vidas en pantalla.
def mostrar_puntuacion_y_vidas():
    fuente = pygame.font.Font(None, 36)
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, NEGRO)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, NEGRO)
    ventana.blit(texto_puntuacion, (10, 10))
    ventana.blit(texto_vidas, (10, 40))

# Método de Ordenamiento por Inserción (InsertionSort) para enemigos en la pantalla.
def insertion_sort_enemigos(enemigos):
    for i in range(1, len(enemigos)):
        key = enemigos[i]
        j = i-1
        while j >= 0 and key[1] < enemigos[j][1]: 
            enemigos[j+1] = enemigos[j]
            j -= 1
        enemigos[j+1] = key

# Aumento de dificultad.
def aumentar_dificultad():
    global velocidad_enemigo
    if puntuacion % 50 == 0 and puntuacion > 0:
        velocidad_enemigo += 1  
        if len(enemigos) < 5:  
            enemigos.append(crear_enemigo())

# Ordenar y mostrar los registros.
def mostrar_registros():
    global registros
    registros.sort(key=lambda x: x.puntuacion, reverse=True)  
    print("\nRegistro de puntuaciones:")
    for jugador in registros:
        print(jugador)

# Solicita el nombre al inicio del juego.
solicitar_nombre()

# Reinicia el juego.
reiniciar_juego()

# Bucle principal del juego.
while True:
    ventana.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                balas.append([nave_x + ancho_nave // 2 - ancho_bala // 2, nave_y])

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave_x > 0:
        nave_x -= velocidad_nave
    if teclas[pygame.K_RIGHT] and nave_x < ANCHO - ancho_nave:
        nave_x += velocidad_nave
    if teclas[pygame.K_UP] and nave_y > 0:
        nave_y -= velocidad_nave
    if teclas[pygame.K_DOWN] and nave_y < ALTO - alto_nave:
        nave_y += velocidad_nave

    # Balas hacia arriba.
    balas = [[x, y - velocidad_bala] for x, y in balas if y > -alto_bala]

    # Enemigos hacia abajo.
    for i, (x, y) in enumerate(enemigos):
        enemigos[i][1] += velocidad_enemigo
        if y > ALTO:
            enemigos[i] = crear_enemigo()

    # Aumenta la dificultad.
    aumentar_dificultad()

    # Ordena los enemigos por su posición en el eje Y.
    insertion_sort_enemigos(enemigos)

    # Balas chocan con enemigo.
    for bala in balas:
        bx, by = bala
        for enemigo in enemigos:
            ex, ey = enemigo
            if ex < bx < ex + ancho_enemigo and ey < by < ey + alto_enemigo:
                balas.remove(bala)
                enemigos.remove(enemigo)
                puntuacion += 10
                enemigos.append(crear_enemigo())
                break

    # Enemigos colisionan con la nave.
    for enemigo in enemigos:
        ex, ey = enemigo
        if nave_x < ex < nave_x + ancho_nave and nave_y < ey < nave_y + alto_nave:
            vidas -= 1
            enemigos.remove(enemigo)
            enemigos.append(crear_enemigo())
            if vidas <= 0:
                print(f"\nJuego Terminado! Puntuación final: {puntuacion}")
                registros.append(Jugador(jugador.nombre, puntuacion))  # Guardar el puntaje del jugador.
                mostrar_registros()  # Mostrar los registros de puntuaciones.
                pygame.quit()
                sys.exit()

    # Dibuja la nave.
    pygame.draw.rect(ventana, AZUL, (nave_x, nave_y, ancho_nave, alto_nave))

    # Dibuja las balas.
    for bala in balas:
        pygame.draw.rect(ventana, AZUL, (bala[0], bala[1], ancho_bala, alto_bala))

    # Dibuja los enemigos.
    for enemigo in enemigos:
        pygame.draw.rect(ventana, ROJO, (enemigo[0], enemigo[1], ancho_enemigo, alto_enemigo))

    # Muestra la puntuación y las vidas.
    mostrar_puntuacion_y_vidas()
    pygame.display.flip()
    pygame.time.Clock().tick(30)