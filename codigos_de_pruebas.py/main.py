import pygame
import colores
import naves_enemigas
import nave_rebelde

ANCHO_VENTANA = 700
ALTO_VENTANA = 700

pygame.init()

# TAMAO DE LA VENTANA
ventana_ppal = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

# TITULO DE LA VENTANA
pygame.display.set_caption("      STAR WARS     ")

# TIMER
timer = pygame.USEREVENT + 0
pygame.time.set_timer(timer,100)

# CREACIN DE ELEMENTOS
player = nave_rebelde.crear(ANCHO_VENTANA/2,ALTO_VENTANA-100,100,100)
lista_naves_enemigas = naves_enemigas.crear_lista_naves_enemigas(20)


#LGICA DEL JUEGO
flag_run = True
while flag_run:

    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            flag_run = False

        if evento.type == pygame.USEREVENT:
            if evento.type == timer:
                naves_enemigas.update(lista_naves_enemigas)

    lista_teclas = pygame.key.get_pressed()

    if lista_teclas[pygame.K_LEFT] :
        nave_rebelde.update(player,-2)
    if lista_teclas[pygame.K_RIGHT] :
        nave_rebelde.update(player,2)
    

    #VOLCAR CAMBIOS
    ventana_ppal.fill(colores.BLANCO)
    nave_rebelde.actualizar_pantalla(player,ventana_ppal)
    naves_enemigas.actualizar_pantalla(lista_naves_enemigas,player,ventana_ppal)

    pygame.display.flip()
pygame.quit()