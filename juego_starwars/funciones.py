import pygame,sys
from colores import *
import re
import random
from pygame.locals import  QUIT
from musica_sonidos import *
import sqlite3
from objetos import *
from constantes import *
from musica_sonidos import *
from colores import *
from objetos import *
from funciones import *
from fondos import *
from constantes import *

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720

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

x = 0
y = 0

#------------------------ FUNCIONES -------------------------------------------------

def texto_puntuacion(frame,text,size,x,y):
    '''
    muestra la puntuacion en pantalla al momento del juego, recibe un frame(donde se ubica el 
    texto),el texto, el tamaño y las coordenada en la pantalla.
    '''
    font = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf",size)
    texto_frame = font.render(text,True,blanco,negro)
    text_rect = texto_frame.get_rect()
    text_rect.midtop = (x,y)
    frame.blit(texto_frame,text_rect)
    
#-------------------------barra de vidas-----------------------------------    
def barra_vida(frame,str,x,y,nivel):
    '''
    barra de vida en la pantalla de juego con una longitud de 100 vidas.
    recibe el un frame, un texto(opcional), las coordenadas en la pantalla, y el 
    nivel actual.
    
    '''
    longitud = 100
    alto = 20
    fill = int((nivel/100)*longitud)
    border = pygame.Rect(x,y,longitud,alto)
    fill = pygame.Rect(x,y,fill,alto)
    pygame.draw.rect(frame,green,fill)
    pygame.draw.rect(frame,blanco,border,2)
#-------------------------cronometro-----------------------------
def mostrar_cronometro(tiempo_restante):
    '''
    muestra el tiempo restante en el juego. y se ubica en el centro arriba.
    '''
    fuente_cronometro = pygame.font.Font("tp_video_juego.py/tipografia.py\Starjedi.ttf", 30)
    texto_cronometro = fuente_cronometro.render(f"{tiempo_restante}", True, blanco)
    rect_cronometro = texto_cronometro.get_rect(center=(ANCHO_VENTANA // 2, 30))
    ventana_ppal.blit(texto_cronometro, rect_cronometro)

#------------------------primer pantalla-------------------------
def pantalla_inicial(screen):
    '''se inicia muestra una imagen 
    luego se debe apreta enter para pasar al menu.
    '''
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
#------------------------ menu principal -----------------------------------------------
def nombre_en_menu(screen):
    
    '''
    Permite al jugador ingresar su nombre en el menu inicial del juego.recibe
    screen: (Surface) de Pygame que representa la ventana del juego.
    Muestra un título de bienvenida, un subtitulo para ingresar el nombre, un campo de entrada de texto 
    y botones para jugar y ver el ranking.
    Controla el botón de sonido para activar/desactivar la musica.
    Retorna el nombre del jugador ingresado.
    Si el nombre ingresado no es valido, muestra un mensaje de error.
    '''
    global sonido_activado
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
                        mensaje_error = "Texto no valido. Ingrese solo letras y numeros."
                        texto_ingresado = ''
                        
            # Controla clic en el botón de sonido
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
#-----------------------pantalla game over----------------------------------------
def pantalla_game_over(score):
    '''
    Muestra la pantalla de "Game Over" con la puntuación del jugador y opciones para volver a jugar o salir.
    recibe el score, tiene una musica predeterminada anunciando que se perdio.

    '''
    pygame.mixer.music.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/sonidos.py/darth vader.mp3")  # Detener la música de fondo
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    fuente_game_over = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    game_over_texto = fuente_game_over.render("game over", True, (255, 0, 0))
    game_over_rect = game_over_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    score_texto = fuente_game_over.render(f"Puntuación: {score}", True, (255, 255, 255))
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))

    #volver_a_jugar_fuente = pygame.font.Font(None, 36)
   # volver_a_jugar_texto = volver_a_jugar_fuente.render("Volver a Jugar", True, (255, 255, 255))
    #volver_a_jugar_rect = volver_a_jugar_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 120))
    
    salir_fuente = pygame.font.Font(None, 36)
    salir_texto = salir_fuente.render("Salir", True, (255, 255, 255))
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 160))
    
    ventana_ppal.blit(game_over_texto, game_over_rect)
    #ventana_ppal.blit(volver_a_jugar_texto, volver_a_jugar_rect)
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
                if salir_rect.collidepoint(event.pos):  # Verifica si el clic está dentro de salir_rect
                    pygame.quit()
                    sys.exit()

#--------------------- PANTALLA NIVEL -------------------------------------
def pantalla_nivel(screen, nivel, mision):
    '''
    Muestra una pantalla informativa del nivel con el numero de nivel y 
    la mision del nivel. recibe una superficie, el numero de nivel(int) y la mision(str)
    '''
    font_titulo = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 20)
    font_indicacion = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tipografia.py/Starjedi.ttf", 18)

    titulo_texto = font_titulo.render(f"Nivel {nivel}", True, amarillo)
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render(mision, True, (255, 255, 255))
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

#---------------PANTALLA WINS------------------------------------------------------
def pantalla_victoria(nombre_jugador,score):
    '''
    Muestra la pantalla de victoria con un mensaje y la puntuacion.
    recibe el nombre del jugador y el score.
    reproduce musica y da la opcion de salir o volver a jugar

    '''
    pygame.mixer.music.load("tp_video_juego.py/sonidos.py/obiwan.mp3")  # Cambiar la música de fondo según sea necesario
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito
    pygame.mixer.music.set_volume(0.8)
    
    fuente_victoria = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py//tipografia.py/Starjedi.ttf", 60)
    victoria_texto = fuente_victoria.render(f"you win, {nombre_jugador}!", True, amarillo)
    victoria_rect = victoria_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 30))
    
    fuente_victoria = pygame.font.Font("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py//tipografia.py/Starjedi.ttf", 20)
    score_texto = fuente_victoria.render(f"Puntuación: {score}", True, blanco)
    score_rect = score_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 80))
    
    fondo_blanco = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
    fondo_blanco.fill(negro)
    
    #volver_jugar_fuente = pygame.font.Font(None, 36)
    #volver_jugar_texto = volver_jugar_fuente.render("Volver a Jugar", True, (255, 255, 255))
   # volver_jugar_rect = volver_jugar_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 30))
    
    salir_fuente = pygame.font.Font(None, 36)
    salir_texto = salir_fuente.render("Salir", True, (255, 255, 255))
    salir_rect = salir_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 100))
    
   
   # ventana_ppal.blit(volver_jugar_texto, volver_jugar_rect)
    
    
    ventana_ppal.blit(fondo_blanco, (0, 0))  # Dibujar el fondo blanco en la posición (0, 0)
    ventana_ppal.blit(victoria_texto, victoria_rect)
    ventana_ppal.blit(salir_texto, salir_rect)
    ventana_ppal.blit(score_texto, score_rect)
    pygame.display.flip()
    
    pygame.display.flip()

 
    esperando_evento = True
    while esperando_evento:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if salir_rect.collidepoint(event.pos):  # Verifica si el clic está dentro de salir_rect
                    pygame.quit()
                    sys.exit()
#----------------------------------------------------------------------------------
def manejar_ingreso_texto(texto_ingresado, event):
    '''
    Gestiona el ingreso de texto por parte del usuario, recibe
    texto_ingresado y el evento del teclado- le agrega sonido tbm
    '''
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
    '''
    Muestra los mejores 5 puntajes almacenados en la base de datos y 
    espera a que el usuario cierre la ventana o presione Esc.
    '''
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
    '''
    muestra el nivel estando en la partida en el costado izquierdo inferior.
    recibe el paramentro nivel.
    '''
    font = pygame.font.Font(None, 20)
    texto = font.render(f"Nivel: {nivel}", True, blanco)
    ventana_ppal.blit(texto, (10, ALTO_VENTANA - 30))

#---------------------------- MOVIMIENTO DE FONDO ---------------------------------   
def movimiento_fondo(imagen):
    '''
    Realiza el movimiento vertical del fondo en el juego.
    recibe una imagen para utilizar en el fondo de la pantalla.
    '''
    global y
    # Movimiento del fondo
    y_relativa = y % imagen.get_rect().height
    ventana_ppal.blit(imagen,(0,y_relativa - imagen.get_rect().height))

    if(y_relativa < ALTO_VENTANA):
        ventana_ppal.blit(imagen,(0,y_relativa))
    y += 6

#--------------------------------- NIVELES ------------------------------------------
def nivel_uno():
    for x in range(5):
                meteoritos = Meteoros(random.randint(-10, ANCHO_VENTANA),- 10)
                grupo_meteoros.add(meteoritos)
                grupo_jugador.add(meteoritos)
    for x in range(2):
                nueva_moneda = Moneda(random.randint(-10, ANCHO_VENTANA), -10)
                grupo_monedas.add(nueva_moneda)  
                grupo_jugador.add(nueva_moneda)   
def nivel_dos():  
    for x in range(7):
                enemigo = nave_enemiga(random.randint(-10, ANCHO_VENTANA), -10)
                grupo_enemigos.add(enemigo)
                grupo_jugador.add(enemigo)
def nivel_tres():
    for x in range(1):
                estrella = estrella_de_la_muerte(ANCHO_VENTANA//2, 0)
                grupo_estrella.add(estrella)
                grupo_jugador.add(estrella)

#------------------  ACTUALIZACION DE GRUPOS --------------------------------------------------------
def grupos_update():
    '''
    actualiza los grupos de los sprites.
    '''
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    grupo_balas_estrella.update()
        
    grupo_hiperrayo.update()
    grupo_estrella.update()
    grupo_meteoros.update()
    grupo_monedas.update()
    
    grupo_jugador.update()
    grupo_jugador.draw(ventana_ppal)
    
#-------------- BASE DE DATOS --------------------------
def abrir_base_de_datos():
    '''
    abre la base de datos con nombre puntuacion.
    si no existe la crea.
    '''
    conn = sqlite3.connect("puntuacion.db")
    cursor = conn.cursor()
    # Creo la tabla de puntajes si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS puntuacion (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, score INTEGER    )''')
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()