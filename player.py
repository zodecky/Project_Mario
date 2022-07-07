"""Codigo do jogador."""

import pygame

PLAYER_SPEED = 6
PLAYER_PULO = 7
GRAVIDADE = 2
MAX_Y = 24
TEMPO_PULO = 8  # Qtd maxima de frames que o pulo dura
CONSTANTE_PULO_MONSTRO = 3


# Imagens:

olhando_direita = pygame.image.load("assets/PNG/player1.png")
olhando_esquerda = pygame.image.load("assets/PNG/player2.png")
pulando_direita = pygame.image.load("assets/PNG/playerjump1.png")
pulando_esquerda = pygame.image.load("assets/PNG/playerjump2.png")

class Player(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.Surface((32, 64))  # Sprite do jogador
        self.image = olhando_direita
        self.rect = self.image.get_rect(topleft=posicao)
        # Usar vetor pq é melhor que tupla/lista

        # Velocidade do jogador
        self.speed = PLAYER_SPEED
        self.direcao = pygame.math.Vector2(0, 0)
        self.constante_gravidade = GRAVIDADE
        self.speed_pulo = PLAYER_PULO

        # Contador de pulo
        self.tempo_pulo = 0

    def key_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direcao.x = 1
            self.image = olhando_direita
        elif keys[pygame.K_a]:
            self.direcao.x = -1
            self.image = olhando_esquerda
        else:
            self.direcao.x = 0

        if keys[pygame.K_SPACE]:
            self.pulo()

    def gravidade(self):
        self.direcao.y += self.constante_gravidade
        self.rect.y += self.direcao.y

    def pulo(self, do_monstro=False):
        if self.tempo_pulo < TEMPO_PULO:
            self.direcao.y -= self.speed_pulo
            self.tempo_pulo += 1
        if do_monstro:
            self.direcao.y -= self.speed_pulo * CONSTANTE_PULO_MONSTRO

        self.image = pulando_direita if self.direcao.x == 1 else pulando_esquerda

    def max_speed_y(self):
        if self.direcao.y > MAX_Y:
            self.direcao.y = MAX_Y
        elif self.direcao.y < -MAX_Y:
            self.direcao.y = -MAX_Y

    def update(self):
        self.key_input()
        self.max_speed_y()
        # incrementa o pulo a velocidade (pulo = -16, é negativo, pygame estranho...)
