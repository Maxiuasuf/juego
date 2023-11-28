from final_andando import *
import pygame


#nivel 1                
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador= pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()   
grupo_explosiones = pygame.sprite.Group()  
grupo_estrella = pygame.sprite.Group() 

def nivel_uno():
    for x in range(10):
                enemigo = nave_enemiga(random.randint(0,ANCHO_VENTANA),0)
                grupo_enemigos.add(enemigo)
                grupo_jugador.add(enemigo)