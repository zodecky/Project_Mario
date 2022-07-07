"""Codigo do monstro."""

import pygame

MONSTRO_SPEED = -3


class Monstro(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.Surface((32, 32))  # Sprite do jogador
        self.image = pygame.image.load("assets/PNG/monstro.png")
        self.rect = self.image.get_rect(topleft=posicao)
        # Usar vetor pq é melhor que tupla/lista

        # Velocidade do jogador
        self.speed = MONSTRO_SPEED
        self.velocidade_queda = 0
        self.direcao = pygame.math.Vector2(0, 0)
        self.speed_pulo = MONSTRO_SPEED

        # Contador de pulo
        self.tempo_pulo = 0

    def movimento(self):
        self.rect.x += self.speed

    def update(self, shift_x):
        self.movimento()
        self.rect.x += shift_x
