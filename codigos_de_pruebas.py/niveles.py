
import random
import pygame
# Inicializar
pygame.init()

# Medidas
ANCHO = 1280
ALTO = 720

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)


# Funciones

def colision(x1, y1, a1, b1, x2, y2, a2, b2, ex=0):
    if x1 + a1 > x2 + ex and \
       x1 + ex < x2 + a2 and \
       y1 + b1 > y2 + ex and \
       y1 + ex < y2 + b2:
        return True
    else:
        return False


# Ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente1 = pygame.font.SysFont("arial black", 24)
fuente2 = pygame.font.SysFont("Segoe print", 32)

# Carga imágenes
fondo = pygame.image.load("fondo.png").convert()
nave_arr = pygame.image.load("nave_arriba.png").convert_alpha()
nave_abj = pygame.image.load("nave_abajo.png").convert_alpha()
nave_izq = pygame.image.load("nave_izquierda.png").convert_alpha()
nave_der = pygame.image.load("nave_derecha.png").convert_alpha()

aste_1a = pygame.image.load("asteroide_1a.png").convert_alpha()
aste_1b = pygame.image.load("asteroide_1b.png").convert_alpha()
aste_1c = pygame.image.load("asteroide_1c.png").convert_alpha()
aste_1d = pygame.image.load("asteroide_1d.png").convert_alpha()

aste_1 = [aste_1a, aste_1b, aste_1c, aste_1d]
aste_3 = [aste_1b, aste_1c, aste_1d, aste_1a]
aste_4 = [aste_1c, aste_1d, aste_1a, aste_1b]
aste_5 = [aste_1d, aste_1a, aste_1b, aste_1c]

aste_2a = pygame.image.load("asteroide_2a.png").convert_alpha()
aste_2b = pygame.image.load("asteroide_2b.png").convert_alpha()
aste_2c = pygame.image.load("asteroide_2c.png").convert_alpha()
aste_2d = pygame.image.load("asteroide_2d.png").convert_alpha()

aste_2 = [aste_2a, aste_2b, aste_2c, aste_2d]
aste_6 = [aste_2b, aste_2c, aste_2d, aste_2a]
aste_7 = [aste_2c, aste_2d, aste_2a, aste_2b]
aste_8 = [aste_2d, aste_2a, aste_2b, aste_2c]



# Bucle principal

en_juego = True
while en_juego:

    num_vidas = 3
    num_nivel = 1

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

        ventana.fill(NEGRO)

        historia = [
            "                      MISIÓN A JUPITER",
            "     Tras meses de viaje en misión a Júpiter ya sólo se",
            "    interponen en tu camino tres cinturones de asteroides",
            "  que te dificultan el paso y amenazan con no dejarte pasar.",
            "   Intenta traspasarlos para conseguir finalizar tu misión.",
            "",
            "                Pulsa 'ENTER' para empezar"
            ]

        y = 80
        for frase in historia:
            texto = fuente2.render(frase, True, BLANCO)
            ventana.blit(texto, (150, y))
            y += 80

        pygame.display.update()


    while en_partida:

        en_final = False

        num_aste_grandes = num_nivel * 5
        num_aste_pequenios = num_nivel * 10

        asteroides_grandes = []
        asteroides_pequenios = []

        for i in range(num_aste_grandes):
            x = random.randint(0, ANCHO)
            y = random.randint(50, ALTO-120)
            v = random.randint(1, 3)
            f = random.choice([aste_1, aste_3, aste_4, aste_5])
            a = [f, x, y, v]
            asteroides_grandes.append(a)
            
        for i in range(num_aste_pequenios):
            x = random.randint(0, ANCHO)
            y = random.randint(50, ALTO-120)
            v = random.randint(1, 4)
            f = random.choice([aste_2, aste_6, aste_7, aste_8])
            a = [f, x, y, v]
            asteroides_pequenios.append(a)

        asteroides = asteroides_grandes + asteroides_pequenios


        nave_pos_x = 600
        nave_pos_y = 670
        nave_vel_x = 0
        nave_vel_y = 0
        direccion = "arriba"

        frames_asteroides = 0


        en_nivel = True
        while en_nivel:

            reloj.tick(60)
    
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_nivel = False
                    en_partida = False
                    en_juego = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        direccion = "derecha"
                        nave_vel_x = 2
                    if event.key == pygame.K_LEFT:
                        direccion = "izquierda"
                        nave_vel_x = -2
                    if event.key == pygame.K_DOWN:
                        direccion = "abajo"
                        nave_vel_y = 2
                    if event.key == pygame.K_UP:
                        direccion = "arriba"
                        nave_vel_y = -2

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        nave_vel_x = 0
                    if event.key == pygame.K_LEFT:
                        nave_vel_x = 0
                    if event.key == pygame.K_DOWN:
                        nave_vel_y = 0
                    if event.key == pygame.K_UP:
                        nave_vel_y = 0

            # Lógica
      
            for a in asteroides_grandes:
                a[1] += a[3]
                if a[1] > ANCHO:
                    a[1] = -64

            for a in asteroides_pequenios:
                a[1] += a[3]
                if a[1] > ANCHO:
                    a[1] = -32


            nave_pos_x += nave_vel_x
            nave_pos_y += nave_vel_y

            if nave_pos_x > ANCHO - 32:
                nave_pos_x = ANCHO - 32
            if nave_pos_x < 0:
                nave_pos_x = 0
            if nave_pos_y > ALTO - 32:
                nave_pos_y = ALTO - 32

            if nave_pos_y < 10:
                en_nivel = False
                num_nivel += 1
                

            for a in asteroides_grandes:
                if colision(a[1], a[2], 64, 64, nave_pos_x, nave_pos_y, 32, 32, 15):
                    en_nivel = False
                    num_vidas -= 1

            for a in asteroides_pequenios:
                if colision(a[1], a[2], 32, 32, nave_pos_x, nave_pos_y, 32, 32, 15):
                    en_nivel = False
                    num_vidas -= 1


            if num_vidas == 0:
                ganando = False
                en_final = True

            if num_nivel > 3:
                ganando = True
                en_final = True


            # Imágenes
            
            ventana.blit(fondo, (0,0))

            texto1 = fuente1.render("Nivel: " + str(num_nivel), True, BLANCO)
            texto2 = fuente1.render("Vidas: " + str(num_vidas), True, BLANCO)
            ventana.blit(texto1, (20,10))
            ventana.blit(texto2, (1150, 10))


            frames_asteroides += 1
            if frames_asteroides >= 41:
                frames_asteroides = 1
                
            if frames_asteroides < 11:
                for a in asteroides:
                    ventana.blit(a[0][0], (a[1], a[2]))
            elif frames_asteroides < 21:
                for a in asteroides:
                    ventana.blit(a[0][1], (a[1], a[2]))
            elif frames_asteroides < 31:
                for a in asteroides:
                    ventana.blit(a[0][2], (a[1], a[2]))
            elif frames_asteroides < 41:
                for a in asteroides:
                    ventana.blit(a[0][3], (a[1], a[2]))

            if direccion == "arriba":    
                ventana.blit(nave_arr, (nave_pos_x, nave_pos_y))
            elif direccion == "abajo":    
                ventana.blit(nave_abj, (nave_pos_x, nave_pos_y))
            elif direccion == "izquierda":    
                ventana.blit(nave_izq, (nave_pos_x, nave_pos_y))
            elif direccion == "derecha":    
                ventana.blit(nave_der, (nave_pos_x, nave_pos_y))


            pygame.display.update()



        while en_final:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_final = False
                    en_partida = False
                    en_juego = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        en_final = False
                        en_partida = False
                        en_juego = False

                    if event.key == pygame.K_s:
                        en_final = False
                        en_partida = False
                    
                    
            ventana.fill(NEGRO)

            historia_perdido = [
                "    No has conseguido llegar a Júpiter. Los cinturones",
                "   de asteroides han destruido tu nave. Pero has tenido",
                "   suerte y te han recogido unos chatarreros del espacio.",
                "  ¿Quieres volverlo a intentar a borde de una nueva nave?",
                "",
                "              Pulsa 's' para volverlo a intentar",
                "              Pulsa 'n' para salir del juego"]

            historia_ganado = [
                "  Has conseguido llegar a Júpiter y completar tu misión.",
                "  Los cinturones de asteroides no han conseguido pararte.",
                "       Te has convertido en un héroe del espacio.",
                "       ¿Quieres embarcarte en una nueva misión?",
                "", 
                "              Pulsa 's' para volver a jugar",
                "              Pulsa 'n' para salir del juego"]


            if ganando:
                historia = historia_ganado
            else:
                historia = historia_perdido

            y = 80
            for frase in historia:
                texto = fuente2.render(frase, True, BLANCO)
                ventana.blit(texto, (150, y))
                y += 80

            pygame.display.update()


pygame.quit()