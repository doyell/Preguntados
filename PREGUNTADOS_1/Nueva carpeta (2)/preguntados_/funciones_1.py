import pygame
import random
import csv
from constantes_1 import fondo, imagen_boton, imagen_boton_hover, fondos_categoria, BLANCO, NEGRO

# Función para dibujar un botón con una imagen
def dibujar_boton(texto, x, y, ancho, alto, hover=False, pantalla=None):
    imagen = imagen_boton_hover if hover else imagen_boton
    pantalla.blit(imagen, (x, y))  # Usar pantalla que es pasada como argumento
    font = pygame.font.SysFont("Arial", 30)
    texto_superficie = font.render(texto, True, BLANCO)
    pantalla.blit(texto_superficie, (x + (ancho - texto_superficie.get_width()) // 2, y + (alto - texto_superficie.get_height()) // 2))

# Función para detectar si el botón fue presionado
def boton_presionado(x, y, ancho, alto, mouse_x, mouse_y):
    return x < mouse_x < x + ancho and y < mouse_y < y + alto

# Función para cargar preguntas desde un archivo CSV
def cargar_preguntas():
    preguntas = {}
    try:
        with open('preguntados_/preguntas.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if len(fila) != 7:
                    print(f"Fila ignorada (incorrecta o incompleta): {fila}")
                    continue
                categoria = fila[0]
                pregunta = fila[1]
                respuestas = fila[2:6]
                respuesta_correcta = int(fila[6]) - 1  # Restamos 1 porque en CSV las respuestas comienzan en 1
                if categoria not in preguntas:
                    preguntas[categoria] = []
                preguntas[categoria].append((pregunta, respuestas, respuesta_correcta))
                print(f"Categoría: {categoria}, Pregunta: {pregunta}")  # Agregar depuración aquí
    except Exception as e:
        print(f"Error al cargar el archivo de preguntas: {e}")

    if not preguntas:
        print("No hay preguntas disponibles en el archivo.")
    return preguntas

# Función para mostrar las categorías y seleccionar una
def mostrar_categorias(categorias, pantalla):
    corriendo = True
    categoria_seleccionada = None

    while corriendo:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, categoria in enumerate(categorias):
                    if boton_presionado(300, 150 + i * 70, 200, 50, mouse_x, mouse_y):
                        categoria_seleccionada = categoria
                        print(f"Categoría seleccionada: {categoria_seleccionada}")  # Mostrar en consola
                        corriendo = False
                        break

        pantalla.fill(BLANCO)  # Limpiar la pantalla antes de redibujar

        # Cambiar el fondo según la categoría seleccionada
        if categoria_seleccionada:
            if categoria_seleccionada in fondos_categoria:
                pantalla.blit(fondos_categoria[categoria_seleccionada], (0, 0))

        for i, categoria in enumerate(categorias):
            dibujar_boton(categoria, 300, 150 + i * 70, 200, 50, pantalla=pantalla)  # Asegúrate de pasar pantalla

        pygame.display.update()

    return categoria_seleccionada

# Función para mostrar una pregunta
def mostrar_pregunta(categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas, pantalla):
    if categoria not in preguntas or not preguntas[categoria]:
        print("No hay preguntas disponibles para esta categoría.")
        return puntuacion, vidas, respuestas_correctas_consecutivas
    
    pregunta, respuestas, respuesta_correcta = random.choice(preguntas[categoria])

    corriendo_pregunta = True
    while corriendo_pregunta:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo_pregunta = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, (respuesta, y) in enumerate(zip(respuestas, [150, 220, 290, 360])): 
                    if boton_presionado(300, y, 200, 50, mouse_x, mouse_y):
                        if i == respuesta_correcta:
                            puntuacion += 10
                            respuestas_correctas_consecutivas += 1
                            print("¡Respuesta correcta!")
                            if respuestas_correctas_consecutivas == 5:
                                vidas += 1
                                print("¡Ganaste una vida extra!")
                        else:
                            puntuacion -= 5
                            vidas -= 1
                            respuestas_correctas_consecutivas = 0
                            print("Respuesta incorrecta.")
                        
                        if vidas <= 0:
                            print("¡Te has quedado sin vidas!")
                            corriendo_pregunta = False
                            return puntuacion, vidas, respuestas_correctas_consecutivas

                        corriendo_pregunta = False 

        font = pygame.font.SysFont("Arial", 30)
        texto = font.render(pregunta, True, NEGRO)
        pantalla.blit(texto, (65, 40)) 

        for i, respuesta in enumerate(respuestas):
            dibujar_boton(respuesta, 300, 150 + i * 70, 200, 50, pantalla=pantalla)

        font_puntuacion = pygame.font.SysFont("Arial", 20)
        texto_puntuacion = font_puntuacion.render(f"Puntuación: {puntuacion}", True, BLANCO)
        texto_vidas = font_puntuacion.render(f"Vidas: {vidas}", True, BLANCO)

        pantalla.blit(texto_puntuacion, (10, 10))  
        pantalla.blit(texto_vidas, (650, 10))  

        pygame.display.update()

    return puntuacion, vidas, respuestas_correctas_consecutivas

# Función para mostrar el mensaje de "Perdiste"
def mostrar_mensaje_perdido(pantalla):
    font = pygame.font.SysFont("Arial", 50)
    texto = font.render("¡Perdiste!", True, NEGRO)
    pantalla.blit(texto, (300, 250))  # Centrar el mensaje
    pygame.display.update()

    # Esperar un momento antes de salir
    pygame.time.delay(2000)  # 2 segundos

# Función para mostrar el menú principal
def menu_principal(vidas, pantalla):
    corriendo = True
    while corriendo:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_presionado(300, 500, 200, 50, mouse_x, mouse_y):
                    print("¡Botón Jugar presionado!")
                    return True 

        pantalla.blit(fondo, (0, 0))

        hover = boton_presionado(300, 500, 200, 50, mouse_x, mouse_y)
        dibujar_boton("Jugar", 300, 500, 200, 50, hover, pantalla=pantalla)

        # Mostrar las vidas en el menú principal
        font = pygame.font.SysFont("Arial", 30)
        texto_vidas = font.render(f"Vidas: {vidas}", True, BLANCO)
        pantalla.blit(texto_vidas, (650, 10))  # Mostrar vidas en la parte superior derecha

        pygame.display.update()

    pygame.quit()

# Función principal para el juego
def main():
    pygame.init()

    # Configuración de la ventana
    pantalla = pygame.display.set_mode((800, 600))

    puntuacion = 0
    vidas = 3
    respuestas_correctas_consecutivas = 0

    preguntas = cargar_preguntas()

    if preguntas:
        while True:
            if menu_principal(vidas, pantalla):  # Pasamos la pantalla a la función del menú principal
                categorias = list(preguntas.keys())
                categoria = mostrar_categorias(categorias, pantalla)
                puntuacion, vidas, respuestas_correctas_consecutivas = mostrar_pregunta(
                    categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas, pantalla
                )

                # Si las vidas son 0, mostrar mensaje de "Perdiste"
                if vidas <= 0:
                    mostrar_mensaje_perdido(pantalla)
                    break  # Salir del bucle si el jugador ha perdido
    else:
        print("No hay preguntas disponibles en el archivo.")

    pygame.quit()

# Iniciar el juego
if __name__ == "__main__":
    main()
