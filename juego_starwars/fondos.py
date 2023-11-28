
import pygame
from colores import *
import moviepy.editor 

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720
PANTALLA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
fondo = pygame.image.load("tp_video_juego.py/imagenes.py/eclipse.jpg").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

fondo_nivel_dos = pygame.image.load("tp_video_juego.py/imagenes.py/space-1.png").convert()
fondo_nivel_dos = pygame.transform.scale(fondo_nivel_dos, (ANCHO_VENTANA, ALTO_VENTANA))

fondo_nivel_tres = pygame.image.load("tp_video_juego.py\imagenes.py\ojorojo.jpg").convert()
fondo_nivel_tres = pygame.transform.scale(fondo_nivel_tres, (ANCHO_VENTANA, ALTO_VENTANA))

pygame.init()

fuente_pausa = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 60)
mensaje_pausa = fuente_pausa.render("pausa", True, blanco)

# Cargar la imagen del icono
icono = pygame.image.load("tp_video_juego.py/imagenes.py/xwing.png")

# Establecer el icono de la ventana
pygame.display.set_icon(icono)

ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("   STAR WARS   ")

video = moviepy.editor.VideoFileClip("tp_video_juego.py/imagenes.py/tamaño.mp4")

x = 0
y = 0
