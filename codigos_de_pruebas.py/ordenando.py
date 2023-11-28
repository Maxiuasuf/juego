import time
import pygame
import random
from pygame.locals import K_RIGHT, K_LEFT, K_SPACE, K_b, QUIT
from pygame.math import Vector2
import re

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720
nivel_actual = 1
DURACION_NIVEL = 60
tiempo_inicial = None
cronometro_iniciado = False

pygame.mixer.init()

sonido_torpedo = pygame.mixer.Sound("tp_video_juego.py/sonido laser.mp3")
sonido_torpedo.set_volume(0.9)
sonido_laser = pygame.mixer.Sound("tp_video_juego.py/disparo original star wars.mp3")
sonido_laser.set_volume(0.7)
sonido_colision = pygame.mixer.Sound("tp_video_juego.py/golpe.wav")
sonido_colision.set_volume(0.5)

def pantalla_inicial(screen):
    imagen_inicial = pygame.image.load("tp_video_juego.py/wall4.jpg")
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

def mostrar_pantalla_nivel(ventana, nivel):
    font_titulo = pygame.font.Font("tp_video_juego.py/Starjedi.ttf", 40)
    font_mision = pygame.font.Font("tp_video_juego.py/Starjedi.ttf", 24)

    titulo_texto = font_titulo.render(f"Nivel {nivel}", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 50))

    mision_texto = font_mision.render("Descripción del nivel", True, (255, 255, 255))
    mision_rect = mision_texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 50))

    ventana.fill((0, 0, 0))
    ventana.blit(titulo_texto, titulo_rect)
    ventana.blit(mision_texto, mision_rect)
    pygame.display.flip()

    esperando_input = True
    while esperando_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                esperando_input = False
                break

def nombre_en_menu(screen):
    nombre = ""
    font = pygame.font.Font("tp_video_juego.py/Starjedi.ttf", 26)
    input_rect = pygame.Rect(400, 155, 140, 50)
    color_inactivo = pygame.Color((255, 165, 0))
    color_activo = pygame.Color((255, 255, 0))
    color = color_inactivo
    activo = False
    texto_ingresado = ''
    mensaje_error = ''
    reloj = pygame.time.Clock

    titulo_fuente = pygame.font.Font("tp_video_juego.py/Starjedi.ttf", 30)
    titulo_texto = titulo_fuente.render("$ Bienvenido a combatir contra el imperio $", True, (255, 255, 255))
    titulo_rect = titulo_texto.get_rect(center=(ANCHO_VENTANA // 2, 90))

    subtitulo_font = pygame.font.Font("tp_video_juego.py/Starjedi.ttf", 20)
    subtitulo_text = subtitulo_font.render("ingresa tu nombre", True, (255, 255, 255))
    subtitulo_rect = subtitulo_text.get_rect(center=(ANCHO_VENTANA // 2, input_rect.y - 20))

    imagen_abajo = pygame.image.load("tp_video_juego.py/loguito.png")
    imagen_rect = imagen_abajo.get_rect()
    imagen_rect.center = (ANCHO_VENTANA // 2, input_rect.bottom + 285)

    fuente_boton = pygame.font.Font(None, 30)
    texto_boton = fuente_boton.render(" INGRESAR ", True, (255, 255, 255))
    rect_boton = texto_boton.get_rect(center=(ANCHO_VENTANA // 2, input_rect.bottom + 20))

    pygame.mixer.music.load("tp_video_juego.py/Star Wars Main Theme (Full) (128 kbps).mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

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

        screen.fill((30, 30, 30))
        screen.blit(titulo_texto, titulo_rect)
        screen.blit(subtitulo_text, subtitulo_rect)
        txt_surface = font.render(texto_ingresado, True, color)
        width = max(200, txt_surface.get_width() + 90)
        input_rect.w = width
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, color, input_rect, 5)

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

pygame.init()
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("   STAR WARS   ")

class nave_rebelde(pygame.sprite.Sprite):
    def __init__(self, posicion=(0, 0)):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("tp_video_juego.py/xwing.png"), (120, 120))
        self.img = self.image
        self.rect = self.image.get_rect(center=(posicion[0], ALTO_VENTANA - 60))
        self.posicion = Vector2(self.rect.center)
        self.velocidad = Vector2(0, 0)
        self.x_vel = Vector2(0, 12)
        self.y_vel = Vector2(4, 0)
        self.vidas = 3
        self.cadencia_torpedo = 2.5
        self.cadencia_laser = 0.8
        self.proyectiles = pygame.sprite.Group()
        self._t_ultimo_laser = time.time()
        self._t_ultimo_torpedo = time.time()
        self.score = 0

    def iniciar(self, nombre):
        self.nombre = nombre

    def mover(self, direccion):
        if direccion == "derecha":
            self.velocidad += self.y_vel
        if direccion == "izquierda":
            self.velocidad += -self.y_vel

        self.posicion += self.velocidad
        self.posicion.x = max(66, min(ANCHO_VENTANA - 66, self.posicion.x))
        self.rect.center = self.posicion
        self.proyectiles.update()

    def disparar(self):
        este_momento = time.time()
        if este_momento - self._t_ultimo_laser >= self.cadencia_laser:
            self._t_ultimo_laser = este_momento
            self.proyectiles.add(
                Laser(Vector2(self.rect.x + 5, self.rect.y + 110)),
                Laser(Vector2(self.rect.x + 110, self.rect.y + 110))
            )
            sonido_laser.play()

    def torpedo(self):
        este_momento = time.time()
        if este_momento - self._t_ultimo_torpedo >= self.cadencia_torpedo:
            self._t_ultimo_torpedo = este_momento
            self.proyectiles.add(
                Torpedo(Vector2(self.rect.center))
            )
            sonido_torpedo.play()

    def update(self):
        self.posicion += self.velocidad
        self.rect.center = self.posicion
        self.proyectiles.update()

class Torpedo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("tp_video_juego.py/rayo_laser_rojo.png"), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.posicion = posicion
        self.velocidad = Vector2(0, -10)

    def update(self):
        self.posicion += self.velocidad
        self.rect.center = self.posicion
        if self.rect.bottom < 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init()
        self.image = pygame.transform.scale(pygame.image.load("tp_video_juego.py/rayolaser_verde.png"), (70, 80))
        self.rect = self.image.get_rect(center=(posicion[0], ALTO_VENTANA - 100))
        self.rect.center = posicion
        self.posicion = Vector2(self.rect.center)
        self.velocidad = Vector2(0, -15)

    def update(self):
        self.posicion += self.velocidad
        self.rect.center = self.posicion
        if self.rect.bottom < 0:
            self.kill()

class nave_enemiga(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("tp_video_juego.py/tie figther.png"), (80, 70))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = Vector2(position)
        self.velocity = Vector2(0, 2)
        self.last_shoot_time = time.time()
        self.shoot_delay = random.uniform(1.0, 2.0)

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position
        if self.rect.top > ALTO_VENTANA:
            self.kill()

        este_momento = time.time()
        if este_momento - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = este_momento
            self.shoot_laser()

    def shoot_laser(self):
        enemy_laser = Laser(self.position)
        enemy_laser.velocidad = Vector2(0, 10)
        nave_propia.proyectiles.add(enemy_laser)

def main():
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    reloj = pygame.time.Clock()
    jugador = nave_rebelde(ventana)
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(jugador)
    disparos = pygame.sprite.Group()
    torpedos = pygame.sprite.Group()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.mover("izquierda")
        if keys[pygame.K_RIGHT]:
            jugador.mover("derecha")
        if keys[pygame.K_SPACE]:
            jugador.disparar()
        if keys[pygame.K_b]:
            jugador.torpedo()

        jugador.update()

        if random.random() < 0.02:
            enemigo = nave_enemiga(ventana)
            todos_los_sprites.add(enemigo)

        for enemigo in todos_los_sprites:
            enemigo.update()

        ventana.fill((0, 0, 0))
        todos_los_sprites.draw(ventana)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()