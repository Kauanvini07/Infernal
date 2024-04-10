import pygame
from globais import *
from sprite import Entidade, Mob
from player import Player
from texturas import texturas_por_imagem, texturas_sheet


class Cena:
    def __init__(self, app):
        self.app = app  # Recebe o objeto Jogo

        self.textura_solo = self.gen_textura_solo()
        self.textura_sheet = self.gen_texturassheet('imgs/ALL Spritesheet.png')

        self.sprites = pygame.sprite.Group()
        self.entidade = Entidade([self.sprites])
        self.blocos = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()

        # Parede
        Entidade([self.sprites, self.blocos], pygame.Surface((BLOCO_TAM * 6, BLOCO_TAM)), posicao=(300, 200))

        # Player
        self.player = Player([self.sprites], self.textura_sheet, (400, 300), {'grupo_blocos': self.blocos})

        # Inimigo
        Mob([self.sprites], self.textura_solo['inimigo'], posicao=(250, 150), parametros={'grupo_blocos': self.blocos, 'player': self.player})


    def gen_texturassheet(self, caminho):
        texturas = {}
        sheet_img = pygame.image.load(caminho).convert_alpha()

        for nome, data in texturas_sheet.items():
            temp_list = []
            pos_x = 0
            for i in range(6):
                temp_img = pygame.Surface.subsurface(sheet_img,
                                                     pygame.Rect((pos_x, data['posicao'][1]), data['tamanho']))
                temp_list.append(pygame.transform.scale(temp_img, (BLOCO_TAM * 2, BLOCO_TAM * 2)))
                pos_x += 144
            texturas[nome] = temp_list
        print(texturas)
        return texturas

    #  Pega as texturas por imagem(Atualziar o dicionário com o caminhos e informações da imagem)
    def gen_textura_solo(self):
        texturas = {}

        for nome, data in texturas_por_imagem.items():
            texturas[nome] = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))
        return texturas

    def update(self):
        self.sprites.update()  # É um metodo implicito, o pygames.sprite.Sprite, já contém o .update()

    def draw(self):
        self.app.screen.fill('lightgreen')
        self.app.screen.blit(self.textura_solo['fundo'], (0, 0))
        self.sprites.draw(self.app.screen)
