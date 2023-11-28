import time
import pygame as pg
from pygame.locals import K_DOWN, K_UP, K_RIGHT, K_LEFT, K_SPACE, K_b, QUIT
from pygame.math import Vector2
import pygame
import random

ANCHO_VENTANA = 800
ALTO_VENTANA = 720

pygame.init()
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

# TITULO DE LA VENTANA
pygame.display.set_caption("                                                           **********STAR WARS***********")

class StarShip(pg.sprite.Sprite):

    def __init__(self, posicion=(0, 0)):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/xwing.png") , (100, 100))
        self.img = self.image
        self.rect = self.image.get_rect(center=posicion)
        self.posicion = Vector2(posicion)
        self.velocidad = Vector2(0,  0)
        self.x_vel = Vector2(0,  7)
        self.y_vel = Vector2(4,  0)

        self.cadencia_torpedo = 1
        self.cadencia_laser = 0.4

        self.proyectiles = pg.sprite.Group()

        self._t_ultimo_laser = time.time()
        self._t_ultimo_torpedo = time.time()


    def update(self):
        keys = pg.key.get_pressed()
        self.velocidad = (0,  0)
        
        if keys[K_LEFT]:
            self.velocidad += -self.y_vel
        if keys[K_RIGHT]:
            self.velocidad += self.y_vel
        if keys[K_SPACE]:
            now_time = time.time()
            if now_time - self._t_ultimo_laser >= self.cadencia_laser:
                self._t_ultimo_laser = now_time
                self.proyectiles.add(
                    Laser(Vector2(self.rect.x + 35,  self.rect.y + 110)), 
                    Laser(Vector2(self.rect.x + 62,  self.rect.y + 95)), 
                    Laser(Vector2(self.rect.x + 137,  self.rect.y + 95)), 
                    Laser(Vector2(self.rect.x + 160,  self.rect.y + 110))
                    )
        if keys[K_b]:
            now_time = time.time()
            if now_time - self._t_ultimo_torpedo >= self.cadencia_torpedo:
                self._t_ultimo_torpedo = now_time
                self.proyectiles.add(
                    Torpedo(Vector2(self.rect.center))
                    )
        self.posicion +=  self.velocidad
        self.rect.center = self.posicion
        self.proyectiles.update()


class Torpedo(pg.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/rayo_laser_rojo.png") , (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.posicion = posicion
        self.velocidad = Vector2(0,  -10)    

    def update(self):
        self.posicion += self.velocidad
        self.rect.center = self.posicion
        # Destruir cuando se salga de la ventana (superior)
        if self.rect.bottom < 0:    
            self.kill()   

class Laser(pg.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.image = pg.transform.scale(
            pg.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/rayo_laser.png") , (30, 30)
        )
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.posicion = posicion
        self.velocidad = Vector2(0,  -15)    

    def update(self):
        self.posicion += self.velocidad
        self.rect.center = self.posicion
        # Destruir cuando se salga de la ventana (superior)
        if self.rect.bottom < 0:    
            self.kill()   
    

class EnemyShip(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/tie figther.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = Vector2(position)
        self.velocity = Vector2(0, 2)  # Velocidad de movimiento hacia abajo
        self.last_shoot_time = time.time()
        self.shoot_delay = random.uniform(1.0, 2.0)  # Cadencia de disparo aleatoria

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position

        # Destruir cuando se salga de la ventana (parte inferior)
        if self.rect.top > ALTO_VENTANA:
            self.kill()

        now_time = time.time()
        if now_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = now_time
            self.shoot_laser()


def main():
    pg.init()
    ventana = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    star_ship = StarShip((ANCHO_VENTANA / 2, ALTO_VENTANA / 2))
    star_ship_grp = pg.sprite.GroupSingle(star_ship)

    clock = pg.time.Clock()
    while True:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                break
        star_ship_grp.update()
        ventana.fill((0,  0,  0))
        star_ship.proyectiles.draw(ventana)
        star_ship_grp.draw(ventana)

        pg.display.flip()


if __name__ == '__main__':
    main()
    
    
pygame.display.flip()
pygame.quit()