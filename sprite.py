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


class Mob(Entidade):
    def __init__(self, groups, image=pygame.Surface((BLOCO_TAM, BLOCO_TAM)), posicao=(0, 0), parametros = {}):
        super().__init__(groups, image, posicao)

        #Parametros
        if parametros:
            self.grupo_blocos = parametros['grupo_blocos']
            self.player = parametros['player']

        self.velocity = pygame.math.Vector2()
        self.tempo_geral = pygame.time.get_ticks()

    def move(self):
        self.tempo_geral = pygame.time.get_ticks()
        try:
            dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * MOB_SPEED
            self.checar_colisoes('horizontal',dx,dy)
            self.rect.y += dy * MOB_SPEED
            self.checar_colisoes('vertical', dx,dy)
            if self.player.rect.colliderect(self.rect):
                self.player.hit()
        except Exception as e:
            print(e)

    def checar_colisoes(self, direcao,dx,dy):
        if direcao == "horizontal":
            for block in self.grupo_blocos:
                if block.rect.colliderect(self.rect):
                    if dx > 0:  # Movimento para direita
                        self.rect.right = block.rect.left
                    else:  # Movimento para esquerda
                        self.rect.left = block.rect.right
        if direcao == "vertical":
            for block in self.grupo_blocos:
                if block.rect.colliderect(self.rect):
                    if dy > 0:  # Movimento para cima
                        self.rect.bottom = block.rect.top
                    else:  # Movimento para baixo
                        self.rect.top = block.rect.bottom

    def update(self):
        self.move()