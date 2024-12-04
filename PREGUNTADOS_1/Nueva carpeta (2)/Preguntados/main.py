import pygame
from constantes_1 import VENTANA
from funciones_1 import menu_principal, mostrar_categorias, mostrar_pregunta, cargar_preguntas,mostrar_mensaje


# Inicialización de pygame
pygame.init()


# Configuración de la ventana
pantalla = pygame.display.set_mode(VENTANA)


# Función principal
def main():
    global puntuacion, vidas, respuestas_correctas_consecutivas
    puntuacion = 0
    vidas = 3
    respuestas_correctas_consecutivas = 0

    preguntas = cargar_preguntas('Preguntados/preguntados.csv')
    if preguntas:
        while True:
            if menu_principal(vidas,puntuacion):  # Pasamos las vidas a la función del menú principal
                categorias = list(preguntas.keys())
                categoria = mostrar_categorias(categorias)
                puntuacion, vidas, respuestas_correctas_consecutivas = mostrar_pregunta(
                    categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas
                )
            if vidas <= 0:
                mostrar_mensaje("Perdiste", (255,0,0))
                break
    else:
        print("No hay preguntas disponibles en el archivo.")

    pygame.quit()


if __name__ == "__main__":
    main()
