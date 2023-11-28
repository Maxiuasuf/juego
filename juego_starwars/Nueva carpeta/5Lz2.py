
import pygame ,sys
import random
from pygame.locals import  QUIT
import re
import sqlite3
from musica_sonidos import *
from colores import *


pygame.init()
pygame.mixer.init()  # Inicializar el módulo de sonido


#lista de fotos de la explosion
explosion_lista = []
for i in range(1,13):
    explosion = pygame.image.load(f"tp_video_juego.py/imagenes.py/explosion/{i}.png")
    explosion_lista.append(explosion)
    

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720
PANTALLA = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
fondo = pygame.image.load("tp_video_juego.py/imagenes.py/eclipse.jpg").convert()
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

fondo_nivel_dos = pygame.image.load("tp_video_juego.py/imagenes.py/space-1.png").convert()
fondo_nivel_dos = pygame.transform.scale(fondo_nivel_dos, (ANCHO_VENTANA, ALTO_VENTANA))

fondo_nivel_tres = pygame.image.load("tp_video_juego.py\imagenes.py\ojorojo.jpg").convert()
fondo_nivel_tres = pygame.transform.scale(fondo_nivel_tres, (ANCHO_VENTANA, ALTO_VENTANA))




x = 0
y = 0


# Duración del nivel en segundos (1 minuto)
DURACION_NIVEL = 15

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



# Cargar la imagen del icono
icono = pygame.image.load("tp_video_juego.py/imagenes.py/xwing.png")

# Establecer el icono de la ventana
pygame.display.set_icon(icono)

###################SQL#######################################
# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect("puntuacion.db")
cursor = conn.cursor()

# Crear la tabla de puntajes si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS puntuacion (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, score INTEGER    )''')

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
    fuente_cronometro = pygame.font.Font("tp_video_juego.py/tipografia.py\Starjedi.ttf", 30)
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
    font_titulo = pygame.font.Font("tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 20)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)
    
    titulo_texto = font_titulo.render("Nivel 1", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("Tu misión es eliminar la estrella de la muerte! ten mucho cuidado", True, amarillo)
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
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)


    titulo_texto = font_titulo.render("Nivel 2", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("ya saben que llegamos, cuidado el enemigo abrio fuego!", True, (255, 255, 255))
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

#-----------------------pantalla game over----------------------------------------
def pantalla_game_over():
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/sonidos.py/darth vader.mp3")  # Detener la música de fondo
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    fuente_game_over = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    game_over_texto = fuente_game_over.render("game over", True, (255, 0, 0))
    game_over_rect = game_over_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    score_texto = fuente_game_over.render(f"Puntuación: {score}", True, (255, 255, 255))
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))

    volver_a_jugar_fuente = pygame.font.Font(None, 36)
    volver_a_jugar_texto = volver_a_jugar_fuente.render("Volver a Jugar", True, (255, 255, 255))
    volver_a_jugar_rect = volver_a_jugar_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 80))
    
    salir_fuente = pygame.font.Font(None, 36)
    salir_texto = salir_fuente.render("Salir", True, (255, 255, 255))
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))
    
    ventana_ppal.blit(game_over_texto, game_over_rect)
    ventana_ppal.blit(volver_a_jugar_texto, volver_a_jugar_rect)
    ventana_ppal.blit(score_texto, score_rect)
    ventana_ppal.blit(salir_texto, salir_rect)
    pygame.display.flip()
    
    esperando_evento = True
    while esperando_evento:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if volver_a_jugar_rect.collidepoint(event.pos):
                    vida = 100
                    resetear_juego()
                    
                    esperando_evento = False  # Salir del bucle cuando se reinicia el juego
                elif salir_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    

#---------------------------------------------------------------------------------
def resetear_juego():
    global run, score,vida, nivel_actual, primer_nivel, segundo_nivel, tercer_nivel, tiempo_inicial

    vida = 100
    score = 0
    
    nivel_actual = 1
    primer_nivel = True
    segundo_nivel = False
    tercer_nivel = False
    tiempo_inicial = pygame.time.get_ticks()
    pantalla_nivel_uno(ventana_ppal)    
    run = True
    

#---------------PANTALLA WINS------------------------------------------------------
def pantalla_victoria(nombre_jugador,score):
    pygame.mixer.music.load("tp_video_juego.py/sonidos.py/obiwan.mp3")  # Cambiar la música de fondo según sea necesario
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    
    fuente_victoria = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py//tipografia.py/Starjedi.ttf", 60)
    victoria_texto = fuente_victoria.render(f"you win, {nombre_jugador}!", True, amarillo)
    victoria_rect = victoria_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    
    fuente_victoria = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py//tipografia.py/Starjedi.ttf", 20)
    score_texto = fuente_victoria.render(f"Puntuación: {score}", True, blanco)
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 80))
    
    
    volver_jugar_fuente = pygame.font.Font(None, 36)
    volver_jugar_texto = volver_jugar_fuente.render("Volver a Jugar", True, (255, 255, 255))
    volver_jugar_rect = volver_jugar_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))
    
    salir_fuente = pygame.font.Font(None, 36)
    salir_texto = salir_fuente.render("Salir", True, (255, 255, 255))
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
    
    ventana_ppal.blit(victoria_texto, victoria_rect)
    ventana_ppal.blit(volver_jugar_texto, volver_jugar_rect)
    ventana_ppal.blit(salir_texto, salir_rect)
    ventana_ppal.blit(score_texto,score_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volver_jugar_rect.collidepoint(event.pos):
                    run = True
                    resetear_juego()
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
    conn = sqlite3.connect("puntuacion.db")
    cursor = conn.cursor()

    # Seleccionar los 5 mejores puntajes
    cursor.execute("SELECT nombre, score FROM puntuacion ORDER BY score DESC LIMIT 5")
    top_puntajes = cursor.fetchall()
    
    conn.commit()

    # Crear una fuente para el texto
    font_ranking = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 30)
    font_salir = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 15)

    # Mostrar el título del ranking
    titulo_texto = font_ranking.render("# Top 5 Puntajes", True, negro)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 100))

    # Mostrar el título del ranking
    salir_texto = font_salir.render('Para salir presiona "esc"', True, negro)
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

    # Esperar a que el usuario cierre la ventana o presione Esc
    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Volver a la pantalla principal al presionar Esc

        pygame.display.flip()

#--------------------------------mostrar nivel------------------------------------
def mostrar_nivel(nivel):
    font = pygame.font.Font(None, 20)
    texto = font.render(f"Nivel: {nivel}", True, blanco)
    ventana_ppal.blit(texto, (10, ALTO_VENTANA - 30))

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
        self.velocidad_y = 0
        
        lista_teclas = pygame.key.get_pressed()
        if lista_teclas[pygame.K_LEFT]:
            self.velocidad_x = -5
        elif lista_teclas[pygame.K_RIGHT]:
            self.velocidad_x = 5
            
        if lista_teclas[pygame.K_UP]:
            self.velocidad_y = -5  # Modificar la velocidad vertical para subir
        elif lista_teclas[pygame.K_DOWN]:
            self.velocidad_y = 5 
        # Ajustar la posición para que la nave no salga de los límites
        self.rect.x += self.velocidad_x
        if self.rect.right > ANCHO_VENTANA:
            self.rect.right = ANCHO_VENTANA
        elif self.rect.left < 0:
            self.rect.left = 0
            
        self.rect.y += self.velocidad_y
        
        if self.rect.bottom > ALTO_VENTANA:
            self.rect.bottom = ALTO_VENTANA
        elif self.rect.top < 0:
            self.rect.top = 0
        
    def disparar(self):
        bala = Balas(self.rect.centerx,self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        sonido_laser.play()
#---------------------kamikaze----------------------------------------
class Meteoros(pygame.sprite.Sprite):
	def __init__(self,x,y):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load("tp_video_juego.py/imagenes.py/meteorito.png"),(random.randint(60, 80), random.randint(30, 120)))	
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(ANCHO_VENTANA - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 2)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > ALTO_VENTANA + 10 or self.rect.left < -25 or self.rect.right > ANCHO_VENTANA + 22 :
			self.rect.x = random.randrange(ANCHO_VENTANA - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)

#----------------------NAVE ENEMIGA-----------------------------------
class nave_enemiga(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/caza.png"), (90, 55))
        self.rect = self.image.get_rect()
        self.rect.x =  random.randrange(1,ANCHO_VENTANA)
        # self.rect.y =   0
        self.velocidad_y = random.randrange(1,5)


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
            #grupo_meteoros.add(bala)

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
        self.velocidad_y = 5
        
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > ALTO_VENTANA:
            self.kill()

#---------------EXPLOSION----------------------------------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self,position,tamaño):
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
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/estrelladelamuerte.png"), (220, 220))
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA // 2 - self.rect.width // 2
        self.rect.y = 5
        self.velocidad_y = 0  # Puedes ajustar la velocidad según sea necesario
        self.vidas = 1000
        
    def update(self):
        self.rect.y += self.velocidad_y  
        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height  


def movimiento_fondo(imagen):
    global y
     # Movimiento del fondo
    y_relativa = y % imagen.get_rect().height
    ventana_ppal.blit(imagen,(0,y_relativa - imagen.get_rect().height))

    if(y_relativa < ALTO_VENTANA):
        ventana_ppal.blit(imagen,(0,y_relativa))
    y += 6
###################################################################################
##################################LOGICA###########################################
###################################################################################

grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()

grupo_balas_jugador= pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

grupo_explosiones = pygame.sprite.Group()  
grupo_estrella = pygame.sprite.Group() 

grupo_meteoros = pygame.sprite.Group()

player = Jugador()
grupo_balas_jugador.add(player)
grupo_jugador.add(player)
pantalla_inicial(ventana_ppal)

def nivel_uno():
    for x in range(4):
                meteoritos = Meteoros(random.randint(0, ANCHO_VENTANA), 0)
                grupo_meteoros.add(meteoritos)
                grupo_jugador.add(meteoritos)
def nivel_dos():  

    for x in range(6):
                enemigo = nave_enemiga(random.randint(0, ANCHO_VENTANA), 0)
                grupo_enemigos.add(enemigo)
                grupo_jugador.add(enemigo)

def nivel_tres():
    for x in range(1):
                estrella = estrella_de_la_muerte(ANCHO_VENTANA//2, 0)
                grupo_estrella.add(estrella)
                grupo_jugador.add(estrella)
                
player_name = nombre_en_menu(ventana_ppal)
pantalla_nivel_uno(ventana_ppal) 
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
                
    for enemigo in grupo_enemigos:
            if enemigo.rect.top > ALTO_VENTANA:
                enemigo.rect.y = 0
    
                enemigo.rect.x = random.randint(1, ANCHO_VENTANA - 50)
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
            pantalla_game_over()

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
            pantalla_game_over()
            
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
            pantalla_game_over()
            
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
                pantalla_victoria(player_name,score)
                
                
                
#--------------------------------------------------------------------------
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
            if tiempo_restante == 0:
                segundo_nivel = False
                tercer_nivel = False
                primer_nivel = False
                pantalla_game_over()
        

    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
        
    grupo_estrella.update()
    grupo_meteoros.update()
    
    grupo_jugador.update()
    grupo_jugador.draw(ventana_ppal)

    texto_puntuacion(ventana_ppal,('score: '+ str(score)+' '),20,ANCHO_VENTANA-75,2)
    barra_vida(ventana_ppal,texto_puntuacion(ventana_ppal,'  vida: ',20,ANCHO_VENTANA-970,2),ANCHO_VENTANA-930,10,player.vidas)
    mostrar_nivel(nivel_actual)
    mostrar_cronometro(tiempo_restante)
    
    pygame.display.update()  
    Reloj.tick(fps) 

    pygame.display.flip()
pygame.quit()
sys.exit()

