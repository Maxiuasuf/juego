import pygame
from final_andando import *

 ########################### COLISIONES #######################################
def colisiones():
    choque_entre_naves = pygame.sprite.spritecollide(player,grupo_enemigos,True)
    for choque in choque_entre_naves:
        explo_3 = Explosion(choque.rect.center)
        grupo_jugador.add(explo_3)
        player.vidas   -= 30
        sonido_colision.play()
        enemigos = nave_enemiga(10,10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vidas <=0:
            explo_3 = Explosion(choque.rect.center)
            grupo_jugador.add(explo_3)
            time.sleep(0.2)
            pantalla_game_over()
            run = False

    laser_rebelde_a_enemigos = pygame.sprite.groupcollide(grupo_enemigos,grupo_balas_jugador,True,True)
    for i in laser_rebelde_a_enemigos:
        score+=100
        enemigo.disparos_enemigos()
        enemigo = nave_enemiga(300,10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        sonido_explosion.play()
    

    laser_nave_enemiga_a_rebelde = pygame.sprite.spritecollide(player,grupo_balas_enemigos,True)
    for j in laser_nave_enemiga_a_rebelde:
        player.vidas -= 20
        explo_1 = Explosion(j.rect.center)
        grupo_jugador.add(explo_1)
        if player.vidas <=0:
            run = False
            pantalla_game_over()
            
            
            
#nivel 2
'''
grupo_jugador_nivel_dos = pygame.sprite.Group()
grupo_enemigos_nivel_dos = pygame.sprite.Group()
grupo_balas_jugador_nivel_dos = pygame.sprite.Group()


grupo_jugador_nivel_tres = pygame.sprite.Group()
grupo_enemigos_nivel_tres = pygame.sprite.Group()
grupo_balas_jugador_nivel_tres =pygame.sprite.Group()

grupo_balas_enemigos_nivel_dos = pygame.sprite.Group()
grupo_balas_enemigos_nivel_tres = pygame.sprite.Group()