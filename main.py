""" Rode esse arquivo para executar o programa."""
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
level = Level(mapa, screen)  # Instancia o level

while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    screen.fill("black")  # Preenche a tela com preto
    level.run()  # Executa o level

    # Tela:
    pygame.display.update()

    # Framerate
    clock.tick(60)
