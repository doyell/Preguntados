import pygame
import os

# Constantes de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración de la ventana
VENTANA = (800, 600)

# Cargar imágenes
fondo = pygame.image.load("Preguntados/fondoprincipal.jpg")
fondo = pygame.transform.scale(fondo, (800, 600))
fondo_final = fondo
fondo_final = pygame.transform.scale(fondo_final, (800, 600))
imagen_boton = pygame.image.load("Preguntados/boton1.jpg")  # Imagen de botones
imagen_boton_hover = pygame.image.load("Preguntados/boton2.jpg")  # Imagen de botones cuando pasas el mouse
imagen_boton = pygame.transform.scale(imagen_boton, (200, 50))
imagen_boton_hover = pygame.transform.scale(imagen_boton_hover, (200, 50))

# Comprobar si los archivos existen antes de intentar cargarlos
def cargar_imagen(categoria):
    archivo = f"Preguntados/{categoria}.jpg"
    if os.path.exists(archivo):
        return pygame.image.load(archivo)
    else:
        print(f"Error: El archivo {archivo} no se encuentra.")
        return None

# Diccionario con las imágenes de las categorías
fondos_categoria = {
    'Historia': cargar_imagen('HISTORIA'),
    'Matematica': cargar_imagen('MATEMATICA'),
    'Entretenimiento': cargar_imagen('ENTRETENIMIENTO'),
    'Deportes': cargar_imagen('DEPORTES'),
}

# Verificar si alguna categoría falló al cargar
for categoria, imagen in fondos_categoria.items():
    if imagen is None:
        print(f"Error al cargar la imagen de la categoría: {categoria}")
