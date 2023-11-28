
import pygame ,sys
import random
from pygame.locals import  K_RIGHT, K_LEFT, K_SPACE, K_b, QUIT
import re


pygame.init()
pygame.mixer.init()  # Inicializar el módulo de sonido

sonido_laser = pygame.mixer.Sound("tp_video_juego.py/corto.wav")
sonido_laser.set_volume(1.0)
sonido_colision = pygame.mixer.Sound("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/golpe.wav")
sonido_colision.set_volume(0.8)  # Ajusta el volumen según tus preferencias
sonido_explosion = pygame.mixer.Sound("tp_video_juego.py/explosion.wav")
sonido_activado = True
#lista de fotos de la explosion
explosion_lista = []
for i in range(1,13):
    explosion = pygame.image.load(f"tp_video_juego.py/explosion/{i}.png")
    explosion_lista.append(explosion)
    

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720
PANTALLA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
fondo = pygame.image.load("tp_video_juego.py/space-1.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
x = 0
y = 0
#fondo_rect = fondo.get_rect()
#fondo_rect.topleft = (0, 0)

# Duración del nivel en segundos (1 minuto)
DURACION_NIVEL = 15

tiempo_inicial = None
cronometro_iniciado = False
tiempo_restante = 0
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("   STAR WARS   ")
run = True
fps = 80
Reloj = pygame.time.Clock()
score = 0
vida = 100
blanco = (255,255,255)
negro =  (0,0,0)
green = (0,255,0)
amarillo = (255, 255, 0)
segundo_nivel = False

def texto_puntuacion(frame,text,size,x,y):
    font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py\Starjedi.ttf",size)
    texto_frame = font.render(text,True,blanco,negro)
    text_rect = texto_frame.get_rect()
    text_rect.midtop = (x,y)
    frame.blit(texto_frame,text_rect)
#-------------------------barra de vidas-----------------------------------    
def barra_vida(frame,str,x,y,nivel):
    longitud = 100
    alto = 20
    fill = int((nivel/100)*longitud)
    border = pygame.Rect(x,y,longitud,alto)
    fill = pygame.Rect(x,y,fill,alto)
    pygame.draw.rect(frame,green,fill)
    pygame.draw.rect(frame,blanco,border,2)
#-------------------------cronometro-----------------------------
def mostrar_cronometro(tiempo_restante):
    fuente_cronometro = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py\Starjedi.ttf", 30)
    texto_cronometro = fuente_cronometro.render(f"{tiempo_restante}", True, blanco)
    rect_cronometro = texto_cronometro.get_rect(center=(ANCHO_VENTANA // 2, 30))
    ventana_ppal.blit(texto_cronometro, rect_cronometro)


#----------------------------------primer pantalla-------------------------
'''se inicia muestra una imagen luego se debe apreta enter para pasar al menu.'''
def pantalla_inicial(screen):
    imagen_inicial = pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/wall4.jpg")
    ventana_ancho, ventana_alto = screen.get_size()
    imagen_inicial = pygame.transform.scale(imagen_inicial, (ventana_ancho, ventana_alto))
    screen.blit(imagen_inicial, (0, 0))
    pygame.display.flip()
    
    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                esperando_input = False
                break
#-----------------------------menu principal-----------------------------------------------
def nombre_en_menu(screen):
    global sonido_activado
    #nombre = ""
    font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py\Starjedi.ttf", 26)
    input_rect = pygame.Rect(400, 155, 140, 50)
    color_inactivo = pygame.Color((255, 165, 0))
    color_activo = pygame.Color((255, 255, 0))
    color = color_inactivo
    activo = False
    texto_ingresado = ''
    mensaje_error = ''
    reloj = pygame.time.Clock()
    
#titulo inicial de bienvenida
    titulo_fuente = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 30)
    titulo_texto = titulo_fuente.render("$ Bienvenido a combatir contra el imperio $", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, 90))
#subtitulo da orden
    subtitulo_font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py\Starjedi.ttf", 20)
    subtitulo_text = subtitulo_font.render("ingresa tu nombre", True, (255, 255, 255))
    subtitulo_rect = subtitulo_text.get_rect(center=(ANCHO_VENTANA // 2, input_rect.y - 20))

#imagen logo star wars
    imagen_abajo = pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/loguito.png")
    imagen_rect = imagen_abajo.get_rect()
    imagen_rect.center = (ANCHO_VENTANA // 2, input_rect.bottom + 285)

#boton ingresar
    fuente_boton = pygame.font.Font(None, 30)
    texto_boton = fuente_boton.render(" PLAY ", True, (255, 255, 255))
    rect_boton = texto_boton.get_rect(center=(ANCHO_VENTANA // 2, input_rect.bottom + 20))
    
#musica
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Star Wars Main Theme (Full) (128 kbps).mp3")  # Reemplaza con el nombre de tu archivo de música
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.2)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Salir si el usuario cierra la ventana

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    activo = not activo
                else:
                    activo = False
                color = color_activo if activo else color_inactivo

                if rect_boton.collidepoint(event.pos):
                    if re.match("^[a-z0-9]+$", texto_ingresado):
                        return texto_ingresado.lower()  
                    else:
                        mensaje_error = "Texto no válido. Ingrese solo letras y números."
                        texto_ingresado = ''
                        
                    # Controlar clic en el botón de sonido
            if event.type == pygame.MOUSEBUTTONDOWN and sonido_rect.collidepoint(event.pos):
                sonido_activado = not sonido_activado
                if sonido_activado:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

            if event.type == pygame.KEYDOWN:
                if activo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_ingresado = texto_ingresado[:-1]
                    else:
                        texto_ingresado += event.unicode
                        

        screen.fill((30, 30, 30)) #color de fondo
        screen.blit(titulo_texto, titulo_rect)  # Dibuja el título en la ventana
        screen.blit(subtitulo_text, subtitulo_rect)  # Dibuja el subtítulo en la ventana
        txt_surface = font.render(texto_ingresado, True, color)
        width = max(200, txt_surface.get_width() + 90)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, color, input_rect, 5) #grosor del rectangulo

        screen.blit(imagen_abajo, imagen_rect)
        
        
        pygame.draw.rect(screen, (255, 0, 0), rect_boton)
        screen.blit(texto_boton, rect_boton)
        
            # Botón de sonido
        sonido_rect = pygame.Rect(10, 10, 100, 20)
        sonido_color = (0, 255, 0) if sonido_activado else (255, 0, 0)
        sonido_texto = fuente_boton.render("  MUSICA  ", True, (255, 255, 255))
        sonido_rect.topleft = (20, 20)
        pygame.draw.rect(screen, sonido_color, sonido_rect)
        screen.blit(sonido_texto, sonido_rect)

        
        if mensaje_error:
            error_font = pygame.font.Font(None, 24)
            error_text = error_font.render(mensaje_error, True, (255, 0, 0))
            error_rect = error_text.get_rect(center=(ANCHO_VENTANA // 2, input_rect.bottom + 60))
            screen.blit(error_text, error_rect)
        
        pygame.display.flip()
        reloj.tick(30)
#--------------------------------pantalla nivel 1-------------------------------
def pantalla_nivel_uno(screen):
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 24)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 18)
    
    titulo_texto = font_titulo.render("Nivel 1", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("Tu misión es eliminar las naves enemigas", True, (255, 255, 255))
    mision_rect = mision_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))

    indicacion_texto = font_indicacion.render("Pulsa una tecla para empezar...", True, (255, 255, 255))
    indicacion_rect = indicacion_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))

    screen.fill((0, 0, 0))  # Color de fondo
    screen.blit(titulo_texto, titulo_rect)
    screen.blit(mision_texto, mision_rect)
    screen.blit(indicacion_texto, indicacion_rect)
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                esperando_input = False
                break  
            
#-------------------PANTALLA NIVEL 2---------------------------
def pantalla_nivel_dos(screen):
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 24)

    titulo_texto = font_titulo.render("Nivel 2", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("cuidado el enemigo abrio fuego!", True, (255, 255, 255))
    mision_rect = mision_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))

    screen.fill((0, 0, 0))  # Color de fondo
    screen.blit(titulo_texto, titulo_rect)
    screen.blit(mision_texto, mision_rect)
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                esperando_input = False
                break        

#------------------NAVE REBELDE/USUARIO----------------------
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/xwing.png") , (120, 120))
        self.rect = self.image.get_rect()#(center=(posicion[0], ALTO_VENTANA -60))
        self.rect.centerx = ANCHO_VENTANA//2
        self.rect.centery = ALTO_VENTANA -90
        self.velocidad_x = 0
        self.vidas = 100
        


    def update(self):
        self.velocidad_x = 0
        lista_teclas = pygame.key.get_pressed()
        if lista_teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
        elif lista_teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
        # Ajustar la posición para que la nave no salga de los límites
        self.rect.x += self.velocidad_x
        if self.rect.right > ANCHO_VENTANA:
            self.rect.right = ANCHO_VENTANA
        elif self.rect.left < 0:
            self.rect.left = 0
        
    def disparar(self):
        bala = Balas(self.rect.centerx,self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        sonido_laser.play()


#----------------------NAVE ENEMIGA-----------------------------------
class nave_enemiga(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tie figther.png"), (98, 71))
        self.rect = self.image.get_rect()
        self.rect.x =  random.randrange(1,ANCHO_VENTANA)
        # self.rect.y =   0
        self.velocidad_y = random.randrange(1,2)


    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height
            self.rect.x = random.randrange(1, ANCHO_VENTANA)
            self.velocidad_y = random.randrange(1, 5)
    def disparos_enemigos(self):
        bala = Balas_enemigos(self.rect.centerx,self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)

        
        
class Balas(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/rayolaser_verde.png") , (80, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = -18
        
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom <0:
            self.kill()
            
#------------------------BALAS ENEMIGOS--------------------
class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/laser_rojo.png") , (80, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        #self.rect.y = y 
        self.velocidad_y = 4
        
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > ALTO_VENTANA:
            self.kill()
            
#--------------------------EXPLOSION--------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = explosion_lista[0]
        img_scala = pygame.transform.scale(self.image,(20,20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explosion = 30
        self.frames = 0
        
    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explosion:
            self.time = tiempo
            self.frames +=1
            if self.frames == len(explosion_lista):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_lista[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position 
                
 #-----------------------pantalla game over---------------------------------------
def pantalla_game_over():
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/darth vader.mp3")  # Detener la música de fondo
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    fuente_game_over = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 40)
    game_over_texto = fuente_game_over.render("game over", True, (255, 0, 0))
    game_over_rect = game_over_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    score_texto = fuente_game_over.render(f"Puntuación: {score}", True, (255, 255, 255))
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))

    ventana_ppal.blit(game_over_texto, game_over_rect)
    ventana_ppal.blit(score_texto, score_rect)
    pygame.display.flip()
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return             
#---------------segundo nivel-----------------------------------------------------
def segundo_nivel():
    global tiempo_inicial, cronometro_iniciado, segundo_nivel
    tiempo_inicial = pygame.time.get_ticks()
    cronometro_iniciado = True
    segundo_nivel = True
#---------------------------------------------------------------------------------
                

grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador= pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()   
grupo_explosiones = pygame.sprite.Group()   

player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

pantalla_inicial(ventana_ppal)


################################################################################
################################################################################
################################################################################

en_juego = True
#en_partida = False
while en_juego:

    num_vidas = 100
    nivel_actual = 1

    en_partida = False
    en_inicio = True
    
    while en_inicio:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_inicio = False
                en_juego = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    en_inicio = False
                    en_partida = True 

            player_name = nombre_en_menu(ventana_ppal)
            pantalla_nivel_uno(ventana_ppal) 
            en_partida = True
            
            
            pygame.display.update()  
 
            
        while en_partida:

            en_final = False  
        
            for x in range(10):
                enemigo = nave_enemiga(random.randint(0,ANCHO_VENTANA),0)
                grupo_enemigos.add(enemigo)
                grupo_jugador.add(enemigo)
            
            tiempo_inicial = pygame.time.get_ticks()
            cronometro_iniciado = True
            
            en_nivel = True
            while en_nivel:
                Reloj.tick(fps)
                
                        #ventana_ppal.blit(fondo, fondo_rect.topleft)  
                        # Movimiento del fondo
                y_relativa = y % fondo.get_rect().height
                ventana_ppal.blit(fondo,(0,y_relativa - fondo.get_rect().height))

                if(y_relativa < ALTO_VENTANA):
                    ventana_ppal.blit(fondo,(0,y_relativa))
                y += 10
                
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_nivel = False
                        en_partida = False
                        en_juego = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            player.disparar() 
        
                for enemigo in grupo_enemigos:
                    if enemigo.rect.top > ALTO_VENTANA:
                        enemigo.rect.y = 0
                        enemigo.rect.x = random.randint(1, ANCHO_VENTANA - 50)
                        
                        
                if player.vidas == 0:
                    ganando = False
                    en_final = True

                if nivel_actual > 3:
                    ganando = True
                    en_final = True
                '''
                if tiempo_restante == 0 and player.vidas >= 1 and not segundo_nivel:
                        nivel_actual += 1
                        segundo_nivel = True
                        pantalla_nivel_dos(ventana_ppal)
                        segundo_nivel()
                        tiempo_inicial = pygame.time.get_ticks()
                        player.vidas = 3

                tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial

                if tiempo_inicial is not None and cronometro_iniciado:
                    tiempo_restante = max(0, DURACION_NIVEL - tiempo_transcurrido // 1000)
                    mostrar_cronometro(tiempo_restante)

                #if tiempo_restante == 0 and not segundo_nivel:
                # cronometro_iniciado = False  # Termina el cronómetro cuando se agota el tiempo
                '''
############################actualizacion de grupos#########################################    
        
                grupo_jugador.update()
                grupo_enemigos.update()
                grupo_balas_jugador.update()
                grupo_balas_enemigos.update()
        
                grupo_jugador.draw(ventana_ppal)
                
################################## colosiones ###############################################                
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
                        pantalla_game_over()
                        explo_3 = Explosion(choque.rect.center)
                        grupo_jugador.add(explo_3)
                        en_juego = False

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
                        en_juego = False
                
                texto_puntuacion(ventana_ppal,('score: '+ str(score)+' '),20,ANCHO_VENTANA-75,2)
                barra_vida(ventana_ppal,texto_puntuacion(ventana_ppal,'  vida: ',20,ANCHO_VENTANA-970,2),ANCHO_VENTANA-930,10,player.vidas)
                pygame.display.flip()
                
            while en_final:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        en_nivel = False
                        en_partida = False
                        en_juego = False
                        pantalla_game_over()

                pygame.display.update()  
        

    Reloj.tick(fps) 
    pygame.display.flip()
pygame.quit()

