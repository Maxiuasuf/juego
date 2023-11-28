import pygame, random
from musica_sonidos import *

ANCHO_VENTANA = 1000
ALTO_VENTANA = 720

#lista de fotos de la explosion
explosion_lista = []
for i in range(1,13):
    explosion = pygame.image.load(f"tp_video_juego.py/imagenes.py/explosion/{i}.png")
    explosion_lista.append(explosion)
    
burbuja_lista = []
for i in range(1,9):
    burbuja = pygame.image.load(f"tp_video_juego.py/imagenes.py/burbuja/{i}.png")
    burbuja_lista.append(burbuja)
    

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
#--------------------- METEOROS ----------------------------------------
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

#---------------------- NAVE ENEMIGA -----------------------------------
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

#----------------------------- BALAS ---------------------------------------------        
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

#----------------------- BALAS ENEMIGOS  --------------------
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

#------------------- EXPLOSION  ----------------------------------------------------------
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
#--------------------------- EXPLOSION BURBUJA -----------------------------------
class Burbuja(pygame.sprite.Sprite):
    def __init__(self,position,tamaño):
        super().__init__()
        self.image = burbuja_lista[0]
        img_scala = pygame.transform.scale(self.image,tamaño)
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_burbuja = 50
        self.frames = 0
        
    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_burbuja:
            self.time = tiempo
            self.frames +=1
            if self.frames == len(burbuja_lista):
                self.kill()
            else:
                position = self.rect.center
                self.image = burbuja_lista[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position 
#------------------------ ESTRELLA DE LA MUERTE -----------------------------------
class estrella_de_la_muerte(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/imagenes.py/estrelladelamuerte.png"), (250, 250))
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO_VENTANA // 2 - self.rect.width // 2
        self.rect.y = 5
        self.velocidad_y = 0  # Puedes ajustar la velocidad según sea necesario
        self.vidas = 1000
            # Configuracion para disparar
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.cadencia_disparo = 6000  # Tiempo en milisegundos entre disparos (10 segundos)        

    def update(self):
        self.rect.y += self.velocidad_y

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_disparo > self.cadencia_disparo:
            self.disparar()
            self.tiempo_ultimo_disparo = tiempo_actual

        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height
            
    def disparar(self):
        # Crea y agrega un proyectil automáticamente
        rayo_estrella = Hiperrayo(500, 240)
        grupo_balas_estrella.add(rayo_estrella)
        grupo_jugador.add(rayo_estrella)
        sonido_hiperrayo.play()

#----------------------- HIPER RAYO ----------------------------------
class Hiperrayo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load("tp_video_juego.py\imagenes.py\cañonazul.png") , (80, 170))
        #self.image.fill((255, 0, 0))  # Color rojo (puedes cambiar esto)
        self.rect = self.image.get_rect()
        
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad_y = 3 # Ajusta la velocidad del proyectil según sea necesario

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()  # Elimina el proyectil cuando sale de la pantalla

#-------------------------------------------------------------------------
class Moneda(pygame.sprite.Sprite):
    def __init__(self,x ,y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("tp_video_juego.py/imagenes.py/rebeldes.png"), (70, 100))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x =  random.randrange(1,ANCHO_VENTANA)
        self.rect.y =   0
        self.velocidad_y = random.randrange(1,3)


    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.y > ALTO_VENTANA:
            self.rect.y = -self.rect.height
            self.rect.x = random.randrange(1, ANCHO_VENTANA)
            self.velocidad_y = random.randrange(1, 2)


grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()

grupo_balas_estrella = pygame.sprite.Group()
grupo_balas_jugador= pygame.sprite.Group()
grupo_hiperrayo = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

grupo_explosiones = pygame.sprite.Group() 
grupo_burbujas = pygame.sprite.Group() 
grupo_estrella = pygame.sprite.Group() 

grupo_meteoros = pygame.sprite.Group()
grupo_monedas = pygame.sprite.Group()