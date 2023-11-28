
import pygame ,sys
import random
from pygame.locals import  K_RIGHT, K_LEFT, K_SPACE, K_b, QUIT
import re
import sqlite3
import time


pygame.init()
#pygame.mixer.init()  # Inicializar el módulo de sonido

sonido_laser = pygame.mixer.Sound("tp_video_juego.py\sonidos.py\sonido_laser_w.mpeg")
sonido_laser.set_volume(1.0)
sonido_colision = pygame.mixer.Sound("tp_video_juego.py\sonidos.py\golpe.wav")
sonido_colision.set_volume(0.8)  # Ajusta el volumen según tus preferencias
sonido_explosion = pygame.mixer.Sound("tp_video_juego.py\sonidos.py\corto.wav")
sonido_activado = True
# Añadir sonido al ingreso de caracteres en el input
sonido_tecla = pygame.mixer.Sound("tp_video_juego.py\sonidos.py\corto.wav")
sonido_tecla.set_volume(1.5)  # Ajusta el volumen según tus preferencias

#lista de fotos de la explosion
explosion_lista = []
for i in range(1,13):
    explosion = pygame.image.load(f"tp_video_juego.py\imagenes.py\explosion\{i}.png")
    explosion_lista.append(explosion)
    

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720
PANTALLA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
fondo = pygame.image.load("tp_video_juego.py\imagenes.py\space-1.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
x = 0
y = 0


# Duración del nivel en segundos (1 minuto)
DURACION_NIVEL = 7

tiempo_inicial = None
cronometro_iniciado = False
#tiempo_restante = 0
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("   STAR WARS   ")
run = True
fps = 80
Reloj = pygame.time.Clock()
score = 0
vida = 100
#COLORES
blanco = (255,255,255)
negro =  (0,0,0)
green = (0,255,0)
amarillo = (255, 255, 0)



# Cargar la imagen del icono
icono = pygame.image.load("tp_video_juego.py/imagenes.py/xwing.png")

# Establecer el icono de la ventana
pygame.display.set_icon(icono)

###################SQL#######################################
# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect("puntajes.db")
cursor = conn.cursor()

# Crear la tabla de puntajes si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS puntajes(nombre TEXT, score INTEGER)''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
#--------------------------------------------------------------------------
def texto_puntuacion(frame,text,size,x,y):
    font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf",size)
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
    fuente_cronometro = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 30)
    texto_cronometro = fuente_cronometro.render(f"{tiempo_restante}", True, blanco)
    rect_cronometro = texto_cronometro.get_rect(center=(ANCHO_VENTANA // 2, 30))
    ventana_ppal.blit(texto_cronometro, rect_cronometro)


#----------------------------------primer pantalla-------------------------
'''se inicia muestra una imagen luego se debe apreta enter para pasar al menu.'''
def pantalla_inicial(screen):
    imagen_inicial = pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/wall4.jpg")
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
    font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 26)
    input_rect = pygame.Rect(400, 155, 140, 50)
    color_inactivo = pygame.Color((255, 165, 0))
    color_activo = pygame.Color((255, 255, 0))
    color = color_inactivo
    activo = False
    texto_ingresado = ''
    mensaje_error = ''
    reloj = pygame.time.Clock()
    
#titulo inicial de bienvenida
    titulo_fuente = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 30)
    titulo_texto = titulo_fuente.render("$ Bienvenido a combatir contra el imperio $", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, 90))
#subtitulo da orden
    subtitulo_font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 20)
    subtitulo_text = subtitulo_font.render("ingresa tu nombre", True, (255, 255, 255))
    subtitulo_rect = subtitulo_text.get_rect(center=(ANCHO_VENTANA // 2, input_rect.y - 20))

#imagen logo star wars
    imagen_abajo = pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/loguito.png")
    imagen_rect = imagen_abajo.get_rect()
    imagen_rect.center = (ANCHO_VENTANA // 2, input_rect.bottom + 285)

#boton ingresar
    fuente_boton = pygame.font.Font(None, 30)
    texto_boton = fuente_boton.render(" PLAY ", True, (255, 255, 255))
    rect_boton = texto_boton.get_rect(center=(ANCHO_VENTANA // 2, input_rect.bottom + 20))
    
#musica
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/sonidos.py/Star Wars Main Theme (Full) (128 kbps).mp3")  # Reemplaza con el nombre de tu archivo de música
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.2)
    
# Botón de ranking
    fuente_boton_ranking = pygame.font.Font(None, 30)
    texto_boton_ranking = fuente_boton_ranking.render(" RANKING ", True, (255, 255, 255))
    rect_boton_ranking = texto_boton_ranking.get_rect(topright=(ANCHO_VENTANA - 20, 20))

# Botón de sonido
    sonido_rect = pygame.Rect(10, 10, 100, 20)
    sonido_color = (0, 255, 0) if sonido_activado else (255, 0, 0)
    sonido_texto = fuente_boton.render("  MUSICA  ", True, (255, 255, 255))
    sonido_rect.topleft = (20, 20)


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

                if rect_boton_ranking.collidepoint(event.pos):
                    mostrar_ranking()  # Llamada a la función que muestra el ranking

                
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
                    texto_ingresado = manejar_ingreso_texto(texto_ingresado, event)
                        

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
        
        pygame.draw.rect(screen, (255, 0, 0), rect_boton_ranking)
        screen.blit(texto_boton_ranking, rect_boton_ranking)
        
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
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 24)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)
    
    titulo_texto = font_titulo.render("Nivel 1", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("Tu misión es eliminar las naves enemigas", True, amarillo)
    mision_rect = mision_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))

    indicacion_texto = font_indicacion.render("Pulsa ENTER para empezar...", True, (255, 255, 255))
    indicacion_rect = indicacion_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))

    screen.fill((0, 0, 0))  # Color de fondo
    screen.blit(titulo_texto, titulo_rect)
    screen.blit(mision_texto, mision_rect)
    screen.blit(indicacion_texto, indicacion_rect)
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                esperando_input = False
                break  
            
#-------------------PANTALLA NIVEL 2---------------------------
def pantalla_nivel_dos(screen):
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 24)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)


    titulo_texto = font_titulo.render("Nivel 2", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("cuidado el enemigo abrio fuego!", True, (255, 255, 255))
    mision_rect = mision_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))
    
    indicacion_texto = font_indicacion.render("Pulsa ENTER para empezar...", True, (255, 255, 255))
    indicacion_rect = indicacion_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))

    screen.fill((0, 0, 0))  # Color de fondo
    screen.blit(titulo_texto, titulo_rect)
    screen.blit(mision_texto, mision_rect)
    screen.blit(indicacion_texto, indicacion_rect)
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                esperando_input = False
                break  
#--------------------PANTALLA NIVEL 3 ----------------------------------------------
def pantalla_nivel_tres(screen):
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 24)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)

    titulo_texto = font_titulo.render("Nivel 3", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("destruye la estrella de la muerte!", True, (255, 255, 255))
    mision_rect = mision_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))

    indicacion_texto = font_indicacion.render("Pulsa ENTER para empezar...", True, (255, 255, 255))
    indicacion_rect = indicacion_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))
    
    screen.fill((0, 0, 0))  # Color de fondo
    screen.blit(titulo_texto, titulo_rect)
    screen.blit(mision_texto, mision_rect)
    screen.blit(indicacion_texto, indicacion_rect)
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                esperando_input = False
                break    

#------------------NAVE REBELDE/USUARIO----------------------
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/xwing.png") , (80, 80))
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
#---------------------kamikaze----------------------------------------
class meteoritos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        # Cargar la imagen original desde el archivo "meteorito.png"
        imagen_original = pygame.image.load("tp_video_juego.py/imagenes.py/meteorito.png")
        
        # Escalar la imagen a un tamaño aleatorio
        escala = random.uniform(0.1, 0.3)  # Puedes ajustar estos valores según tus preferencias
        ancho = int(imagen_original.get_width() * escala)
        alto = int(imagen_original.get_height() * escala)
        
        # Crear la imagen escalada
        self.image = pygame.transform.scale(imagen_original, (ancho, alto))
        
        # Obtener el rectángulo de la imagen escalada
        self.rect = self.image.get_rect()
        
        # Configurar otras propiedades de la instancia
        self.rect.x = random.randrange(1, ANCHO_VENTANA)
        self.rect.y = 0
        self.velocidad_y = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height
            self.rect.x = random.randrange(1, ANCHO_VENTANA)
            self.velocidad_y = random.randrange(1, 5)


#----------------------NAVE ENEMIGA-----------------------------------
class nave_enemiga(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/nave_enemiga.png"), (68, 51))
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
        grupo_balas_enemigos_nivel_dos.add(bala)

        
#-----------------------------------BALAS---------------------------------------------        
class Balas(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/rayolaser_verde.png") , (50, 60))
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
        self.image = pygame.transform.scale( pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/laser_rojo.png") , (80, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        #self.rect.y = y 
        self.velocidad_y = 4
        
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > ALTO_VENTANA:
            self.kill()
            
#---------------EXPLOSION----------------------------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = explosion_lista[0]
        img_scala = pygame.transform.scale(self.image,tamaño)
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
                
#------------------------ ESTRELLA DE LA MUERTE -----------------------------------
class estrella_de_la_muerte(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/estrelladelamuerte.png"), (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA // 2 - self.rect.width // 2
        self.rect.y = 0
        self.velocidad_y = 0  # Puedes ajustar la velocidad según sea necesario
        self.vidas = 1000
        
    def update(self):
        self.rect.y += self.velocidad_y  
        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height  
    '''       
    def impacto(self, int):
        self.vidas -= 30
        if self.vidas <= 0:
            explo_estrella = Explosion(self.rect.center)
            grupo_explosiones.add(explo_estrella)
            self.kill()
    '''      
#-----------------------pantalla game over----------------------------------------
def pantalla_game_over():
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/darth vader.mp3")  # Detener la música de fondo
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    fuente_game_over = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    game_over_texto = fuente_game_over.render("game over", True, (255, 0, 0))
    game_over_rect = game_over_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    score_texto = fuente_game_over.render(f"Puntuación: {score}", True, (255, 255, 255))
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))

    salir_fuente = pygame.font.Font(None, 36)
    salir_texto = salir_fuente.render("Salir", True, (255, 255, 255))
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))
    
    ventana_ppal.blit(game_over_texto, game_over_rect)
    ventana_ppal.blit(score_texto, score_rect)

    ventana_ppal.blit(salir_texto, salir_rect)
    pygame.display.flip()
        
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return  
            if event.type == pygame.MOUSEBUTTONDOWN:
                salir_rect.collidepoint(event.pos)
                pygame.quit()
                sys.exit()           
#---------------PANTALLA WINS------------------------------------------------------
def pantalla_victoria(nombre_jugador):
    pygame.mixer.music.load("tp_video_juego.py/sonidos.py/obiwan.mp3")  # Cambiar la música de fondo según sea necesario
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    
    fuente_victoria = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    victoria_texto = fuente_victoria.render(f"Haz Triunfado, {nombre_jugador}!", True, (0, 255, 0))
    victoria_rect = victoria_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    
    volver_jugar_fuente = pygame.font.Font(None, 36)
    volver_jugar_texto = volver_jugar_fuente.render("Volver a Jugar", True, (255, 255, 255))
    volver_jugar_rect = volver_jugar_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))
    
    salir_fuente = pygame.font.Font(None, 36)
    salir_texto = salir_fuente.render("Salir", True, (255, 255, 255))
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
    
    ventana_ppal.blit(victoria_texto, victoria_rect)
    ventana_ppal.blit(volver_jugar_texto, volver_jugar_rect)
    ventana_ppal.blit(salir_texto, salir_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volver_jugar_rect.collidepoint(event.pos):
                    nivel_uno()
                    # Aquí puedes reiniciar el juego o volver al menú principal
                    # Dependiendo de la lógica de tu juego
                    pygame.quit()
                    sys.exit()
                elif salir_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
#----------------------------------------------------------------------------------
def manejar_ingreso_texto(texto_ingresado, event):
    global sonido_tecla
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            texto_ingresado = texto_ingresado[:-1]
        else:
            texto_ingresado += event.unicode
            sonido_tecla.play()  # Reproducir el sonido de la tecla
    return texto_ingresado
#----------------------------------------------------------------------------------
def mostrar_ranking():
    conn = sqlite3.connect("puntajes.db")
    cursor = conn.cursor()

    # Seleccionar los 5 mejores puntajes
    cursor.execute("SELECT nombre, score FROM puntajes ORDER BY score DESC LIMIT 5")
    top_puntajes = cursor.fetchall()

    # Crear una fuente para el texto
    font_ranking = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 30)
    font_salir = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 15)

    # Mostrar el título del ranking
    titulo_texto = font_ranking.render("# top 5 puntajes $", True, negro)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 100))
    
    # Mostrar el título del ranking
    salir_texto = font_salir.render('para salir presiona "esc" ', True, negro)
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 200))
    
    # Crear un fondo negro para la lista de puntajes
    fondo_rect = pygame.Rect(ANCHO_VENTANA // 2 - 188, ALTO_VENTANA // 2 - 135, 380, 370)
    pygame.draw.rect(ventana_ppal, (204, 119, 34), fondo_rect)
    
    ventana_ppal.blit(titulo_texto, titulo_rect)
    ventana_ppal.blit(salir_texto, salir_rect)

    # Mostrar los puntajes
    y_offset = 0
    for i, (nombre, puntaje) in enumerate(top_puntajes, start=1):
        texto_ranking = font_ranking.render(f"{i}. {nombre}: {puntaje}", True, negro)
        rect_ranking = texto_ranking.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50 + y_offset))
        ventana_ppal.blit(texto_ranking, rect_ranking)
        y_offset += 40

    pygame.display.flip()

    # Esperar a que el usuario cierre la ventana
    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volver a la pantalla principal al presionar Esc
                sys.exit()
                
        pygame.display.flip()
        #reloj.tick(30)

#--------------------------------mostrar nivel------------------------------------
def mostrar_nivel(nivel):
    font = pygame.font.Font(None, 20)
    texto = font.render(f"Nivel: {nivel}", True, blanco)
    ventana_ppal.blit(texto, (10, ALTO_VENTANA - 30))

#----------------------------------------------------------------------------------
###################################################################################
##################################LOGICA###########################################
###################################################################################

#nivel 1                
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador= pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()   
grupo_explosiones = pygame.sprite.Group()  
grupo_estrella = pygame.sprite.Group()
grupo_meteoritos =pygame.sprite.Group()
#nivel 2
grupo_jugador_nivel_dos = pygame.sprite.Group()
grupo_enemigos_nivel_dos = pygame.sprite.Group()
grupo_balas_jugador_nivel_dos = pygame.sprite.Group()

grupo_jugador_nivel_tres = pygame.sprite.Group()
grupo_enemigos_nivel_tres = pygame.sprite.Group()
grupo_balas_jugador_nivel_tres =pygame.sprite.Group()

grupo_balas_enemigos_nivel_dos = pygame.sprite.Group()
grupo_balas_enemigos_nivel_tres = pygame.sprite.Group()






player = Jugador()
grupo_jugador.add(player)
grupo_jugador_nivel_dos.add(player)
grupo_jugador_nivel_tres.add(player)


grupo_balas_jugador.add(player)
grupo_balas_jugador_nivel_dos.add(player)
grupo_balas_enemigos_nivel_dos.add(player)
grupo_balas_enemigos_nivel_tres.add(player)

pantalla_inicial(ventana_ppal)
player_name = nombre_en_menu(ventana_ppal)
pantalla_nivel_uno(ventana_ppal) 

def nivel_uno():
    for x in range(10):
                meteoros = meteoritos(random.randint(0,ANCHO_VENTANA),0)
                grupo_enemigos.add(meteoros)
                grupo_jugador.add(meteoros)
def nivel_dos():                            
    for x in range(10):
                enemigo = nave_enemiga(random.randint(0,ANCHO_VENTANA),0)
                grupo_enemigos.add(enemigo)
                grupo_jugador.add(enemigo)

def nivel_tres():
    for x in range(15):
                #enemigos_nivel_tres = nave_enemiga(random.randint(0, ANCHO_VENTANA), 0)
                #grupo_enemigos_nivel_tres.add(enemigos_nivel_tres)
                #grupo_jugador_nivel_tres.add(enemigos_nivel_tres)
 
                estrella = estrella_de_la_muerte(ANCHO_VENTANA//2, 0)
                grupo_estrella.add(estrella)
                grupo_jugador_nivel_tres.add(estrella)
                



nivel_actual = 1
primer_nivel =True
segundo_nivel = False
tercer_nivel = False

tiempo_inicial = pygame.time.get_ticks()


nivel_uno()

while run:
    Reloj.tick(fps)
    cronometro_iniciado = True
    
    # Movimiento del fondo
    y_relativa = y % fondo.get_rect().height
    ventana_ppal.blit(fondo,(0,y_relativa - fondo.get_rect().height))

    if(y_relativa < ALTO_VENTANA):
        ventana_ppal.blit(fondo,(0,y_relativa))
    y += 10
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()
                
    for enemigo in grupo_enemigos:
            if enemigo.rect.top > ALTO_VENTANA:
                enemigo.rect.y = 0
                enemigo.rect.x = random.randint(1, ANCHO_VENTANA - 50)
                
                
    ###################################cronometro################################
    tiempo_transcurrido = pygame.time.get_ticks() - tiempo_inicial

    if tiempo_inicial is not None and cronometro_iniciado:
        tiempo_restante = max(0, DURACION_NIVEL - tiempo_transcurrido // 1000)
    
    ########################### COLISIONES #######################################
#CHOQUE METEORITO A jugador        
    choque_meteorito_jugador = pygame.sprite.spritecollide(player,grupo_enemigos_nivel_dos,True)
    for choque in choque_meteorito_jugador:
        explo_3 = Explosion(choque.rect.center,(10,10))
        pygame.display.flip()
        grupo_jugador.add(explo_3)
        player.vidas   -= 30
        sonido_colision.play()
        meteorito = meteoritos(10,10)
        grupo_jugador.add(meteorito)
        grupo_enemigos_nivel_dos.add(meteorito)
        if player.vidas <=0:
            explo_3 = Explosion(choque.rect.center,(10,10))
            grupo_jugador.add(explo_3)
            
            pantalla_game_over()
            run = False
                  
#LASER REBELDE A METEORITOS
    laser_jugador_meteoritos = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)

    for meteorito, balas in laser_jugador_meteoritos.items():
        score+=100
        explo_meteorito = Explosion(meteorito.rect.center)
        grupo_jugador.add(explo_meteorito)
        sonido_explosion.play()

        # Puedes realizar otras acciones aquí, como sumar puntos al jugador

        # Puedes generar nuevos meteoritos si lo deseas
        nuevo_meteorito = meteoritos(10, 10)
        grupo_jugador.add(nuevo_meteorito)
        grupo_enemigos.add(nuevo_meteorito)
        
        
#CHOQUE ENTRE NAVES ENEMIGAS Y JUGADOR
    '''
    choque_entre_naves = pygame.sprite.spritecollide(player,grupo_enemigos_nivel_dos,True)
    for choque in choque_entre_naves:
        explo_3 = Explosion(choque.rect.center,(10,10))
        grupo_jugador.add(explo_3)
        player.vidas   -= 30
        sonido_colision.play()
        enemigos = nave_enemiga(10,10)
        grupo_jugador_nivel_dos.add(enemigos)
        grupo_enemigos_nivel_dos.add(enemigos)
        if player.vidas <=0:
            explo_3 = Explosion(choque.rect.center,(10,10))
            grupo_jugador.add(explo_3)
            pantalla_game_over()
            run = False
    '''        
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
            explo_3 = Explosion(choque.rect.center)
            grupo_jugador.add(explo_3)
            time.sleep(0.2)
            pantalla_game_over()
            run = False
#LASER NAVE ENEMIGA A JUGADOR
    laser_nave_enemiga_a_rebelde = pygame.sprite.spritecollide(player,grupo_balas_enemigos,True)
    for j in laser_nave_enemiga_a_rebelde:
        player.vidas -= 20
        explo_1 = Explosion(j.rect.center)
        grupo_jugador.add(explo_1)
        if player.vidas <=0:
            run = False
            pantalla_game_over()
 #LASER A NAVES ENEMIGAS
    laser_rebelde_a_enemigos = pygame.sprite.groupcollide(grupo_enemigos_nivel_dos ,grupo_balas_jugador,True,True)
    for i in laser_rebelde_a_enemigos:
        score+=100
        enemigo.disparos_enemigos()
        enemigo = nave_enemiga(300,10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        sonido_explosion.play()

#LASER A ESTRELLA DE LA MUERTE   
    laser_rebelde_a_estrella = pygame.sprite.groupcollide(grupo_estrella,grupo_balas_jugador, False, True)
    for estrella, balas in laser_rebelde_a_estrella.items():
        for bala in balas:
            estrella.vidas -= 50
            explo_estrella = Explosion(bala.rect.center ) 
            grupo_jugador.add(explo_estrella)
            sonido_explosion.play()

            if estrella.vidas <= 0:
                run = False
                pantalla_victoria(player_name)
                    
####################################################################################
###################################################################################

#NIVELES:
    if tiempo_restante == 0 and player.vidas >= 1:
        if nivel_actual == 1 and not segundo_nivel:
            # Cambio al NIVEL 2
            nivel_actual += 1
            segundo_nivel = True
            primer_nivel = False
            tercer_nivel = False
            pantalla_nivel_dos(ventana_ppal)
            tiempo_inicial = pygame.time.get_ticks()
            player.vidas = 100    
            nivel_dos()  
        elif nivel_actual == 2 and not tercer_nivel:
            # Cambio al NIVEL 3
            nivel_actual += 1
            tercer_nivel = True
            segundo_nivel = False
            primer_nivel = False
            pantalla_nivel_tres(ventana_ppal)
            tiempo_inicial = pygame.time.get_ticks()
            player.vidas = 100 
            nivel_tres()
        elif tercer_nivel:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.disparar()


    grupo_jugador.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    grupo_meteoritos.update()
    grupo_jugador.draw(ventana_ppal)
        
    grupo_estrella.update()
    
    grupo_jugador_nivel_dos.update()
    grupo_enemigos_nivel_dos.update()
    grupo_balas_jugador_nivel_dos.update()
    grupo_jugador_nivel_dos.draw(ventana_ppal)
    
    grupo_jugador_nivel_tres.update()
    grupo_enemigos_nivel_tres.update()
    grupo_balas_jugador_nivel_tres.update()
    
    grupo_jugador_nivel_tres.draw(ventana_ppal)

    
    texto_puntuacion(ventana_ppal,('score: '+ str(score)+' '),20,ANCHO_VENTANA-75,2)
    barra_vida(ventana_ppal,texto_puntuacion(ventana_ppal,'  vida: ',20,ANCHO_VENTANA-970,2),ANCHO_VENTANA-930,10,player.vidas)
    mostrar_nivel(nivel_actual)
    mostrar_cronometro(tiempo_restante)
    
    if not run:
        # Guardar el puntaje en la base de datos
        conn = sqlite3.connect("puntajes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO puntajes (nombre, score) VALUES (?, ?)", (player_name, score))
        conn.commit()
        conn.close()

    pygame.display.update()  
    Reloj.tick(fps) 

    pygame.display.flip()
pygame.quit()

#######3333333#########################################3##33333##############
#3##333333333333333333333333333333333333333###############################333
##########################################################################3##