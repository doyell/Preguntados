import pygame

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

fondos_categoria = {
    'Geografía': pygame.image.load("Preguntados/GEOGRAFIA.jpg"),
    'Historia': pygame.image.load("Preguntados/HISTORIA.jpg"),
    'Matemática': pygame.image.load("Preguntados/MATEMATICA.jpg"),
    'Entretenimiento': pygame.image.load("Preguntados/ENTRETENIMIENTO.jpg"),
    'Deportes': pygame.image.load("Preguntados/DEPORTES.jpg"),
    
}
