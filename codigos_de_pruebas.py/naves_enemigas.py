import pygame
import colores
import random

def crear(x,y,ancho,alto):
    # Leer una imagen
    imagen_dona = pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tie figther.png")
    imagen_dona = pygame.transform.scale(imagen_dona,(ancho,alto))
    rect_dona = imagen_dona.get_rect()
    rect_dona.x = x
    rect_dona.y = y
    dict_dona = {}
    dict_dona["surface"] = imagen_dona
    dict_dona["rect"] = rect_dona
    dict_dona["visible"] = True
    dict_dona["speed"] = random.randrange (10,20,1)
    return dict_dona

def update(lista_donas):
    for dona in lista_donas:
        rect_dona = dona["rect"]
        rect_dona.y = rect_dona.y + dona["speed"]


def actualizar_pantalla(lista_naves_enemigas,personaje,ventana_ppal):
    for dona in lista_naves_enemigas:
        if(personaje["rect_boca"].colliderect(dona["rect"])):
            personaje["score"] = personaje["score"] + 1
            restar_dona(dona)
        
        if(dona["rect"].y > 800):
            restar_dona(dona)
        ventana_ppal.blit(dona["surface"],dona["rect"])
        #pygame.draw.rect(ventana_ppal,colores.ROJO,dona["rect"])

    font = pygame.font.SysFont("Courier new", 50, False, True)
    text = font.render("Score: {0}".format(personaje["score"]), True, colores.NEGRO)
    ventana_ppal.blit(text,(0,0))

def crear_lista_naves_enemigas(cantidad):
    crear_lista_naves_enemigas = []
    for i in range(cantidad):
        y = random.randrange (-1000,0,60)        
        x = random.randrange (0,740,60)
        crear_lista_naves_enemigas.append(crear(x,y,60,60))
    return crear_lista_naves_enemigas

def restar_dona(dona):
    dona["rect"].x = random.randrange (0,740,60)
    dona["rect"].y = random.randrange (-1000,0,60)    
