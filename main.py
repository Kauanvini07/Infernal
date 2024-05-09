import sys

import pygame

from cena import \
    Cena  # Arquivo com todas as funções que irão manipular o que acontece no jogo
from globais import *  # Arquivo com todas as variaveis globlais


class Jogo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.musica_tema = pygame.mixer.Sound('sons/tema.wav')
        self.musica_tema.play(-1)
        self.running = True
        self.cena = Cena(self)

    def run(self):
        while self.running:
            self.update()
            self.draw()
        self.close()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.cena.update()

        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.cena.draw()

    def close(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Jogo()
    game.run()
