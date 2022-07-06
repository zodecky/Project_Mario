import pygame
from tiles import StaticTile, Tile
from player import PLAYER_SPEED, Player
from configuracoes import tile_size, screen_width, screen_height
from utilitarios import import_cut_graphics


class Level:

    def __init__(self, level_data, superficie):
        self.display = superficie
        self.setup_level(level_data)
        self.shift_tudo = 0  # Desloca o nível ao invés do jogador (por quanto)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()  # Cria um grupo de sprites
        self.player = pygame.sprite.GroupSingle()  # Cria um grupo só com 1 sprite
        terrain_tile_list = import_cut_graphics(
            "assets/PNG/terrain_tiles.png")

        # DEFINICOES DE TILES DA LISTA: - - - - - - - - - - - - - -
        ground_tile = terrain_tile_list[1]
        ground_esquerdo_tile = terrain_tile_list[0]
        ground_direito_tile = terrain_tile_list[2]
        meio_tile = terrain_tile_list[5]
        canto_esquerdo_tile = terrain_tile_list[4]
        canto_direito_tile = terrain_tile_list[6]
        fim_esquerda_tile = terrain_tile_list[8]
        fim_meio_tile = terrain_tile_list[9]
        fim_direita_tile = terrain_tile_list[10]
        torre_cima_tile = terrain_tile_list[3]
        torre_meio_tile = terrain_tile_list[7]
        torre_fim_tile = terrain_tile_list[11]
        ground_solo_meio_tile = terrain_tile_list[13]
        ground_solo_esquerdo_tile = terrain_tile_list[12]
        ground_solo_direito_tile = terrain_tile_list[14]
        ground_solo_tile = terrain_tile_list[15]

        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        for row_i, row in enumerate(layout):
            for col_i, cell in enumerate(row):

                # Para não repetir: (pega a posição do tile independente do conteúdo)
                x = col_i * tile_size  # Posicao X do tile
                y = row_i * tile_size  # Posiciona o tile

                if cell == "G":  # Referencia se tem um X no mapa.
                    # Instancia o tile
                    tile = StaticTile((x, y), tile_size, ground_tile)
                    self.tiles.add(tile)  # Adiciona o tile ao grupo de sprites
                elif cell == "L":
                    tile = StaticTile((x, y), tile_size, ground_esquerdo_tile)
                    self.tiles.add(tile)
                elif cell == "R":
                    tile = StaticTile((x, y), tile_size, ground_direito_tile)
                    self.tiles.add(tile)
                elif cell == "E":
                    tile = StaticTile((x, y), tile_size, canto_esquerdo_tile)
                    self.tiles.add(tile)
                elif cell == "X":
                    tile = StaticTile((x, y), tile_size, meio_tile)
                    self.tiles.add(tile)
                elif cell == "D":
                    tile = StaticTile((x, y), tile_size, canto_direito_tile)
                    self.tiles.add(tile)
                elif cell == "T":
                    tile = StaticTile((x, y), tile_size, torre_cima_tile)
                    self.tiles.add(tile)
                elif cell == "O":
                    tile = StaticTile((x, y), tile_size, torre_meio_tile)
                    self.tiles.add(tile)
                elif cell == "F":
                    tile = StaticTile((x, y), tile_size, torre_fim_tile)
                    self.tiles.add(tile)
                elif cell == "S":
                    tile = StaticTile((x, y), tile_size, ground_solo_tile)
                    self.tiles.add(tile)
                elif cell == "A":
                    tile = StaticTile((x, y), tile_size, ground_solo_esquerdo_tile)
                    self.tiles.add(tile)
                elif cell == "W":
                    tile = StaticTile((x, y), tile_size, ground_solo_meio_tile)
                    self.tiles.add(tile)
                elif cell == "Z":
                    tile = StaticTile((x, y), tile_size, ground_solo_direito_tile)
                    self.tiles.add(tile)
                elif cell == "Y":
                    tile = StaticTile((x, y), tile_size, fim_esquerda_tile)
                    self.tiles.add(tile)
                elif cell == "U":
                    tile = StaticTile((x, y), tile_size, fim_meio_tile)
                    self.tiles.add(tile)
                elif cell == "I":
                    tile = StaticTile((x, y), tile_size, fim_direita_tile)
                    self.tiles.add(tile)
                ##### Adicionar M para monstro e K para poder
                elif cell == "P":  # Referencia se tem um P no mapa.
                    # Instancia o Player
                    player_sprite = Player((x, y))
                    # Adiciona o Player ao grupo de sprites (que só tem o player)
                    self.player.add(player_sprite)

    def scroll_x(self):  # move o nível e para o player

        player = self.player.sprite
        player_x = player.rect.centerx
        direcao_x = player.direcao.x

        if player_x < screen_width / 4 and direcao_x < 0:
            self.shift_tudo = PLAYER_SPEED
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direcao_x > 0:
            self.shift_tudo = -PLAYER_SPEED
            player.speed = 0
        else:
            self.shift_tudo = 0
            player.speed = PLAYER_SPEED

    def colisao_x(self):
        player = self.player.sprite
        player.rect.x += player.direcao.x * player.speed

        for objeto in self.tiles.sprites():
            if objeto.rect.colliderect(player.rect):
                if player.direcao.x > 0:
                    player.rect.right = objeto.rect.left
                elif player.direcao.x < 0:
                    player.rect.left = objeto.rect.right

    def colisao_y(self):
        player = self.player.sprite
        player.gravidade()

        for objeto in self.tiles.sprites():
            if objeto.rect.colliderect(player.rect):

                if player.direcao.y > 0:  # Colisão com o chao
                    player.rect.bottom = objeto.rect.top
                    player.direcao.y = 0  # Para não atravessar (gravidade = 0)
                    player.tempo_pulo = 0  # Zera para poder pular novamente

                elif player.direcao.y < 0:  # Colisão com o teto
                    player.rect.top = objeto.rect.bottom
                    player.tempo_pulo = 1000  # Termina o pulo se colidir com o teto

    def run(self):
        # Atualiza o grupo de tiles com o shift (camera)

        self.player.update()  # Atualiza o player
        self.tiles.update(self.shift_tudo)  # Atualiza o grupo de tiles
        self.tiles.draw(self.display)  # Desenha os tiles
        self.player.draw(self.display)  # Desenha o player
        self.scroll_x()
        self.colisao_x()
        self.colisao_y()
