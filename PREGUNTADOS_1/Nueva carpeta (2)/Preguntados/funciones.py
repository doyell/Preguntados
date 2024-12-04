#FUNCIONES.PY

import pygame
import random
import csv
from constantes import fondo, imagen_boton, imagen_boton_hover, fondos_categoria, BLANCO, fondo_final, NEGRO, VENTANA
import json
from datetime import datetime
import os
nombre_jugador =None


def dibujar_boton(texto, x, y, ancho, alto):

    """Dibuja un botón con el texto proporcionado en las coordenadas (x, y)."""
    pantalla = pygame.display.set_mode((800, 600))
    fuente = pygame.font.SysFont("Arial", 30)
    pygame.draw.rect(pantalla, NEGRO, (x, y, ancho, alto))
    texto_boton = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_boton, (x + 10, y + 10))

def boton_presionado(x, y, ancho, alto, mouse_x, mouse_y):
    """Verifica si el clic del ratón está dentro de los límites de un botón."""
    return x <= mouse_x <= x + ancho and y <= mouse_y <= y + alto

def dibujar_comodin(comodin_disponible):
    """Dibuja el botón de comodín si está disponible."""
    if comodin_disponible:
        dibujar_boton("Comodín", 650, 550, 130, 40)

def usar_comodin(comodin_disponible):
    """Usa el comodín si está disponible."""
    if comodin_disponible:
        print("¡Comodín activado!")
        comodin_disponible = False
    return comodin_disponible




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
                        nombre += chr(tecla).lower()  # Añadir letra al nombre (en minúscula)

                # Verificar teclas de números
                for tecla in range(pygame.K_0, pygame.K_9 + 1):  # Desde '0' hasta '9'
                    if teclas_presionadas[tecla]:
                        nombre += chr(tecla)  # Añadir número al nombre

                # Tecla de retroceso para borrar
                if evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]

                # Tecla Enter para finalizar el ingreso
                if evento.key == pygame.K_RETURN and nombre != "":
                    active = False  # Terminar el proceso una vez el nombre esté ingresado

        pygame.display.update()

    return nombre


def guardar_partida(nombre_jugador, puntuacion):
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear un diccionario con los datos a guardar
    partida = {
        "nombre": nombre_jugador,
        "puntaje": puntuacion,
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



def mostrar_pregunta(categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas, comodin_disponible):
    corriendo_pregunta = True
    while corriendo_pregunta and vidas > 0:
        # Elegir una pregunta aleatoria
        pregunta, respuestas, respuesta_correcta = random.choice(preguntas)
        corriendo_pregunta = True

    global nombre_jugador  # Asegurarse de que se utilice la variable global

    if categoria not in preguntas or not preguntas[categoria]:
        print("No hay preguntas disponibles para esta categoría.")
        return puntuacion, vidas, respuestas_correctas_consecutivas

    pantalla = pygame.display.get_surface()
    fondo_categoria = fondos_categoria.get(categoria)
    if fondo_categoria:
        fondo_categoria = pygame.transform.scale(fondo_categoria, (800, 600))
        pantalla.blit(fondo_categoria, (0, 0))
    pygame.display.update()

    preguntas_restantes = preguntas[categoria][:]

    while preguntas_restantes and vidas > 0:
        pregunta, respuestas, respuesta_correcta = random.choice(preguntas_restantes)
        preguntas_restantes.remove((pregunta, respuestas, respuesta_correcta))

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
                                
                                


                                # Extra: Si el jugador alcanza 5 respuestas consecutivas correctas, obtiene una vida extra
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
                                corriendo_pregunta = False

                            if vidas <= 0:
                                print("¡Te has quedado sin vidas!")
                                # Pedimos el nombre solo una vez al perder
                                if nombre_jugador is None:
                                    nombre_jugador = obtener_nombre()
                                    guardar_partida(nombre_jugador, puntuacion)
                                corriendo_pregunta = False

                        if not preguntas_restantes:
                            print(f"No hay más preguntas disponibles en la categoría {categoria}.")
                            corriendo_pregunta = False
                            return puntuacion, vidas, respuestas_correctas_consecutivas

            # Mostrar pregunta y respuestas
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

        return puntuacion, vidas, respuestas_correctas_consecutivas, comodin_disponible







def mostrar_mensaje(mensaje, color):
    fuente = pygame.font.SysFont("Arial", 50)
    texto_superficie = fuente.render(mensaje, True, color)
    pantalla = pygame.display.get_surface()
    pantalla.blit(texto_superficie, (VENTANA[0] // 2 - texto_superficie.get_width() // 2, VENTANA[1] // 2 - texto_superficie.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(1000)  # Muestra el mensaje por 1 segundo

    # Esperar 2 segundos o hasta que el jugador presione cualquier tecla
    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperar = False
            if evento.type == pygame.KEYDOWN:  # Esperar que el jugador presione cualquier tecla
                esperar = False
        pygame.time.Clock().tick(30)  # Limitar la tasa de refresco


# Función para guardar el puntaje en un archivo
def guardar_partida(nombre_jugador, puntuacion):
    # Obtener la hora y fecha actual
    tiempo_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Crear un diccionario con los datos de la partida
    datos_partida = {
        'nombre': nombre_jugador,
        'puntuacion': puntuacion,
        'hora': tiempo_actual
    }
    
    # Intentamos cargar el ranking existente, si no existe, creamos uno nuevo
    try:
        with open('ranking.json', 'r') as archivo:
            ranking = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        ranking = []
    
    # Agregar la nueva partida al ranking
    ranking.append(datos_partida)
    
    # Ordenar el ranking por puntuación (de mayor a menor)
    ranking.sort(key=lambda x: x['puntuacion'], reverse=True)
    
    # Guardar solo los primeros 10 resultados
    ranking = ranking[:10]
    
    # Guardar el ranking actualizado en el archivo JSON
    with open('ranking.json', 'w') as archivo:
        json.dump(ranking, archivo, indent=4)

def mostrar_ranking():
    # Intentamos cargar el ranking desde el archivo
    try:
        with open('ranking.json', 'r') as archivo:
            ranking = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay ranking disponible.")
        return

    # Mostrar el ranking
    print("Top 10 Mejores Puntajes:")
    for i, entrada in enumerate(ranking):
        print(f"{i + 1}. {entrada['nombre']} - {entrada['puntuacion']} puntos - {entrada['hora']}")

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
def mostrar_puntaje(pantalla, puntuacion):
    fuente = pygame.font.SysFont("Arial", 30)
    texto_puntaje = fuente.render(f"Puntaje: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto_puntaje, (10, 10))  # Esto se dibuja en la parte superior izquierda

# Función para mostrar el menú principal
def menu_principal(vidas, puntuacion):
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

        pantalla = pygame.display.get_surface()
        pantalla.blit(fondo, (0, 0))

        hover = boton_presionado(300, 500, 200, 50, mouse_x, mouse_y)
        dibujar_boton("Jugar", 300, 500, 200, 50, hover)

        # Mostrar las vidas y el puntaje en el menú principal
        font = pygame.font.SysFont("Arial", 30)
        texto_vidas = font.render(f"Vidas: {vidas}", True, BLANCO)
        texto_puntuacion = font.render(f"Puntuación: {puntuacion}", True, BLANCO)

        pantalla.blit(texto_vidas, (650, 10))  # Mostrar vidas en la parte superior derecha
        pantalla.blit(texto_puntuacion, (10, 40))  # Mostrar puntuación justo debajo de las vidas

        pygame.display.update()

    pygame.quit()
