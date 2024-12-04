import pygame
from funciones_1 import cargar_preguntas, menu_principal, mostrar_pregunta, mostrar_mensaje_perdido , mostrar_categorias

def main():
    pygame.init()  # Asegúrate de inicializar pygame correctamente

    # Configuración de la ventana
    pantalla = pygame.display.set_mode((800, 600))

    puntuacion = 0
    vidas = 3
    respuestas_correctas_consecutivas = 0

    preguntas = cargar_preguntas()

    if preguntas:
        while True:
            if menu_principal(vidas, pantalla):  # Pasamos las vidas a la función del menú principal
                categorias = list(preguntas.keys())
                categoria = mostrar_categorias(categorias, pantalla)
                puntuacion, vidas, respuestas_correctas_consecutivas = mostrar_pregunta(
                    categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas, pantalla
                )

                # Si las vidas son 0, mostrar mensaje de "Perdiste"
                if vidas <= 0:
                    mostrar_mensaje_perdido()
                    break  # Salir del bucle si el jugador ha perdido
    else:
        print("No hay preguntas disponibles en el archivo.")

    pygame.quit()  # Al finalizar, cerramos pygame

# Iniciar el juego
if __name__ == "__main__":
    main()
