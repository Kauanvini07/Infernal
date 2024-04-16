import pygame
import spritesheet
import os

class animacao:
    def __init__(self, group, quant_frame):
        self.animacao = group
        self.quant_frame = quant_frame
        frame = 0

class Mago(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.hp = 15
        self.mana = 25
        self.stamina = 10
        self.sprites = animacao()
        frame = 0
