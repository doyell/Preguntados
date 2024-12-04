import pygame
import random
import csv
from constantes_1 import fondo, imagen_boton, imagen_boton_hover, fondos_categoria, BLANCO, fondo_final, NEGRO, VENTANA
import json
import datetime
import os

# Función para dibujar un botón con una imagen
def dibujar_boton(texto, x, y, ancho, alto, hover=False):
    imagen = imagen_boton_hover if hover else imagen_boton
    pantalla = pygame.display.get_surface()
    pantalla.blit(imagen, (x, y))  
    font = pygame.font.SysFont("Arial", 30)
    texto_superficie = font.render(texto, True, BLANCO)
    pantalla.blit(texto_superficie, (x + (ancho - texto_superficie.get_width()) // 2, y + (alto - texto_superficie.get_height()) // 2))

# Función para detectar si el botón fue presionado
def boton_presionado(x, y, ancho, alto, mouse_x, mouse_y):
    return x < mouse_x < x + ancho and y < mouse_y < y + alto




# Función para obtener y validar el nombre del jugador
def obtener_nombre():
    nombre = ""
    fuente = pygame.font.SysFont("Arial", 40)
    input_rect = pygame.Rect(200, 300, 400, 50)  # Área para el nombre
    pantalla = pygame.display.set_mode((800, 600))  # Suponiendo que la ventana es de 800x600
    pygame.display.set_caption("Preguntados - Fin del Juego")
    active = True

    while active:
        pantalla.blit(fondo_final, (0, 0))  # Aplicar el fondo

        # Mostrar texto "Ingrese su nombre"
        texto_instruccion = fuente.render("Ingrese su nombre:", True, BLANCO)
        pantalla.blit(texto_instruccion, (250, 150))

        # Mostrar el nombre ingresado hasta ahora
        texto_nombre = fuente.render(nombre, True, BLANCO)
        pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 10))

        # Dibujar el rectángulo donde se escribirá el nombre
        pygame.draw.rect(pantalla, BLANCO, input_rect, 2)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                active = False

            # Detectar teclas presionadas
            if evento.type == pygame.KEYDOWN:
                teclas_presionadas = pygame.key.get_pressed()  # Obtiene todas las teclas presionadas

                # Verificar si alguna tecla del alfabeto o números es presionada
                for tecla in range(pygame.K_a, pygame.K_z + 1):  # Desde 'a' hasta 'z'
                    if teclas_presionadas[tecla]:
                        nombre += chr(tecla)  # Añadir letra al nombre

                # Verificar teclas de números
                for tecla in range(pygame.K_0, pygame.K_9 + 1):  # Desde '0' hasta '9'
                    if teclas_presionadas[tecla]:
                        nombre += chr(tecla)

                # Verificar la tecla 'Backspace' para eliminar el último carácter
                if teclas_presionadas[pygame.K_BACKSPACE] and len(nombre) > 0:
                    nombre = nombre[:-1]

                # Verificar la tecla 'Enter' para finalizar la entrada de nombre
                if teclas_presionadas[pygame.K_RETURN] and nombre:  # Al presionar Enter, terminar
                    return nombre

        pygame.display.update()


# Función para guardar los datos de la partida en un archivo JSON
# Función para guardar los datos de la partida en un archivo JSON
def guardar_partida(nombre_jugador, puntaje):
    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear un diccionario con los datos a guardar
    partida = {
        "nombre": nombre_jugador,
        "puntaje": puntaje,
        "fecha": fecha_actual
    }

    # Verificar si el archivo 'partidas.json' existe
    if os.path.exists('Preguntados/partidas.json'):
        # Si el archivo existe, lo abrimos en modo lectura
        try:
            with open('Preguntados/partidas.json', 'r') as archivo:
                partidas = json.load(archivo)
        except json.JSONDecodeError:
            # Si el archivo está vacío o tiene un error de formato JSON, inicializamos partidas como una lista vacía
            partidas = []
    else:
        # Si el archivo no existe, inicializamos la lista de partidas
        partidas = []

    # Agregar la nueva partida a la lista
    partidas.append(partida)

    # Guardar la lista actualizada en el archivo 'partidas.json'
    with open('partidas.json', 'w') as archivo:
        json.dump(partidas, archivo, indent=4)























# Función para cargar preguntas desde un archivo CSV
def cargar_preguntas():
    preguntas = {}
    try:
        with open('Preguntados/preguntas.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if len(fila) != 7:
                    print(f"Fila ignorada (incorrecta o incompleta): {fila}")
                    continue
                categoria = fila[0]
                pregunta = fila[1]
                respuestas = fila[2:6]
                respuesta_correcta = int(fila[6]) - 1
                if categoria not in preguntas:
                    preguntas[categoria] = []
                preguntas[categoria].append((pregunta, respuestas, respuesta_correcta))
    except Exception as e:
        print(f"Error al cargar el archivo de preguntas: {e}")

    if not preguntas:
        print("No hay preguntas disponibles en el archivo.")
        print(f"Preguntas cargadas: {preguntas}")  # Para verificar las preguntas cargadas
    return preguntas

# Función para mostrar una pregunta
def mostrar_pregunta(categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas):
    if categoria not in preguntas or not preguntas[categoria]:
        print("No hay preguntas disponibles para esta categoría.")
        return puntuacion, vidas, respuestas_correctas_consecutivas
    pantalla = pygame.display.get_surface()
    
    fondo_categoria = fondos_categoria.get(categoria)
    if fondo_categoria:
        fondo_categoria = pygame.transform.scale(fondo_categoria, (800, 600))
        pantalla = pygame.display.get_surface()
        pantalla.blit(fondo_categoria, (0, 0))  
    pygame.display.update()

    # Copiar las preguntas de la categoría para que no se repitan
    preguntas_restantes = preguntas[categoria][:]
    while preguntas_restantes and vidas > 0:
        # Seleccionamos una pregunta aleatoria de las preguntas restantes
        pregunta, respuestas, respuesta_correcta = random.choice(preguntas_restantes)
        preguntas_restantes.remove((pregunta, respuestas, respuesta_correcta))  # Eliminamos la pregunta de las preguntas disponibles

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
                                respuestas_correctas_consecutivas = 0
                                print("¡Ganaste una vida extra!")
                            corriendo_pregunta = False
                                
                        else:
                            puntuacion -= 5
                            vidas -= 1
                            respuestas_correctas_consecutivas = 0
                            print("Respuesta incorrecta.")
                        
                        if vidas <= 0:
                            print("¡Te has quedado sin vidas!")
                            nombre_jugador = obtener_nombre()
                            guardar_partida(nombre_jugador,puntuacion)
                            corriendo_pregunta = False
                            return puntuacion, vidas, respuestas_correctas_consecutivas

                        # Si ya no quedan preguntas en la categoría, muestra un mensaje
                        if not preguntas_restantes:
                            print(f"No hay más preguntas disponibles en la categoría {categoria}.")
                        return puntuacion, vidas, respuestas_correctas_consecutivas

        font = pygame.font.SysFont("Arial", 30)
        texto = font.render(pregunta, True, NEGRO)
        pantalla.blit(texto, (65, 40)) 

        for i, respuesta in enumerate(respuestas):
            dibujar_boton(respuesta, 300, 150 + i * 70, 200, 50)

        font_puntuacion = pygame.font.SysFont("Arial", 20)
        texto_puntuacion = font_puntuacion.render(f"Puntuación: {puntuacion}", True, BLANCO)
        texto_vidas = font_puntuacion.render(f"Vidas: {vidas}", True, BLANCO)

        pantalla.blit(texto_puntuacion, (10, 10))  
        pantalla.blit(texto_vidas, (650, 10))  

        pygame.display.update()

    return puntuacion, vidas, respuestas_correctas_consecutivas


def mostrar_mensaje(mensaje, color):
    fuente = pygame.font.SysFont("Arial", 50)
    texto_superficie = fuente.render(mensaje, True, color)
    pantalla = pygame.display.get_surface()
    pantalla.blit(texto_superficie, (VENTANA[0] // 2 - texto_superficie.get_width() // 2, VENTANA[1] // 2 - texto_superficie.get_height() // 2))
    pygame.display.update()


    # Esperar 2 segundos o hasta que el jugador presione cualquier tecla
    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperar = False
            if evento.type == pygame.KEYDOWN:  # Esperar que el jugador presione cualquier tecla
                esperar = False
        pygame.time.Clock().tick(30)  # Limitar la tasa de refresco

# Función para mostrar las categorías y seleccionar una
def mostrar_categorias(categorias):
    corriendo = True
    while corriendo:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, categoria in enumerate(categorias):
                    if boton_presionado(300, 150 + i * 70, 200, 50, mouse_x, mouse_y):
                        print(f"Categoría seleccionada: {categoria}")
                        return categoria  # Retorna la categoría seleccionada

        pantalla = pygame.display.get_surface()
        pantalla.blit(fondo, (0, 0))  # Dibujar fondo

        for i, categoria in enumerate(categorias):
            dibujar_boton(categoria, 300, 150 + i * 70, 200, 50)

        pygame.display.update()  # Actualizar la pantalla

# Función para mostrar el menú principal
def menu_principal(vidas, puntuacion):
    # Mostrar la pantalla del menú principal
    pantalla.fill(NEGRO)  # Limpiar la pantalla
    pantalla.blit(fondo, (0, 0))  # Fondo del menú
    # Mostrar texto en el menú
    texto_titulo = FUENTE.render("¡Bienvenido a Preguntados!", True, BLANCO)
    texto_puntuacion = FUENTE.render(f"Puntuación: {puntuacion}", True, BLANCO)
    texto_vidas = FUENTE.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_titulo, (VENTANA[0] // 2 - texto_titulo.get_width() // 2, 100))
    pantalla.blit(texto_puntuacion, (VENTANA[0] // 2 - texto_puntuacion.get_width() // 2, 200))
    pantalla.blit(texto_vidas, (VENTANA[0] // 2 - texto_vidas.get_width() // 2, 250))

    # Botón para iniciar el juego
    boton_rect = pygame.Rect(VENTANA[0] // 2 - 100, 350, 200, 50)
    pantalla.blit(imagen_boton, boton_rect)

    pygame.display.update()  # Actualizar la pantalla

    # Gestión de eventos para clics
    continuar = False  # Variable que se usa para determinar si se continúa con el juego
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(evento.pos):  # Si el clic fue dentro del área del botón
                continuar = True  # Cambiamos a True si se hace clic en el botón de continuar

    return continuar
    pygame.display.update()

    pygame.quit()
