import pygame ,sys
import random
from pygame.locals import  QUIT
import re
import sqlite3
from musica_sonidos import *
from colores import *
from objetos import *
from funciones import *
from fondos import  *
from funciones import pantalla_inicial,pantalla_game_over,nombre_en_menu,pantalla_victoria

pygame.init()
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))


DURACION_NIVEL = 25
tiempo_inicial = None
cronometro_iniciado = False
run = True
fps = 80
Reloj = pygame.time.Clock()
score = 0
vida = 100

player = Jugador()
grupo_balas_jugador.add(player)
grupo_jugador.add(player)
pantalla_inicial(ventana_ppal)


player_name = nombre_en_menu(ventana_ppal)
pantalla_nivel(ventana_ppal, 1, "Tu misión es eliminar la estrella de la muerte! Ten mucho cuidado")
nivel_actual = 1
primer_nivel =True
segundo_nivel = False
tercer_nivel = False

tiempo_inicial = pygame.time.get_ticks()

def gestionar_colisiones_jugador():
    # Choque entre meteoros y jugador
    choque_entre_meteoro_y_nave = pygame.sprite.spritecollide(player, grupo_meteoros, True)
    for choque in choque_entre_meteoro_y_nave:
        player.vidas -= 30
        sonido_colision.play()
        piedras = Meteoros(random.randint(0, ANCHO_VENTANA), 0)
        grupo_jugador.add(piedras)
        grupo_meteoros.add(piedras)
        explo_meteorito = Explosion(choque.rect.center, (10, 10))
        grupo_jugador.add(explo_meteorito)

        if player.vidas <= 0:
            explo_meteorito = Explosion(choque.rect.center, (10, 10))
            grupo_jugador.add(explo_meteorito)
            run = False
            gestionar_puntuacion(player_name, score)
            pantalla_game_over(score)

    # Choque entre naves y jugador
    choque_entre_naves = pygame.sprite.spritecollide(player, grupo_enemigos, True)
    for choque in choque_entre_naves:
        explo_3 = Explosion(choque.rect.center, (10, 10))
        grupo_jugador.add(explo_3)
        player.vidas -= 30
        sonido_colision.play()
        enemigos = nave_enemiga(10, 10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)

        if player.vidas <= 0:
            explo_3 = Explosion(choque.rect.center, (10, 10))
            grupo_jugador.add(explo_3)
            run = False
            gestionar_puntuacion(player_name, score)
            pantalla_game_over(score)

    # Laser de nave enemiga a jugador
    laser_nave_enemiga_a_rebelde = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for j in laser_nave_enemiga_a_rebelde:
        player.vidas -= 20
        explo_1 = Explosion(j.rect.center, (10, 10))
        grupo_jugador.add(explo_1)

        if player.vidas <= 0:
            run = False
            gestionar_puntuacion(player_name, score)
            pantalla_game_over(score)


def gestionar_colisiones_rebeldes():
    # Laser de rebelde a naves enemigas
    laser_rebelde_a_enemigos = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
    for i in laser_rebelde_a_enemigos:
        gestionar_puntuacion(score, 100)
        enemigo.disparos_enemigos()
        enemigo = nave_enemiga(300, 10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center, (10, 10))
        grupo_jugador.add(explo)
        sonido_explosion.play()

    # Laser rebelde a meteoritos
    laser_rebelde_a_meteoritos = pygame.sprite.groupcollide(grupo_meteoros, grupo_balas_jugador, True, True)
    for i in laser_rebelde_a_meteoritos:
        gestionar_puntuacion(score, 100)

        piedras = Meteoros(random.randint(0, ANCHO_VENTANA), 0)
        grupo_meteoros.add(piedras)
        grupo_jugador.add(piedras)

        explo_meteorito = Explosion(i.rect.center, (10, 10))
        grupo_jugador.add(explo_meteorito)

        explo = Explosion(i.rect.center, (10, 10))
        grupo_jugador.add(explo)
        sonido_explosion.play()

    # Laser rebelde a estrella
    laser_rebelde_a_estrella = pygame.sprite.groupcollide(grupo_estrella, grupo_balas_jugador, False, True)
    for estrella, balas in laser_rebelde_a_estrella.items():
        for bala in balas:
            gestionar_puntuacion(score, 300)
            estrella.vidas -= 50

            explo_estrella = Explosion(bala.rect.center, (100, 100))
            grupo_jugador.add(explo_estrella)
            sonido_explosion.play()

            if estrella.vidas <= 0:
                run = False
                gestionar_puntuacion(player_name, score)
                pantalla_victoria(player_name, score)


def gestionar_colisiones_hiper_rayo():
    # Hiper rayo estrella de la muerte a rebelde
    hiperrayo_a_rebelde = pygame.sprite.spritecollide(player, grupo_balas_estrella, True)
    for i in hiperrayo_a_rebelde:
        player.vidas -= 50

        explo = Explosion(i.rect.center, (10, 10))
        grupo_jugador.add(explo)

        if player.vidas <= 0:
            run = False
            gestionar_puntuacion(player_name, score)
            pantalla_game_over(score)


def gestionar_colisiones_monedas():
    # Moneda con rebelde
    colisiones_monedas = pygame.sprite.spritecollide(player, grupo_monedas, True)
    for moneda in colisiones_monedas:
        if player.vidas < 100:
            incremento_vidas = min(20, 100 - player.vidas)
            player.vidas += incremento_vidas
            burbuja_moneda = Burbuja(moneda.rect.center, (20, 20))
            grupo_jugador.add(burbuja_moneda)
            sonido_energia.play()

        nueva_moneda_vida = Moneda(random.randint(0, ANCHO_VENTANA), 0)
        grupo_monedas.add(nueva_moneda_vida)
        grupo_jugador.add(nueva_moneda_vida)


def gestionar_puntuacion(nombre, puntuacion):
    conn = sqlite3.connect("puntuacion.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO puntuacion (nombre, score) VALUES (?, ?)", (nombre, puntuacion))
    conn.commit()
    conn.close()
