import math

import pygame

from globais import *


class Entidade(pygame.sprite.Sprite):
    def __init__(self, groups, image=pygame.Surface((BLOCO_TAM, BLOCO_TAM), pygame.SRCALPHA), posicao=(0, 0)):
        super().__init__(groups)

        self.image = image
        self.rect = self.image.get_rect(topleft=posicao)
        
        
    def update(self):  # Sobreescrvendo o update do pygames.sprite.Sprite
        pass


class Mob(pygame.sprite.Sprite):
    def __init__(self, groups, image, posicao=(0, 0), parametros = {}):
        super().__init__(groups)

        #Parametros
        if parametros:
            self.grupo_blocos = parametros['grupo_blocos']
            self.player = parametros['player']
        
        self.sprite_atual = 0
        self.sprites = image
        self.image = self.sprites['zombie_idle'][self.sprite_atual]
        print(self.image)
        self.rect = self.image.get_rect(topleft=posicao)
        self.velocity = pygame.math.Vector2()
        self.tempo_geral = pygame.time.get_ticks()
        self.seguirInimigo = 0
        
        # Animacao
        self.esquerda = False
        self.ultimo_check = 0
        self.ultima_acao = "nenhuma"
        self.atacando = 0

    def animar(self, acao):
        cooldown_ani = 50

        if self.ultima_acao == "nenhuma":
            self.ultima_acao = acao

        if self.ultima_acao != acao:
            self.sprite_atual = -1
            self.ultima_acao = acao

        # Atualiza o sprite atual, para o frame posterior.

        if pygame.time.get_ticks() - self.ultimo_check > cooldown_ani:
            self.sprite_atual += 1
            self.ultimo_check = pygame.time.get_ticks()

        if self.sprite_atual >= len(self.sprites[acao]):    # Se chegar no ultimo frame, volta para o primeiro.
            self.atacando = 0  # Atualiza o status de ataque para 0.
            self.sprite_atual = 0

        if self.esquerda:  # Se o personagem estiver andando para esquerda, espelha a imagem e atualiza o frame.
            self.image = pygame.transform.flip(self.sprites[acao][int(self.sprite_atual)], self.esquerda, False)

        else:
            self.esquerda = False
            self.image = self.sprites[acao][int(self.sprite_atual)]  # Atualiza o frame.

    def ataque(self):
        if self.atacando == 1:
            self.animar('zombie_ataque')
            self.player.hit()

    def move(self):
        self.tempo_geral = pygame.time.get_ticks()
        raio =  32*10
        
        d = ((self.player.rect.x - self.rect.x )**2 + (self.player.rect.y - self.rect.y)**2 )**(1/2)
        if raio > d :
            self.seguirInimigo = 1
        else:
            self.seguirInimigo = 0

        if self.seguirInimigo:
            try:
                self.animar('zombie_run')
                dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist
                if dx < 0:
                    self.esquerda = True
                else:
                    self.esquerda = False
                self.rect.x += dx * MOB_SPEED
                self.checar_colisoes('horizontal',dx,dy)
                self.rect.y += dy * MOB_SPEED
                self.checar_colisoes('vertical', dx,dy)
                if self.player.rect.colliderect(self.rect):
                    self.atacando = 1

            except Exception as e:
                ...
        else:
            self.animar('zombie_idle')

    def checar_colisoes(self, direcao,dx,dy):
        if direcao == "horizontal":
            for block in self.grupo_blocos:
                self.temp = self.rect.copy()
                if block.rect.colliderect(pygame.Rect.inflate(self.temp,-1,-1)):
                    if dx > 0:  # Movimento para direita
                        self.rect.right = block.rect.left
                    else:  # Movimento para esquerda
                        self.rect.left = block.rect.right
        if direcao == "vertical":
            for block in self.grupo_blocos:
                self.temp = self.rect.copy()
                if block.rect.colliderect(pygame.Rect.inflate(self.temp,-7,-5)):
                    if dy > 0:  # Movimento para cima
                        self.rect.bottom = block.rect.top
                    else:  # Movimento para baixo
                        self.rect.top = block.rect.bottom

    def update(self):
        if self.atacando == 0:
            self.move()
        elif self.atacando:
            self.animar('zombie_ataque')
            self.ataque()