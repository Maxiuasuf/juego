import re
import pygame
import colores 

def crear(x,y,ancho,alto):
    dict_personaje = {}
    dict_personaje["surface"] = pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/xwing.png")
    dict_personaje["surface"] = pygame.transform.scale(dict_personaje["surface"],(ancho,alto))
    dict_personaje["rect_nave_rebelde"] = pygame.Rect(x,y,ancho,alto)
    dict_personaje["rect_boca"] = pygame.Rect((x+ancho/2)-10,y+90,40,20)
    dict_personaje["score"] = 0
    return dict_personaje

def actualizar_pantalla(personaje,ventana_ppal):
    ventana_ppal.blit(personaje["surface"],personaje["rect_nave_rebelde"])
    #pygame.draw.rect(ventana_ppal,colores.ROJO,personaje["rect_homero"])
    #pygame.draw.rect(ventana_ppal,colores.AZUL,personaje["rect_boca"])

def update(personaje,incremento_x):
    nueva_x = personaje["rect_nave_rebelde"].x + incremento_x
    if(nueva_x > 0 and nueva_x < 600):
        personaje["rect_nave_rebelde"].x = personaje["rect_nave_rebelde"].x + incremento_x
        personaje["rect_boca"].x = personaje["rect_boca"].x + incremento_x

