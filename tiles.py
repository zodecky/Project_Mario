"""Tiles para o jogo:"""
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, posicao, tamanho):
        super().__init__()
        # Superficie precisa ser uma superficie quadrada (tamanho x tamanho)
        self.image = pygame.Surface((tamanho, tamanho))
        self.rect = self.image.get_rect(topleft=posicao)

    def update(self, shift_x):
        self.rect.x += shift_x


class StaticTile(Tile):
    def __init__(self, size, posicao, superficie):
        super().__init__(size, posicao)
        self.image = superficie
