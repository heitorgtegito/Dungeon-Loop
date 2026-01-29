# 13 7 16 6 20 15 -> Importante!

import pygame
import random
import sys
import math

# =========================================================
# Iniciozinho basico do pygame
# =========================================================
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Versão beta do dungeon loop ai")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# =========================================================
# Controle do status do jogo
# =========================================================
STATE_TITLE = "TITLE"
STATE_DUNGEON = "DUNGEON"
STATE_COMBAT = "COMBAT"
STATE_LEVEL_UP = "LEVEL_UP"
STATE_GAMEOVER = "GAMEOVER"
STATE_POTION_MENU = "POTION_MENU"

state = STATE_TITLE

# =========================================================
# Tela inicial (IMAGENS) --> PRECISA TER NA VERSÃO PARCIAL MLK
# =========================================================
title_bg = pygame.image.load("Imagens\Jogar.png").convert() # Professor tinha dito q o .convert() era bom né, vo botar
botao_jogar = pygame.image.load("Imagens\BotaoJogar.png").convert()

# Centralizar botão
botao_rect = botao_jogar.get_rect()
botao_rect.center = (930, 375) #eu amo .get_rect()

# =========================================================
# Oq e herdado das outras runs tlgd
# =========================================================
meta = {
    "forca": 0,
    "destreza": 0,
    "constituicao": 0,
    "sorte": 0
}

ultima_heranca = meta.copy()

# =========================================================
# Upar de level
# =========================================================
level_up_options = ["FORÇA", "DESTREZA", "CONSTITUIÇÃO", "SORTE"]
opcao_level_up = 0

STAT_MAP = {
    "FORÇA": "forca",
    "DESTREZA": "destreza",
    "CONSTITUIÇÃO": "constituicao",
    "SORTE": "sorte"
}

# =========================================================
# Jogador ai
# =========================================================
def nova_run():
    base = 5
    return {
        "hp": 0,
        "max_hp": 0,

        "base_forca": base,
        "base_destreza": base,
        "base_constituicao": base,
        "base_sorte": base,

        "start_forca": base,
        "start_destreza": base,
        "start_constituicao": base,
        "start_sorte": base,

        "forca": base + meta["forca"],
        "destreza": base + meta["destreza"],
        "constituicao": base + meta["constituicao"],
        "sorte": base + meta["sorte"],

        "level": 1,
        "exp": 0,
        "exp_next": 20,
        "pontos": 0,
        "sala": 1,

        "pocoes": {
            "simples": 0,
            "media": 0,
            "avancada": 0,
            "especial": 0
        }
    }

player = nova_run()
inimigo = {}
critico_ativo = False

# =========================================================
# Vida
# =========================================================
def recalcular_vida(old_max=None): # mlk q giro foi esse q precisa dar pra poder atualizar uma variavel pqp nao aguento mais
    new_max = 10 + player["constituicao"] * 2

    if old_max is None:
        player["hp"] = new_max
    else:
        player["hp"] += new_max - old_max

    player["max_hp"] = new_max
    player["hp"] = min(player["hp"], player["max_hp"])

recalcular_vida()

# =========================================================
# Inimigos
# =========================================================
def get_tier(sala): # define o tier
    if sala <= 25:
        return 1
    elif sala <= 50:
        return 2
    elif sala <= 75:
        return 3
    else:
        return 4

def exp_por_tier(tier): # define o xp pelo tier ne pit
    return {1: 20, 2: 40, 3: 80, 4: 160}[tier]

def criar_inimigo(sala): # cria os status dele memo
    tier = get_tier(sala)
    return {
        "hp": 12 + sala * 2,
        "dano": 2 + sala,
        "tier": tier,
        "exp": exp_por_tier(tier)
    }

# =========================================================
# Combate
# =========================================================
def calcular_dano_jogador():
    global critico_ativo
    critico_ativo = False

    base = player["forca"] + player["destreza"] * 0.5
    crit_chance = 0.05 + player["sorte"] * 0.005
    bonus_crit = player["forca"] * 0.6

    if random.random() < crit_chance:
        critico_ativo = True
        return int(base + bonus_crit)

    return int(base)

def calcular_dano_recebido(dano_base): # Defesa games
    """
    Reduz o dano recebido com base na CONSTITUIÇÃO.
    Existe um cap pra não virar imortal
    """
    reducao = player["constituicao"] * 0.006  # 0.6% por ponto
    reducao = min(reducao, 0.60)              # cap de 60%

    dano_final = int(dano_base * (1 - reducao))
    return max(1, dano_final)                 # nunca toma 0

def chance_fuga():
    chance = 0.2 + player["destreza"] * 0.005 + player["sorte"] * 0.015
    return min(0.95, chance)

# =========================================================
# Pocao ai slk
# =========================================================
cura_pocao = {
    "simples": 0.25,
    "media": 0.45,
    "avancada": 0.7,
    "especial": 1.0
}

POTION_MAP = {
    "SIMPLES": "simples",
    "MÉDIA": "media",
    "AVANÇADA": "avancada",
    "ESPECIAL": "especial"
}

def dropar_pocao(tier):
    """
    Sorte influencia:
    - quantidade de rolagens
    - chance de poções melhores
    - nenhuma chance chega a 100%
    """
    # quantidade de rolls com sorte
    rolls = 1 + player["sorte"] // 20

    for _ in range(rolls):
        luck = player["sorte"] * 0.003
        roll = random.random()

        # Ajuste de qualidade baseado no tier + sorte
        if tier == 1:
            if roll < 0.35 + luck:
                player["pocoes"]["simples"] += 1
            elif roll < 0.42 + luck * 0.6:
                player["pocoes"]["media"] += 1

        elif tier == 2:
            if roll < 0.30 + luck:
                player["pocoes"]["media"] += 1
            elif roll < 0.38 + luck * 0.6:
                player["pocoes"]["avancada"] += 1

        elif tier == 3:
            if roll < 0.28 + luck:
                player["pocoes"]["avancada"] += 1
            elif roll < 0.35 + luck * 0.5:
                player["pocoes"]["especial"] += 1

        elif tier == 4:
            if roll < 0.30 + luck * 0.8:
                player["pocoes"]["especial"] += 1

def usar_pocao(tipo):
    if player["pocoes"][tipo] > 0:
        cura = int(player["max_hp"] * cura_pocao[tipo])
        player["hp"] = min(player["hp"] + cura, player["max_hp"])
        player["pocoes"][tipo] -= 1
        return True
    return False

# =========================================================
# Pegar os status da run antiga ai
# =========================================================
def aplicar_heranca():
    global ultima_heranca
    ultima_heranca = {
        "forca": math.floor((player["base_forca"] - player["start_forca"]) * 0.8),
        "destreza": math.floor((player["base_destreza"] - player["start_destreza"]) * 0.8),
        "constituicao": math.floor((player["base_constituicao"] - player["start_constituicao"]) * 0.8),
        "sorte": math.floor((player["base_sorte"] - player["start_sorte"]) * 0.8),
    }
    for s in meta:
        meta[s] += max(0, ultima_heranca[s])

def atualizar_status_finais():
    for s in meta:
        player[s] = player[f"base_{s}"] + meta[s]

# =========================================================
# Aumentar +1 em cada atributinho ai
# =========================================================
def bonus_global_level(old_max):
    if player["level"] % 3 == 0:
        for s in ["forca", "destreza", "constituicao", "sorte"]:
            player[f"base_{s}"] += 1
        atualizar_status_finais()
        recalcular_vida(old_max)

# =========================================================
# Desenho
# =========================================================
def draw_text(text, x, y, selected=False):
    color = (255, 255, 0) if selected else (255, 255, 255)
    screen.blit(font.render(text, True, color), (x, y))

# =========================================================
# Menuzinhos
# =========================================================
combat_options = ["ATACAR", "FUGIR", "POÇÃO"]
opcao_combate = 0

potion_menu_options = ["ESPECIAL", "AVANÇADA", "MÉDIA", "SIMPLES", "VOLTAR"]
opcao_pocao = 0

# =========================================================
# Jogo memo ai
# =========================================================

# variavel pra porra nenhuma ta
def sair():
    pygame.quit()
    sys.exit()
# acho q foi mascena q usou e eu achei bonito entao copiei

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair()
        if event.type == pygame.KEYDOWN:
            if state == STATE_TITLE:
                if event.key == pygame.K_RETURN:
                    state = STATE_DUNGEON

            if event.key == pygame.K_ESCAPE and state == STATE_POTION_MENU:
                state = STATE_COMBAT

            if state == STATE_DUNGEON and event.key == pygame.K_RETURN:
                inimigo = criar_inimigo(player["sala"])
                opcao_combate = 0
                critico_ativo = False
                state = STATE_COMBAT

            elif state == STATE_COMBAT:
                if event.key == pygame.K_UP:
                    opcao_combate = (opcao_combate - 1) % len(combat_options)
                elif event.key == pygame.K_DOWN:
                    opcao_combate = (opcao_combate + 1) % len(combat_options)

                elif event.key == pygame.K_RETURN:
                    escolha = combat_options[opcao_combate]

                    if escolha == "ATACAR":
                        inimigo["hp"] -= calcular_dano_jogador()
                        if inimigo["hp"] > 0:
                            player["hp"] -= calcular_dano_recebido(inimigo["dano"])

                    elif escolha == "FUGIR":
                        if random.random() < chance_fuga():
                            # Cura 55% da VIDA ATUAL
                            cura = int(player["max_hp"] * 0.35)
                            player["hp"] = min(player["hp"] + cura, player["max_hp"])
                            player["sala"] += 1
                            state = STATE_DUNGEON
                            continue
                        else:
                            player["hp"] -= calcular_dano_recebido(inimigo["dano"])

                    elif escolha == "POÇÃO":
                        opcao_pocao = 0
                        state = STATE_POTION_MENU
                        continue

                    if player["hp"] <= 0:
                        aplicar_heranca()
                        state = STATE_GAMEOVER
                        continue

                    if inimigo["hp"] <= 0:
                        dropar_pocao(inimigo["tier"])
                        player["exp"] += inimigo["exp"]

                        while player["exp"] >= player["exp_next"]:
                            old = player["max_hp"]
                            player["exp"] -= player["exp_next"]
                            player["level"] += 1
                            player["exp_next"] = player["level"] * 20
                            player["pontos"] += 7
                            bonus_global_level(old)
                            opcao_level_up = 0
                            state = STATE_LEVEL_UP
                            break
                        else:
                            player["sala"] += 1
                            state = STATE_DUNGEON

            elif state == STATE_POTION_MENU:
                if event.key == pygame.K_UP:
                    opcao_pocao = (opcao_pocao - 1) % len(potion_menu_options)
                elif event.key == pygame.K_DOWN:
                    opcao_pocao = (opcao_pocao + 1) % len(potion_menu_options)

                elif event.key == pygame.K_RETURN:
                    opt = potion_menu_options[opcao_pocao]
                    if opt == "VOLTAR":
                        state = STATE_COMBAT
                    else:
                        tipo = POTION_MAP[opt]
                        if not usar_pocao(tipo):
                            player["hp"] -= calcular_dano_recebido(inimigo["dano"])
                        state = STATE_COMBAT

            elif state == STATE_LEVEL_UP:
                if event.key == pygame.K_UP:
                    opcao_level_up = (opcao_level_up - 1) % len(level_up_options)
                elif event.key == pygame.K_DOWN:
                    opcao_level_up = (opcao_level_up + 1) % len(level_up_options)

                elif event.key == pygame.K_RETURN and player["pontos"] > 0:
                    old = player["max_hp"]
                    stat = STAT_MAP[level_up_options[opcao_level_up]]
                    player[f"base_{stat}"] += 1
                    player["pontos"] -= 1
                    atualizar_status_finais()
                    recalcular_vida(old)

                    if player["pontos"] <= 0:
                        player["sala"] += 1
                        state = STATE_DUNGEON

            elif state == STATE_GAMEOVER and event.key == pygame.K_r:
                player = nova_run()
                atualizar_status_finais()
                recalcular_vida()
                inimigo = {}
                state = STATE_DUNGEON

    # =====================================================
    # Desenhos
    # =====================================================
    screen.fill((0, 0, 0))

    if state == STATE_TITLE:
        # Fundo
        screen.blit(title_bg, (0, 0))

        # Botão
        screen.blit(botao_jogar, botao_rect)

        # Texto acima do botão
        texto = font.render("Pressione ENTER para Jogar", True, (0, 0, 0))
        texto_rect = texto.get_rect()
        texto_rect.center = (930, botao_rect.top - 30)
        screen.blit(texto, texto_rect)

    if state == STATE_DUNGEON:
        draw_text(f"SALA: {player['sala']}", 40, 40)
        draw_text(f"LEVEL: {player['level']}", 40, 70)
        draw_text(f"HP: {player['hp']} / {player['max_hp']}", 40, 100)
        draw_text(
            f"STATUS: F{player['forca']} D{player['destreza']} "
            f"C{player['constituicao']} S{player['sorte']}",
            40, 140
        )
        draw_text("ENTER - Entrar em combate", 40, 200)

    elif state == STATE_COMBAT:
        draw_text("COMBATE", 40, 40)
        draw_text(f"HP Jogador: {player['hp']} / {player['max_hp']}", 40, 80)
        draw_text(f"HP Inimigo: {inimigo['hp']}", 40, 110)
        if critico_ativo:
            draw_text("CRÍTICO!", 520, 40)
        for i, opt in enumerate(combat_options):
            draw_text(opt, 40, 200 + i * 40, selected=(i == opcao_combate))

    elif state == STATE_POTION_MENU:
        draw_text("POÇÕES", 40, 40)
        for i, opt in enumerate(potion_menu_options):
            if opt == "VOLTAR":
                texto = "VOLTAR"
            else:
                chave = POTION_MAP[opt]
                texto = f"{opt} ({player['pocoes'][chave]})"
            draw_text(texto, 40, 120 + i * 40, selected=(i == opcao_pocao))

    elif state == STATE_LEVEL_UP:
        draw_text("LEVEL UP!", 40, 40)
        draw_text(f"Pontos restantes: {player['pontos']}", 40, 80)
        for i, opt in enumerate(level_up_options):
            draw_text(opt, 40, 140 + i * 40, selected=(i == opcao_level_up))

    elif state == STATE_GAMEOVER:
        draw_text("VOCÊ MORREU", 40, 40)
        draw_text("HERANÇA DA RUN:", 40, 90)
        y = 120
        for k, v in ultima_heranca.items():
            draw_text(f"{k.title()}: +{v}", 40, y)
            y += 30
        draw_text("R - Nova Run", 40, 300)

    pygame.display.flip()

'''
Acho q ngm vai nunca ler isso, entao vou expressar todo meu ódio pela documentacao do pygame e meus agradecimentos à meu mano Russo q salvou minha pele 500x
meu amigo q documentação vei chibata da porra, tem merda nenhuma escrita lá, pra tu olhar 1 documento de sprite tem q dar 6213632 voltas, meu amigo q
dificuldade da porra cara, eu acho q nunca estive tao exausto de estar na frente de um pc quanto esses tempos. Que plataforminha vei insuportável puta merda
'''

