
import pygame ,sys
import random
from pygame.locals import  QUIT
import sqlite3
from musica_sonidos import *
from colores import *
from objetos import *
from funciones import *
from fondos import *
from constantes import *

pygame.init()

abrir_base_de_datos()

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

nivel_uno()

while run:
    Reloj.tick(fps)
    cronometro_iniciado = True
    
    movimiento_fondo(fondo)
    if nivel_actual == 2:
        movimiento_fondo(fondo_nivel_dos)
    elif nivel_actual == 3:
        movimiento_fondo(fondo_nivel_tres)
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()
            elif event.key == pygame.K_ESCAPE:
                juego_en_pausa = not juego_en_pausa
            
                
    while juego_en_pausa:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    juego_en_pausa = not juego_en_pausa   
                    
        ventana_ppal.blit(mensaje_pausa, (ANCHO_VENTANA // 2 - mensaje_pausa.get_width() // 2, ALTO_VENTANA // 2 - mensaje_pausa.get_height() // 2))  
        pygame.display.flip()  

    for enemigo in grupo_enemigos:
            if enemigo.rect.top > ALTO_VENTANA:
                enemigo.rect.y = -10
                enemigo.rect.x = random.randint(1, ANCHO_VENTANA - 50)
                
    for monedas in grupo_monedas:
            if monedas.rect.top > ALTO_VENTANA:
                monedas.rect.y = -10
                monedas.rect.x = random.randint(1, ANCHO_VENTANA - 50)
                
    ###################################cronometro################################
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial

    if tiempo_inicial is not None and cronometro_iniciado:
        tiempo_restante = max(0, DURACION_NIVEL - tiempo_transcurrido // 1000)
    
    ########################### COLISIONES #######################################
#CHOQUE ENTRE METEORO Y JUGADOR  
    choque_entre_meteoro_y_nave = pygame.sprite.spritecollide(player,grupo_meteoros,True)
    for choque in choque_entre_meteoro_y_nave:
        player.vidas   -= 30
        sonido_colision.play()
        piedras = Meteoros(random.randint(0, ANCHO_VENTANA), 0)
        grupo_jugador.add(piedras)
        grupo_meteoros.add(piedras)
        explo_meteorito = Explosion(choque.rect.center,(10,10))
        grupo_jugador.add(explo_meteorito)
        
        if player.vidas <=0:
            explo_meteorito = Explosion(choque.rect.center,(10,10))
            grupo_jugador.add(explo_meteorito)
            run = False
            conn = sqlite3.connect("puntuacion.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO puntuacion (nombre, score) VALUES (?, ?)", (player_name, score))
            conn.commit()
            conn.close()
            pantalla_game_over(score)

#CHOQUE ENTRE NAVES
    choque_entre_naves = pygame.sprite.spritecollide(player,grupo_enemigos,True)
    for choque in choque_entre_naves:
        explo_3 = Explosion(choque.rect.center,(10,10))
        grupo_jugador.add(explo_3)
        player.vidas   -= 30
        sonido_colision.play()
        enemigos = nave_enemiga(10,10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vidas <=0:
            explo_3 = Explosion(choque.rect.center,(10,10))
            grupo_jugador.add(explo_3)
            run = False
            conn = sqlite3.connect("puntuacion.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO puntuacion (nombre, score) VALUES (?, ?)", (player_name, score))
            conn.commit()
            conn.close()
            pantalla_game_over(score)
            
#LASER NAVE ENEMIGA A JUGADOR
    laser_nave_enemiga_a_rebelde = pygame.sprite.spritecollide(player,grupo_balas_enemigos,True)
    for j in laser_nave_enemiga_a_rebelde:
        player.vidas -= 20
        explo_1 = Explosion(j.rect.center,(10,10))
        grupo_jugador.add(explo_1)
        if player.vidas <=0:
            run = False
            conn = sqlite3.connect("puntuacion.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO puntuacion (nombre, score) VALUES (?, ?)", (player_name, score))
            conn.commit()
            conn.close()
            pantalla_game_over(score)
            
#LASER REBELDE A NAVES ENEMIGAS
    laser_rebelde_a_enemigos = pygame.sprite.groupcollide(grupo_enemigos,grupo_balas_jugador,True,True)
    for i in laser_rebelde_a_enemigos:
        score+=100
        enemigo.disparos_enemigos()
        enemigo = nave_enemiga(300,10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center,(10,10))
        grupo_jugador.add(explo)
        sonido_explosion.play()
        
#LASER REBELDE A METEORITOS
    laser_rebelde_a_meteoritos = pygame.sprite.groupcollide(grupo_meteoros,grupo_balas_jugador,True,True)
    for i in laser_rebelde_a_meteoritos:
        score+=100
        
        piedras = Meteoros(random.randint(0, ANCHO_VENTANA), 0)
        grupo_meteoros.add(piedras)
        grupo_jugador.add(piedras)

        explo_meteorito = Explosion(i.rect.center,(10,10))
        grupo_jugador.add(explo_meteorito)

        explo = Explosion(i.rect.center,(10,10))
        grupo_jugador.add(explo)
        sonido_explosion.play()
    
#LASER REBELDE A ESTRELLA
    laser_rebelde_a_estrella = pygame.sprite.groupcollide(grupo_estrella,grupo_balas_jugador, False, True)
    for estrella, balas in laser_rebelde_a_estrella.items():
        for bala in balas:
            score += 300
            estrella.vidas -= 50
            
            explo_estrella = Explosion(bala.rect.center,(100,100))
            grupo_jugador.add(explo_estrella)
            sonido_explosion.play()

            if estrella.vidas <= 0:
                run = False
                conn = sqlite3.connect("puntuacion.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO puntuacion (nombre, score) VALUES (?, ?)", (player_name, score))
                conn.commit()
                conn.close()
                video.preview()
                pantalla_victoria(player_name,score)
                
#HIPER RAYO ESTRELLA DE LA MUERTE A REBELDE
    hiperrayo_a_rebelde = pygame.sprite.spritecollide(player, grupo_balas_estrella, True)
    for i in hiperrayo_a_rebelde:
            player.vidas -= 50
            
            explo = Explosion(i.rect.center,(10,10))
            grupo_jugador.add(explo)
            if player.vidas <=0:
                run = False
                conn = sqlite3.connect("puntuacion.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO puntuacion (nombre, score) VALUES (?, ?)", (player_name, score))
                conn.commit()
                conn.close()
                pantalla_game_over(score)
                
                
#MONEDA CON REBELDE 
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
        grupo_jugador.add(nueva_moneda_vida )
            
####################################################################################
#NIVELES:
    if tiempo_restante == 0 and player.vidas >= 1:
        if nivel_actual == 1 and not segundo_nivel:
            # Cambio al NIVEL 2
            nivel_actual += 1
            segundo_nivel = True
            primer_nivel = False
            tercer_nivel = False
            pantalla_nivel(ventana_ppal, 2, "Ya saben que llegamos, cuidado el enemigo abrió fuego!")
            
            tiempo_inicial = pygame.time.get_ticks()
            player.vidas = 100    
            nivel_dos()           
        elif nivel_actual == 2 and not tercer_nivel:
            # Cambio al NIVEL 3
            nivel_actual += 1
            tercer_nivel = True
            segundo_nivel = False
            primer_nivel = False
            pantalla_nivel(ventana_ppal, 3, "Destruye la estrella de la muerte!")
            tiempo_inicial = pygame.time.get_ticks()
            player.vidas = 100 
            nivel_tres()
        elif tercer_nivel:
            if tiempo_restante == 0:
                segundo_nivel = False
                tercer_nivel = False
                primer_nivel = False
                pantalla_game_over(score)
                
    grupos_update()

    texto_puntuacion(ventana_ppal,('score: '+ str(score)+' '),20,ANCHO_VENTANA-75,2)
    barra_vida(ventana_ppal,texto_puntuacion(ventana_ppal,'  vida: ',20,ANCHO_VENTANA-970,2),ANCHO_VENTANA-930,10,player.vidas)
    mostrar_nivel(nivel_actual)
    mostrar_cronometro(tiempo_restante)
    
    pygame.display.update()  
    Reloj.tick(fps) 

    pygame.display.flip()
pygame.quit()
sys.exit()

