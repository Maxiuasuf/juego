import pygame


pygame.mixer.init()  # Inicializar el módulo de sonido

sonido_laser = pygame.mixer.Sound("tp_video_juego.py\sonidos.py\sonido_laser_w.mpeg")
sonido_laser.set_volume(1.0)
sonido_colision = pygame.mixer.Sound("C:/Users/maxi/Desktop/programacion 1 2023/tp_video_juego.py/sonidos.py/golpe.wav")
sonido_colision.set_volume(0.8)  # Ajusta el volumen según tus preferencias
sonido_explosion = pygame.mixer.Sound("tp_video_juego.py/sonidos.py/explosion.wav")
sonido_activado = True
# Añadir sonido al ingreso de caracteres en el input
sonido_tecla = pygame.mixer.Sound("tp_video_juego.py/sonidos.py/corto.wav")
sonido_tecla.set_volume(1.5)  # Ajusta el volumen según tus preferencias

sonido_hiperrayo = pygame.mixer.Sound("tp_video_juego.py\sonidos.py\hiper.mpeg")
sonido_hiperrayo.set_volume(15.0)

sonido_energia = pygame.mixer.Sound("tp_video_juego.py/sonidos.py/r2d2.mp3")
sonido_energia.set_volume(10.0)