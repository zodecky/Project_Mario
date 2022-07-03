"""Controla as configurações do jogo."""

"""Contém SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE"""


def converte_txt_para_lista(path):
    with open(path) as file:
        return [line for line in file]


mapa = converte_txt_para_lista("nivel0.txt")

tile_size = 64
screen_width = 1200
screen_height = len(mapa) * tile_size
