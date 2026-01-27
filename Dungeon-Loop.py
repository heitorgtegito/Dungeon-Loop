# 13 7 16 6 20 15 -> Importante!

import pygame

pygame.init() # inicia o pygame
janela = pygame.display.set_mode((1280, 720)) # Cria janela, tamanho 1280x720
clock = pygame.time.Clock() # Objeto q controla o fps
running = True


while running == True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False


    janela.fill((255, 255, 255))
    pygame.display.flip() # Desenha a tela atual 
    clock.tick(60) # 60fps isso dai

pygame.quit()
