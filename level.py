import pygame, sys
from tiles import StaticTile, Tile
from player import PLAYER_SPEED, Player
from monstro import MONSTRO_SPEED, Monstro
from bandeira import Bandeira
from configuracoes import tile_size, screen_width, screen_height
from utilitarios import import_cut_graphics

pygame.mixer.init()
som_morte = pygame.mixer.Sound("assets/hit.wav")
som_win = pygame.mixer.Sound("assets/swoosh.wav")
game_over_sprite = pygame.image.load("assets/gameover.png")

class Level:

    def __init__(self, level_data, superficie, level_indice=0):
        self.display = superficie
        self.setup_level(level_data)
        self.shift_tudo = 0  # Desloca o nível ao invés do jogador (por quanto)
        self.game_over = False
        self.level_completo = False
        self.indice = level_indice
        self.contador = 0


    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()  # Cria um grupo de sprites
        self.monstros = pygame.sprite.Group()  # Cria um grupo de sprites monstros
        self.player = pygame.sprite.GroupSingle()  # Cria um grupo só com 1 sprite
        self.bandeira = pygame.sprite.GroupSingle()  # Cria um grupo só com 1 sprite
        terrain_tile_list = import_cut_graphics(
            "assets/PNG/terrain_tiles.png")

        # DEFINICOES DE TILES DA LISTA: - - - - - - - - - - - - - -
        ground_tile                 =       terrain_tile_list[1]
        ground_esquerdo_tile        =       terrain_tile_list[0]
        ground_direito_tile         =       terrain_tile_list[2]
        meio_tile                   =       terrain_tile_list[5]
        canto_esquerdo_tile         =       terrain_tile_list[4]
        canto_direito_tile          =       terrain_tile_list[6]
        fim_esquerda_tile           =       terrain_tile_list[8]
        fim_meio_tile               =       terrain_tile_list[9]
        fim_direita_tile            =       terrain_tile_list[10]
        torre_cima_tile             =       terrain_tile_list[3]
        torre_meio_tile             =       terrain_tile_list[7]
        torre_fim_tile              =       terrain_tile_list[11]
        ground_solo_meio_tile       =       terrain_tile_list[13]
        ground_solo_esquerdo_tile   =       terrain_tile_list[12]
        ground_solo_direito_tile    =       terrain_tile_list[14]
        ground_solo_tile            =       terrain_tile_list[15]

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
                    tile = StaticTile((x, y), tile_size,
                                      ground_solo_esquerdo_tile)
                    self.tiles.add(tile)
                elif cell == "W":
                    tile = StaticTile((x, y), tile_size, ground_solo_meio_tile)
                    self.tiles.add(tile)
                elif cell == "Z":
                    tile = StaticTile((x, y), tile_size,
                                      ground_solo_direito_tile)
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
                # Adicionar M para monstro e K para poder
                elif cell == "P":  # Referencia se tem um P no mapa.
                    # Instancia o Player
                    player_sprite = Player((x, y))
                    # Adiciona o Player ao grupo de sprites (que só tem o player)
                    self.player.add(player_sprite)

                elif cell == "M":
                    # Instancia o Monstro
                    monstro_sprite = Monstro((x, y))
                    # Adiciona o Monstro ao grupo de sprites
                    self.monstros.add(monstro_sprite)

                elif cell == "B":
                    # Instancia a bandeira
                    bandeira_sprite = Bandeira((x, y))
                    self.bandeira.add(bandeira_sprite)


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

        # Para todo tile
        for objeto in self.tiles.sprites():

            # Colisao do player com o tile
            if objeto.rect.colliderect(player.rect):
                if player.direcao.x > 0:
                    player.rect.right = objeto.rect.left
                elif player.direcao.x < 0:
                    player.rect.left = objeto.rect.right
            
        
            # Para todo monstro
            for monstro in self.monstros.sprites():
                # Colisao do monstro com o tile
                if monstro.rect.colliderect(objeto.rect):
                    if monstro.speed > 0:
                        monstro.rect.right = objeto.rect.left
                        monstro.speed = monstro.speed * -1
                    elif monstro.speed < 0:
                        monstro.rect.left = objeto.rect.right
                        monstro.speed = monstro.speed * -1


            

    def colisao_y(self):
        player = self.player.sprite

        # Aplica a gravidade ao player
        # Assim o código da colisão fica mais fácil (do que fazer na classe)
        player.gravidade() if not self.game_over else None
        
        # Se o player cair
        if player.rect.bottom >= screen_height:
            self.game_over = True

        for objeto in self.tiles.sprites():
            if objeto.rect.colliderect(player.rect) and not self.game_over:

                if player.direcao.y > 0:  # Colisão com o chao
                    player.rect.bottom = objeto.rect.top
                    player.direcao.y = 0  # Para não atravessar (gravidade = 0)
                    player.tempo_pulo = 0  # Zera para poder pular novamente

                elif player.direcao.y < 0:  # Colisão com o teto
                    player.rect.top = objeto.rect.bottom
                    player.tempo_pulo = 1000  # Termina o pulo se colidir com o teto

        
        for monstro in self.monstros.sprites():
            if monstro.rect.colliderect(player.rect):

                # Player matou
                if player.direcao.y > 0:
                    player.rect.bottom = monstro.rect.top
                    player.direcao.y = 0
                    player.tempo_pulo = 0
                    player.pulo(do_monstro=True)
                    # Toca o som:
                    som_morte.play()
                    monstro.kill()
                
                # Player morreu
                elif player.direcao.y <= 0:
                    self.game_over = True

    def colisao_simples(self):
        player = self.player.sprite
        bandeira = self.bandeira.sprite
        if player.rect.colliderect(bandeira.rect):
            print("Você venceu!")
            som_win.play()
            # kill all tiles
            self.tiles.empty()
            # kill all monstros
            self.monstros.empty()
            # kill all bandeira
            self.bandeira.empty()
            # kill all player
            self.player.empty()

            # Load proximo nivel
            self.level_completo = True

    def run(self):
        # Atualiza o grupo de tiles com o shift (camera)

        self.player.update() if not self.game_over else None # Atualiza o player
        self.tiles.update(self.shift_tudo)  # Atualiza o grupo de tiles
        self.monstros.update(self.shift_tudo)  # Atualiza o grupo de monstros
        self.bandeira.update(self.shift_tudo)  # Atualiza o grupo de bandeira
        self.tiles.draw(self.display)  # Desenha os tiles
        self.monstros.draw(self.display)  # Desenha os monstros
        self.player.draw(self.display)  # Desenha o player
        self.bandeira.draw(self.display)  # Desenha a bandeira

        if self.game_over:

            if not self.contador:
                som_morte.play()
                self.contador = 1
            # Display image on center of screen
            self.display.blit(game_over_sprite, (screen_width / 2 - game_over_sprite.get_width() / 2,
                                                    screen_height / 2 - game_over_sprite.get_height() / 2))


            self.player.sprite.speed = 0
            velocidade_y_player = self.player.sprite.direcao.y
            velocidade_y_player = -10
            self.player.sprite.direcao.y = velocidade_y_player
            self.player.sprite.rect.y += velocidade_y_player

            self.contador += 1
            # black out screen bit by bit

            self.display.fill((0, 0, 0)) if self.contador > 250 else None

            if self.contador == 400:
                self.level_completo = True
                self.indice -= 1





        self.scroll_x()
        self.colisao_x()
        self.colisao_y()
        self.colisao_simples()
