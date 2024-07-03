import csv

import pygame

from globais import *
from player import Player
from sprite import Entidade, Mob
from texturas import *

class Camera:

    def __init__(self, game, width, height):

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
        self.y = max(self.height - SCREEN_HEIGHT,min(0,int(self.height/2) - jogador.rect.centery))
        self.camera = pygame.Rect(self.x,self.y,self.width, self.height)
       

class Cena:
    def __init__(self, app):
        self.app = app  # Recebe o objeto Jogo
        self.proxmap = None
        self.fundo = None
        self.textura_solo = self.gen_textura_solo()
        #self.textura_sheet = self.gen_texturassheet('imgs/ALL Spritesheet.png')
        self.sprites = pygame.sprite.Group()
        self.entidade = Entidade([self.sprites])
        self.blocos = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.bola_de_fogo = pygame.sprite.Group()
        self.player = Player(app,[self.sprites], self.gen_texturassheet('imgs/ALL Spritesheet.png', texturas_sheet), (0,0), parametros={'grupo_blocos': self.blocos, 'grupo_inimigos': self.inimigos, 'grupo_bola': self.bola_de_fogo},idplayer=self.app.id)
        self.mapas = [nome for nome in relacao_mapas]
        if self.player.jogador['Salve']:
            self.mapa_atual = self.player.jogador['mapa']
        else:
            self.mapa_atual = self.mapas[0]

        # Player
        self.camera = Camera(self.app,800,800)

        self.criar_mapa(self.mapa_atual)


    def criar_mapa(self, nome):
        self.fundo = pygame.transform.scale(pygame.image.load(relacao_mapas[nome]['fundo']), (relacao_mapas[nome]['tamanho']))
        with open(relacao_mapas[nome]['caminho']) as data:
            map = []
            data = csv.reader(data, delimiter=",")
            x, y = 0, 0
            for linha in data:
                map.append(list(linha))

            for linha in map:
                x = 0
                for bloco in linha:
                    if bloco == "0": #Cria as paredes # self.textura_solo['tijolo'],
                        #Para teste de parede, faz a parede ter um sprite pra verificar a posição
                        #Entidade([self.sprites, self.blocos], self.textura_solo['tijolo'],posicao=(x * BLOCO_TAM, y * BLOCO_TAM))
                        Entidade([self.sprites, self.blocos], posicao=(x * BLOCO_TAM, y * BLOCO_TAM))
                    if bloco == '2': # salva o proximo mapa
                        self.proxmap = (relacao_mapas[nome]['prox_map'], x * BLOCO_TAM, y * BLOCO_TAM)
                    if bloco == '3': # spawna os bixo
                        Mob([self.sprites, self.inimigos], self.gen_texturassheet('imgs/Zombie.png', texturas_zombie), posicao=(x * BLOCO_TAM, y * BLOCO_TAM), parametros={'grupo_blocos': self.blocos, 'player': self.player})
                    if bloco == '4': # spawna o boss:
                        Mob([self.sprites, self.inimigos], self.gen_textura_boss(), posicao=(x * BLOCO_TAM, y * BLOCO_TAM), parametros={'grupo_blocos': self.blocos, 'player': self.player})
                    if bloco == '1': # Nascimento do player
                        self.player.rect.x = x * BLOCO_TAM
                        self.player.rect.y = y * BLOCO_TAM
                        if self.player.jogador['Salve'] == 1:
                            self.player.rect.x = self.player.jogador['x']
                            self.player.rect.y = self.player.jogador['y']
                    x += 1
                y += 1

    def resetar_mapa(self, nome):
        self.mapa_atual = nome
        self.proxmap = relacao_mapas[nome]['prox_map']
        self.sprites = pygame.sprite.Group()
        self.entidade = Entidade([self.sprites])
        self.blocos = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.bola_de_fogo = pygame.sprite.Group()
        
        self.player = Player(self.app,[self.sprites], self.gen_texturassheet('imgs/ALL Spritesheet.png', texturas_sheet), (0,0), parametros={'grupo_blocos': self.blocos, 'grupo_inimigos': self.inimigos, 'grupo_bola': self.bola_de_fogo},idplayer=self.app.id)
        self.player.jogador['mapa'] = self.mapa_atual
        self.player.jogador['Salve'] = 0
        self.camera = Camera(self.app,800,600)
        self.criar_mapa(self.mapa_atual)

    def gen_texturassheet(self, caminho, textura):
        texturas = {}
        sheet_img = pygame.image.load(caminho).convert_alpha()
        print(sheet_img)
        temp_atk = []

        for nome, data in textura.items():
            temp_list = []
            pos_x = data['posicao'][0]
            print(pos_x)
            for i in range(data['quant']):
                print(f"Index: {i}. Quant: {data['quant']}, Posicao: {data['posicao'][1]}, Tam:{data['tamanho']}, pos_x: {pos_x}")
                temp_img = pygame.Surface.subsurface(sheet_img,
                                                     pygame.Rect((pos_x, data['posicao'][1]), data['tamanho']))
                if data['tamanho'][0] != 32:
                    temp_list.append(pygame.transform.scale(temp_img, (32, 32)))
                elif data['tipo'] == 'inimigo' and data['tamanho'][0] == 32:
                    temp_list.append(pygame.transform.scale(temp_img, (44, 44)))
                else:
                    temp_list.append(temp_img)
                pos_x += data['dist_x'] # Atualiza a posição do X
            texturas[nome] = temp_list
            #Tratando os sprites de ataque do Mago
            if data['tipo'] == 'player' and not 'mago_ataque' in texturas:
                for nome, data in textura_ataque.items():
                        temp_img = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                                (data['tamanho']))
                        temp_atk.append(pygame.transform.scale(temp_img, (64, 64))) # Para animação funcionar, tem que ser
                                                                                        # o dobro do tamanho do sprite(ver acima)
                texturas['mago_ataque'] = temp_atk
        return texturas

    #  Pega as texturas por imagem(Atualziar o dicionário com o caminhos e informações da imagem)
    def gen_textura_solo(self):
        texturas = {}

        for nome, data in texturas_por_imagem.items():
            texturas[nome] = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))
        return texturas

    def gen_textura_boss(self):
        texturas = {}
        temp_atk = []
        temp_idle = []
        temp_corre = []

        for nome, data in textura_idle_king.items():
            temp_img = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))

            temp_idle.append(temp_img)
        texturas['zombie_idle'] = temp_idle

        for nome, data in textura_corre_king.items():
            temp_img = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))
            temp_corre.append(temp_img)
        texturas['zombie_run'] = temp_corre

        for nome, data in textura_ataque_king.items():
            temp_img = pygame.transform.scale(pygame.image.load(data['caminho']).convert_alpha(),
                                                    (data['tamanho']))
            temp_atk.append(temp_img)
        texturas['zombie_ataque'] = temp_atk

        return texturas
    
    def update(self):
        self.sprites.update()  # É um metodo implicito, o pygames.sprite.Sprite, já contém o .update()
        if not self.player.atacando and self.player.retangulo_atualizado:
            self.camera.update(self.player)
        if self.player.rect.x == self.proxmap[1] and self.player.rect.y == self.proxmap[2]: #verifica a troca de mapa
            self.resetar_mapa(self.proxmap[0])

    def draw(self):

        self.app.screen.fill('black')
        self.app.screen.blit(self.fundo, self.camera.apply(self.entidade ))
        self.camera.draw(self.app.screen, self.sprites)

        # Desenhar o círculo externo do medidor de vida
        pygame.draw.circle(self.app.screen, WHITE, (meter_x, meter_y), meter_radius + meter_border_width)
        # Desenhar o círculo interno do medidor de vida
        pygame.draw.circle(self.app.screen, RED, (meter_x, meter_y), int(meter_radius * (self.player.hp/ MAX_HP)))
        if not self.player.alive():
            self.app.screen.blit("GAME OVER")
