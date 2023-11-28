if primer_nivel:
        nivel_uno()
        
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
        
        
#NIVEL 2  
        if tiempo_restante == 0 and player.vidas >= 1:
            if nivel_actual == 1 and not segundo_nivel:
                nivel_actual += 1
                segundo_nivel = True
                primer_nivel = False
                pantalla_nivel_dos(ventana_ppal)
                tiempo_inicial = pygame.time.get_ticks()
                player.vidas = 100
    elif segundo_nivel:
        nivel_dos()
        '''    
        Reloj.tick(fps)

        y_relativa = y % fondo.get_rect().height
        ventana_ppal.blit(fondo,(0,y_relativa - fondo.get_rect().height))

        if(y_relativa < ALTO_VENTANA):
            ventana_ppal.blit(fondo,(0,y_relativa))
        y += 10
        '''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.disparar() 
        
        for enemigo in grupo_enemigos_nivel_dos:
                        if enemigo.rect.top > ALTO_VENTANA:
                            enemigo.rect.y = 0
                            enemigo.rect.x = random.randint(1, ANCHO_VENTANA - 50)
        
        grupo_estrella.update()
        grupo_jugador_nivel_dos.update()
        grupo_enemigos_nivel_dos.update()
        grupo_balas_jugador_nivel_dos.update()
        grupo_jugador_nivel_dos.draw(ventana_ppal)

#grupo_jugador_nivel_dos.draw(ventana_ppal)
#NIVEL 3
        
        if tiempo_restante == 0 and player.vidas >=1:
            if nivel_actual == 2 and not tercer_nivel:
                nivel_actual += 1
                tercer_nivel = True
                segundo_nivel = False
                pantalla_nivel_tres(ventana_ppal)
                tiempo_inicial = pygame.time.get_ticks()
                player.vidas = 100
    elif tercer_nivel:
        nivel_tres()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.disparar() 
        for estrella in grupo_estrella:
                        if enemigo.rect.top > ALTO_VENTANA:
                            print("forgrupoestrella")
                            enemigo.rect.y = 0
                            enemigo.rect.x = random.randint(1, ANCHO_VENTANA - 50)
        grupo_jugador_nivel_tres.update()
        grupo_enemigos_nivel_tres.update()
        grupo_balas_jugador_nivel_tres.update()
        grupo_jugador_nivel_tres.draw(ventana_ppal)
    ############################ actualizacion de grupos #######################            
    #grupo_jugador_nivel_tres.update()
    
    #grupo_enemigos_nivel_tres.update()
    
    
    
    #grupo_jugador_nivel_tres.draw(ventana_ppal)

    grupo_jugador.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    grupo_jugador.draw(ventana_ppal)