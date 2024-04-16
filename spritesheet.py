import pygame
import os


class Sheet():
    def __init__(self, imagem):
        self.tabela = imagem

    def pegar_sprite(self, frame, largura, altura, escala):
        imagem = pygame.Surface((largura, altura)).convert_alpha()
        imagem.blit(self.tabela, (0, 0), ((frame * largura), 0, largura, altura))
        imagem = pygame.transform.scale(imagem, (largura * escala, altura * escala))

        return imagem
