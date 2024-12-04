# main.py

import pygame
from constantes import *
from funciones import menu_principal, mostrar_categorias, mostrar_pregunta, cargar_preguntas, mostrar_mensaje, guardar_partida, mostrar_ranking, obtener_nombre, mostrar_puntaje,activar_comodin


# Inicialización de pygame
pygame.init()


# Configuración de la ventana
pantalla = pygame.display.set_mode(VENTANA)
pygame.display.set_caption("Preguntados")
icono = pygame.image.load("Preguntados/icono.png") 
pygame.display.set_icon(icono)


# Función principal
def main():
    global puntuacion, vidas, respuestas_correctas_consecutivas, comodin_disponible
    puntuacion = 10  # Valor inicial de 10 puntos
    vidas = 3
    respuestas_correctas_consecutivas = 0
    comodin_disponible = False  # El comodín no está disponible al principio

    preguntas = cargar_preguntas()
    if preguntas:
        while True:
            if menu_principal(vidas, puntuacion):  # Pasamos las vidas a la función del menú principal
                categorias = list(preguntas.keys())
                categoria = mostrar_categorias(categorias)
                puntuacion, vidas, respuestas_correctas_consecutivas, comodin_disponible = mostrar_pregunta(
    categoria, preguntas, puntuacion, vidas, respuestas_correctas_consecutivas, comodin_disponible
)


                # Activamos el comodín si es necesario
                puntuacion, comodin_disponible = activar_comodin(puntuacion, respuestas_correctas_consecutivas, comodin_disponible)


                # Mostrar puntaje actualizado en la interfaz
                mostrar_puntaje(pantalla, puntuacion)

            if vidas <= 0:
                mostrar_mensaje("Perdiste", (255, 0, 0))

                # Solo pedir el nombre si aún no ha sido solicitado
                if 'nombre_jugador' not in globals():  # Verificamos si el nombre ya fue pedido
                    nombre_jugador = obtener_nombre()  # Asegúrate de tener una función que obtenga el nombre del jugador
                    globals()['nombre_jugador'] = nombre_jugador  # Guardamos el nombre en una variable global

                # Guardar puntaje al finalizar la partida
                guardar_partida(nombre_jugador, puntuacion)

                # Mostrar el ranking después de la partida
                mostrar_ranking()

                break  # Salir del juego cuando el jugador pierde
    else:
        print("No hay preguntas disponibles en el archivo.")

    pygame.quit()

if __name__ == "__main__":
    main()


