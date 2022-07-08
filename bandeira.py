import pygame


class Bandeira(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = pygame.Surface((64, 128))  # Sprite do jogador
        self.image = pygame.image.load("assets/PNG/bandeira.png")
        self.rect = self.image.get_rect(topleft=posicao)

    def update(self, shift_x):
        self.rect.x += shift_x

