""" Rode esse arquivo para executar o programa."""

# Gabriel Zagury
# Luiza Marcondes

import pygame
import sys
from configuracoes import *
from level import Level

# Setup Pygame
pygame.init()
pygame.mixer.init()
# Toca a música de fundo
pygame.mixer.music.load("assets/musica_totalmente_original.mp3")
pygame.mixer.music.play()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(mapa, screen, 0)  # Instancia o level

#Carrega Font Padrao do Sistema
sys_font = pygame.font.Font(pygame.font.get_default_font(), 20)

while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    screen.fill("black")  # Preenche a tela com preto
    level.run()  # Executa o level

    # carrega o proximo nivel
    if level.level_completo:

        if level.indice == -1:
            level = Level(mapa, screen, level.indice + 1)
        elif level.indice == 0:
            level = Level(mapa1, screen, level.indice + 1)
        elif level.indice == 1:
            level = Level(mapa2, screen, level.indice + 1)


    # Mostra o nivel atual
    texto_nivel = "Nivel: " + str(level.indice) if level.indice < 2 else "Fim de Jogo"
    texto = sys_font.render(texto_nivel, True, "white")
    screen.blit(texto, (10, 10))
    # Tela:
    pygame.display.update()

    # Framerate
    clock.tick(60)
