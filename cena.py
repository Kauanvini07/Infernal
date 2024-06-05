import csv

import pygame

from globais import *
from player import Player
from sprite import Entidade, Mob
from texturas import textura_ataque, texturas_por_imagem, texturas_sheet


class Camera:

    def __init__(self, game,width,height):

        self.game = game
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.camera = pygame.Rect(0,0,width, height)
    
    def apply(self, entidade):
        return entidade.rect.move(self.camera.topleft)

    def draw(self, surface,group):
        for sprite in group:
            surface.blit(sprite.image,self.apply(sprite))

    def update(self,jogador):
        
        self.x = max(self.width - SCREEN_WIDTH,min(0,int(self.width/2) - jogador.rect.centerx))
        self.y =  max(self.height - SCREEN_HEIGHT,min(0,int(self.height/2) - jogador.rect.centery))
        self.camera = pygame.Rect(self.x,self.y,self.width, self.height)
       

class Cena:
    def __init__(self, app):
        self.app = app  # Recebe o objeto Jogo

        self.textura_solo = self.gen_textura_solo()
        self.textura_sheet = self.gen_texturassheet('imgs/ALL Spritesheet.png')
        self.sprites = pygame.sprite.Group()
        self.entidade = Entidade([self.sprites])
        self.blocos = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.bola_de_fogo = pygame.sprite.Group()
        self.player = Player(app,[self.sprites], self.textura_sheet, (0,0), parametros={'grupo_blocos': self.blocos, 'grupo_inimigos': self.inimigos, 'grupo_bola': self.bola_de_fogo})

        with open(texturas_por_imagem['fundo']['csv']) as data:
            map = []
            data = csv.reader(data, delimiter=",")
            x, y = 0, 0
            for linha in data:
                map.append(list(linha))
                
            for linha in map:
                x = 0
                for bloco in linha:
                    if bloco == "0":
                        Entidade([self.sprites, self.blocos], posicao=(x*BLOCO_TAM, y*BLOCO_TAM))
                    if bloco == '2':
                        Mob([self.sprites,self.inimigos], self.textura_solo['inimigo'], posicao=(x*BLOCO_TAM, y*BLOCO_TAM), parametros={'grupo_blocos': self.blocos, 'player': self.player})
                    if bloco == '1':
                        self.player.rect.x = x*BLOCO_TAM
                        self.player.rect.y = y*BLOCO_TAM
                    x += 1
                y += 1

        # Player
        self.camera = Camera(self.app,800,600)

    def gen_texturassheet(self, caminho):
        texturas = {}
        sheet_img = pygame.image.load(caminho).convert_alpha()
        temp_atk = []

        for nome, data in texturas_sheet.items():
            temp_list = []
            pos_x = data['posicao'][0]
            for i in range(data['quant']):
                temp_img = pygame.Surface.subsurface(sheet_img,
                                                     pygame.Rect((pos_x, data['posicao'][1]), data['tamanho']))
                temp_list.append(pygame.transform.scale(temp_img, (44, 44)))
                pos_x += 144
            texturas[nome] = temp_list
        for nome, data in textura_ataque.items():
            temp_img = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))
            temp_atk.append(pygame.transform.scale(temp_img, (88, 88)))
        texturas['mago_ataque'] = temp_atk
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
        if not self.player.atacando and self.player.retangulo_atualizado:
            self.camera.update(self.player)

    def draw(self):

        self.app.screen.fill('black')
        self.app.screen.blit(self.textura_solo['fundo'], self.camera.apply(self.entidade ))
        self.camera.draw(self.app.screen, self.sprites)

        # Desenhar o círculo externo do medidor de vida
        pygame.draw.circle(self.app.screen, WHITE, (meter_x, meter_y), meter_radius + meter_border_width)
        # Desenhar o círculo interno do medidor de vida
        pygame.draw.circle(self.app.screen, RED, (meter_x, meter_y), int(meter_radius * (self.player.hp/ MAX_HP)))
        if not self.player.alive():
            self.app.screen.blit("GAME OVER")
