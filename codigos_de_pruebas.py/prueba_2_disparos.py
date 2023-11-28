import time
from typing import Any
import pygame 
import random
from pygame.locals import  K_RIGHT, K_LEFT, K_SPACE, K_b, QUIT
from pygame.math import Vector2
import re






ANCHO_VENTANA = 1000
ALTO_VENTANA = 720
# Duración del nivel en segundos (1 minuto)
DURACION_NIVEL = 60

tiempo_inicial = None
cronometro_iniciado = False

pygame.mixer.init()  # Inicializar el módulo de sonido

sonido_torpedo = pygame.mixer.Sound("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/sonido laser.mp3")
sonido_torpedo.set_volume(0.9) 
sonido_laser = pygame.mixer.Sound("tp_video_juego.py/corto.wav")
sonido_laser.set_volume(1.0)
sonido_colision = pygame.mixer.Sound("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/golpe.wav")
sonido_colision.set_volume(0.8)  # Ajusta el volumen según tus preferencias
sonido_explosion = pygame.mixer.Sound("tp_video_juego.py\explosion.wav")
sonido_explosion.set_volume(0.4)
#lista de fotos de la explosion
explosion_lista = []
for i in range(1,13):
    explosion = pygame.image.load(f"tp_video_juego.py/explosion/{i}.png")
    explosion_lista.append(explosion)
    
    
pygame.init()
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

# TITULO DE LA VENTANA
pygame.display.set_caption("   STAR WARS   ")
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
#--------------------------------pantalla nivel 1-------------------------------
def pantalla_nivel_uno(screen):
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 24)

    titulo_texto = font_titulo.render("Nivel 1", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("Tu misión es eliminar las naves enemigas", True, (255, 255, 255))
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
#---------------------------pantalla nivel 2-------------------------------------
def pantalla_nivel_dos(screen):
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 24)

    titulo_texto = font_titulo.render("Nivel 2", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("presta atencion las naves imperiales abrieron fuego!", True, (255, 255, 255))
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


#-----------------------------menu principal-----------------------------------------------
def nombre_en_menu(screen):
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
    texto_boton = fuente_boton.render(" INGRESAR ", True, (255, 255, 255))
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
        
        if mensaje_error:
            error_font = pygame.font.Font(None, 24)
            error_text = error_font.render(mensaje_error, True, (255, 0, 0))
            error_rect = error_text.get_rect(center=(ANCHO_VENTANA // 2, input_rect.bottom + 60))
            screen.blit(error_text, error_rect)
        
        pygame.display.flip()
        reloj.tick(30)
        
        
#------------------NAVE REBELDE/USUARIO----------------------
class nave_rebelde(pygame.sprite.Sprite):

    def __init__(self, posicion=(0, 0)):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/xwing.png") , (120, 120))
        self.img = self.image 
        self.rect = self.image.get_rect()#(center=(posicion[0], ALTO_VENTANA -60))
        self.rect.centerx = ANCHO_VENTANA//2
        self.rect.centery = ALTO_VENTANA -70
        #self.posicion = Vector2(self.rect.center)
        #self.velocidad = Vector2(0,  0)
        self.velocidad_x = 0
        #self.x_vel = Vector2(0,  12)
        #self.y_vel = Vector2(4,  0)
        self.vidas = 3  # Inicializa el número de vidas en 3
        #cada cuanto se disparan laser y torpedos
        self.cadencia_torpedo = 2.5
        self.cadencia_laser = 0.8
#se crea un grupo para calcular el tiempo de los disparos
        self.proyectiles = pygame.sprite.Group()
#guarda la info de cada uno de los disparos
        self.el_ultimo_laser = time.time()
        self.el_ultimo_torpedo = time.time()  
        self.score = 0

    def update(self):
        #self.velocidad = (0,  0)#cada vez que se actualiza la nave nose mueve sola
        self.velocidad_x = 0
        lista_teclas = pygame.key.get_pressed()
        if lista_teclas[pygame.K_LEFT]:
            #self.velocidad += -self.y_vel
            self.velocidad_x = -5
        elif lista_teclas[pygame.K_RIGHT]:
            #self.velocidad += self.y_vel
            self.velocidad_x = 5


        # Ajustar la posición para que la nave no salga de los límites
        #self.posicion += self.velocidad
        self.rect.x += self.velocidad_x
        if self.rect.right > ANCHO_VENTANA:
            self.rect.right = ANCHO_VENTANA
        #self.posicion.x = max(66, min(ANCHO_VENTANA - 66, self.posicion.x))  # Limitar la posición en el eje x
       # self.rect.center = self.posicion
        elif self.rect.left < 0:
            self.rect.left = 0
        self.proyectiles.update()
        
        if lista_teclas[K_SPACE]:
            este_momento = time.time()
            if este_momento - self.el_ultimo_laser >= self.cadencia_laser:
                self.el_ultimo_laser = este_momento
                self.proyectiles.add(
                    Laser((self.rect.x + 5, self.rect.y + 110)),
                    Laser((self.rect.x + 110, self.rect.y + 110)))
                  #  Laser(Vector2(self.rect.x + 5,  self.rect.y + 110)), 
                  #  Laser(Vector2(self.rect.x + 110,  self.rect.y + 110))
                sonido_laser.play() 
        if lista_teclas[K_b]:
            este_momento = time.time()
            if este_momento - self.el_ultimo_torpedo >= self.cadencia_torpedo:
                self.el_ultimo_torpedo = este_momento
                self.proyectiles.add(
                    Torpedo((self.rect.centerx, self.rect.centery)))
                sonido_torpedo.play() 
       # self.posicion +=  self.velocidad
      #  self.rect.center = self.posicion
        self.proyectiles.update()
#---------------------DISPARO LASER-------------------------------------
class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/rayolaser_verde.png"), (80, 70))
        self.rect = self.image.get_rect(center=(posicion[0], ALTO_VENTANA - 100))
        self.posicion = [self.rect.centerx, self.rect.centery]
        self.velocidad = [0, -15]

    def update(self):
        self.posicion[0] += self.velocidad[0]
        self.posicion[1] += self.velocidad[1]
        self.rect.center = (self.posicion[0], self.posicion[1])

        # Destruir cuando se salga de la ventana (superior)
        if self.rect.bottom < 0:
            self.kill()
    '''
    def __init__(self, posicion):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/rayolaser_verde.png") , (80, 70))
        self.rect = self.image.get_rect(center=(posicion[0], ALTO_VENTANA -100))
        self.rect.center = posicion
        self.posicion = Vector2(self.rect.center)
        self.velocidad = Vector2(0,  -15)    

    def update(self):
        self.posicion += self.velocidad
        self.rect.center = self.posicion
        # Destruir cuando se salga de la ventana (superior)
        if self.rect.bottom < 0:    
            self.kill()   
'''
#----------------DISPARO TORPEDO---------------------------------
class Torpedo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/laser_azul.png") , (150, 120))
        self.rect = self.image.get_rect(center=posicion)
        self.posicion = [self.rect.centerx, self.rect.centery]
        self.velocidad = [0, -10]
    def update(self):
        self.posicion[0] += self.velocidad[0]
        self.posicion[1] += self.velocidad[1]
        self.rect.center = (self.posicion[0], self.posicion[1])

        # Destruir cuando se salga de la ventana (superior)
        if self.rect.bottom < 0:
            self.kill()


#----------------------NAVE ENEMIGA-----------------------------------
class nave_enemiga(pygame.sprite.Sprite):
    def __init__(self,x):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tie figther.png"), (108, 61))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1,ANCHO_VENTANA)
       # self.rect.y = 1
        #self.rect.center = position
        #self.position = Vector2(position)
        #self.velocity = Vector2(0, 2)  # Velocidad de movimiento hacia abajo
        self.velocidad_y = random.randrange(1,7)
        #self.last_shoot_time = time.time()
        #self.shoot_delay = random.uniform(1.0, 2.0)  # Cadencia de disparo aleatoria

    def update(self):
        self.rect.y += self.velocidad_y

        # Si la nave enemiga se mueve fuera de la pantalla hacia abajo, la reiniciamos arriba
        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height
            self.rect.x = random.randrange(1, ANCHO_VENTANA)
            self.velocidad_y = random.randrange(1, 5)
        
        
        #self.time = random.randrange(-1,pygame.time.get_ticks()//5000)
        #self.rect.x += self.time
        #if self.rect.x >= ANCHO_VENTANA:
         #   self.rect.x = 0
         #   self.rect.y +=50
        #self.position += self.velocity  
        #self.rect.center = self.position

        # Destruir cuando se salga de la ventana (parte inferior)
        #if self.rect.top > ALTO_VENTANA:
         #   self.kill()

       # este_momento = time.time()
       # if este_momento - self.last_shoot_time >= self.shoot_delay:
       #     self.last_shoot_time = este_momento
        #    self.shoot_laser()

#def shoot_laser(self):
  #  bala = balas_enemigos(self.rect.centerx,self.rect.bottom)
   # grupo_jugador.add(bala)
   # grupo_balas_enemigos.add(bala)
    def defensa_enemigos(self):
       bala = Balas_enemigos(self.rect.centerx,self.rect.bottom)
       grupo_jugador.add(bala)
       grupo_balas_enemigos.add(bala)
       
   
#------------------------BALAS ENEMIGOS--------------------
class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/laser_rojo.png") , (80, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10,ANCHO_VENTANA)
        self.velocidad_y = 4
        
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > ALTO_VENTANA:
            self.kill()
        #Dispara un láser desde la posición actual de la nave enemiga
        #enemy_laser = Laser(self.position)
        #enemy_laser.velocidad = Vector2(0, 10)  # Ajusta la velocidad del láser enemigo
        #nave_propia.proyectiles.add(enemy_laser)
#---------------EXPLOSION--------------------------------------
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
                
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador= pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()            
#---------------------------main----------------------------------------    
def main():
    pygame.init()

    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pantalla_inicial(ventana)  # Llama a la pantalla inicial
    player_name = nombre_en_menu(ventana)
    nivel_actual = 1
    
    if player_name is None:
        return  # Salir si el usuario cerró la ventana de inicio
    pantalla_nivel_uno(ventana)  # Llama a la pantalla del nivel 1
    tiempo_inicial = time.time()  # Inicializar el cronómetro
    nave_propia = nave_rebelde((ANCHO_VENTANA / 2, ALTO_VENTANA / 2))
    star_ship_grp = pygame.sprite.GroupSingle(nave_propia)

    naves_imperiales = pygame.sprite.Group()

    #reloj = pygame.time.Clock()
    
    fondo = pygame.image.load("tp_video_juego.py/Download 4k Ultra Hd Galaxy Star Constellation Wallpaper.jpg")
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

    while True:
        tiempo_transcurrido = time.time() - tiempo_inicial
        tiempo_restante = max(DURACION_NIVEL - tiempo_transcurrido, 0)
        minutos = int(tiempo_restante / 60)
        segundos = int(tiempo_restante % 60)
        tiempo_formateado = f"{minutos:02d}:{segundos:02d}"

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        star_ship_grp.update()

        # Agregar naves enemigas de forma aleatoria
        if random.random() < 0.02:
            enemy_ship = nave_enemiga((random.randint(0, ANCHO_VENTANA), 0))
            naves_imperiales.add(enemy_ship)

        naves_imperiales.update()
        
        if tiempo_formateado == "00:00" and nave_propia.vidas >= 1:
            nivel_actual += 1  # Incrementa el nivel
            tiempo_inicial = 60  # Reinicia el cronómetro
            nave_propia.vidas = 3  # Restablece las vidas del jugador si lo deseas

            if nivel_actual == 2:
                    pantalla_nivel_dos(ventana)
            #elif nivel_actual == 3:
            #       pantalla_nivel_dos(ventana)

        # Comprobar colisiones entre láseres del jugador y naves enemigas
        collisions = pygame.sprite.groupcollide(nave_propia.proyectiles, naves_imperiales, True, True)
        for enemy in collisions.values():
            for e in enemy:
                e.kill()
                nave_propia.score += 100 # Aumenta la puntuación del jugador en 1 por cada enemigo destruido
                sonido_explosion.play()
        # Resta una vida si la nave rebelde colisiona con una nave enemiga
        if pygame.sprite.spritecollide(nave_propia, naves_imperiales, True):
            nave_propia.vidas -= 1
            sonido_colision.play()
            
        for enemy_ship in naves_imperiales:
            if enemy_ship.rect.top >= ALTO_VENTANA:
            #   nave_propia.score -= 1
                enemy_ship.kill()
        
        ventana.blit(fondo, (0, 0))
        nave_propia.proyectiles.draw(ventana)
        star_ship_grp.draw(ventana)
        naves_imperiales.draw(ventana)

# Muestra la puntuacion en la pantalla(score)    
        font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 30)
        score_texto = font.render(f"Score: {nave_propia.score}", True, (255, 255, 255))
        ventana.blit(score_texto, (10, 10))
        
# Mostrar el cron0metro en la parte superior derecha
        font_cronometro = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 24)
        cronometro_text = font_cronometro.render(tiempo_formateado, True, (255, 255, 255))
        ventana.blit(cronometro_text, (ANCHO_VENTANA - 120, 10))
#muestra vidas
        fuente_vidas = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 24)
        vidas_text = fuente_vidas.render(f"  vidas: {nave_propia.vidas}", True, (255, 255, 255))
        ventana.blit(vidas_text, (10, 40))  # Muestra las vidas en la posición deseada
        
        pygame.display.flip()
        
        if nave_propia.vidas <= 0:
                break
# Game Over
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/darth vader.mp3")  # Detener la música de fondo
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    fuente_game_over = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/Starjedi.ttf", 50)
    game_over_texto = fuente_game_over.render("game over", True, (255, 0, 0))
    game_over_rect = game_over_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    score_texto = font.render(f"Puntuación: {nave_propia.score}", True, (255, 255, 255))
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))

    ventana.blit(game_over_texto, game_over_rect)
    ventana.blit(score_texto, score_rect)
    pygame.display.flip()
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

if __name__ == '__main__':
    main()
    pygame.quit()