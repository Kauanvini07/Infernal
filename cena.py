import csv

import pygame

from globais import *
from player import Player
from sprite import Entidade, Mob
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

        
        with open("1123.csv") as data:
            map = []
            data = csv.reader(data, delimiter=",")
            x, y = 0, 0
            for linha in data:
                map.append(list(linha))
                
            for linha in map:
                x = 0
                for tijolo in linha:
                    if tijolo == "0":
                        Entidade([self.sprites, self.blocos], posicao=(x*BLOCO_TAM, y*BLOCO_TAM))
                    x += 1
                y += 1
                    
                    
            

        # Player
        self.player = Player([self.sprites], self.textura_sheet, (31, 250), parametros={'grupo_blocos': self.blocos, 'grupo_inimigos': self.inimigos})

        # Inimigo
        Mob([self.sprites], self.textura_solo['inimigo'], posicao=(250, 100), parametros={'grupo_blocos': self.blocos, 'player': self.player})
        Mob([self.sprites], self.textura_solo['inimigo'], posicao=(250, 400), parametros={'grupo_blocos': self.blocos, 'player': self.player})


    def gen_texturassheet(self, caminho):
        texturas = {}
        sheet_img = pygame.image.load(caminho).convert_alpha()

        for nome, data in texturas_sheet.items():
            temp_list = []
            pos_x = data['posicao'][0]
            for i in range(data['quant']):
                temp_img = pygame.Surface.subsurface(sheet_img,
                                                     pygame.Rect((pos_x, data['posicao'][1]), data['tamanho']))
                temp_list.append(pygame.transform.scale(temp_img, (BLOCO_TAM * 2, BLOCO_TAM * 2)))
                pos_x += 144
            texturas[nome] = temp_list
        return texturas

    #  Pega as texturas por imagem(Atualziar o dicionário com o caminhos e informações da imagem)
    def gen_textura_solo(self):
        texturas = {}

        for nome, data in texturas_por_imagem.items():
            texturas[nome] = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))
        texturas['fundo'] = pygame.transform.scale(texturas['fundo'],(800,600))
        return texturas

    def update(self):
        self.sprites.update()  # É um metodo implicito, o pygames.sprite.Sprite, já contém o .update()

    def draw(self):
        self.app.screen.fill('lightgreen')
        self.app.screen.blit(self.textura_solo['fundo'], (0, 0))
        self.sprites.draw(self.app.screen)
        if not self.player.alive():
            self.app.screen.blit("gGAME OVER")
        
