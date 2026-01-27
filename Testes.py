import math
import pygame

pygame.init() # inicia o pygame
janela = pygame.display.set_mode((1280, 720)) # Cria janela, tamanho 1280x720
clock = pygame.time.Clock() # Objeto q controla o fps
running = True
Retry = False

#  Atributos
Forca = 0
Destreza = 0
Constituicao = 0
Sorte = 0

Vida = 10 + Constituicao
Vida_Atual = Vida

Sala = 0

def JogarNovamente():
    Forca = Forca/20
    Destreza = Destreza/20
    Constituicao = Constituicao/20
    Sorte = Sorte/20
    Sala = 0
    Vida = 10 + Constituicao
    Vida_Atual = Vida
    return Forca, Destreza, Constituicao, Sorte, Sala, Vida, Vida_Atual

def Escolhendo_Arma_e_Armadura():
    Armadura = 'Pesada' # 'Leve'
    Arma = 'Foice' # Espada Longa, Porrete, Machado, Florete e Adaga
    return Armadura, Arma

def Definindo_Defesa():
    if Armadura == 'Leve':
        Defesa = 2 + round(Constituicao/20)
    elif Armadura == 'Pesada':
        Defesa = 5 + round(Constituicao/15)
    Defesa_Atual = Defesa
    return Defesa, Defesa_Atual

def Definindo_Condicoes():
    Condicoes = []
    if 'Sangramento' in Condicoes:
        Vida_Atual = Vida_Atual - (Vida_Atual/50)
    if 'Envenenamento' in Condicoes:
        Vida_Atual = Vida_Atual - (Destreza/10)
    if 'Debilitado' in Condicoes:
        Defesa_Atual = Defesa - (Forca/10)
    return Condicoes, Vida_Atual, Defesa_Atual

def Tier_Inimigo():
    if Sala < 25:
        tier = 1
    elif 25 <= Sala < 50:
        tier = 2
    elif 50 <= Sala < 75:
        tier = 3
    elif 75 <= Sala < 100:
        tier = 4
    elif Sala == 100:
        tier = 5
    return tier

def Definindo_Inimigo():
    tier = Tier_Inimigo()
    if tier == 1:
        Vida_Inimigo = (Sala * 7) + 7 # 0-47 ----- 14 de vida ---- 182 de vida
        Vida_Inimigo_Atual = Vida_Inimigo
        Defesa_Inimigo = math.ceil(Sala/5) + 1 # ---- 2 de defesa --- 6 de defesa
        Defesa_Inimigo_Atual = Defesa_Inimigo
        Dano_Inimigo = Sala * 3  # ---- 3 de dano ---- 75 de dano
    elif tier == 2:
        Vida_Inimigo = (Sala * 7) + 7 # 47-87
        Vida_Inimigo_Atual = Vida_Inimigo
        Defesa_Inimigo = math.ceil(Sala/4) + 3 # ---- 2 de defesa
        Defesa_Inimigo_Atual = Defesa_Inimigo
        Dano_Inimigo = Sala * 3
    elif tier == 3:
        Vida_Inimigo = (Sala * 8) + 8 # 87-127
        Vida_Inimigo_Atual = Vida_Inimigo
        Defesa_Inimigo = math.ceil(Sala/4) + 7 # ---- 2 de defesa
        Defesa_Inimigo_Atual = Defesa_Inimigo
        Dano_Inimigo = Sala * 3
    elif tier == 4:
        Vida_Inimigo = (Sala * 10) + 13 # 127-167
        Vida_Inimigo_Atual = Vida_Inimigo
        Defesa_Inimigo = math.ceil(Sala/3) + 10 # ---- 2 de defesa
        Defesa_Inimigo_Atual = Defesa_Inimigo
        Dano_Inimigo = Sala * 3
    elif tier == 5:
        Vida_Inimigo = (Sala * 15) + 17 # 170
        Vida_Inimigo_Atual = Vida_Inimigo
        Defesa_Inimigo = math.ceil(Sala/2) # ---- 2 de defesa
        Defesa_Inimigo_Atual = Defesa_Inimigo
        Dano_Inimigo = Sala * 3

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
    if Retry == True:
        JogarNovamente()
        Retry = False
    
    

    janela.fill((255, 255, 255))
    Escolher_Arma_e_Armadura()
    pygame.display.flip() # Desenha a tela atual 
    clock.tick(60) # 60fps isso dai

pygame.quit()
