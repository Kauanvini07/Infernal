import pygame
from globais import *


class BolaDeFogo(pygame.sprite.Sprite):
    def __init__(self, app, x, y, velo, groups):
        super().__init__(groups)
        self.app = app
        self.x = x
        self.y = y
        print(f"X e y bola", self.x, self.y)
        self.velo = velo  # Velocidade de movimento da bola de fogo
        self.image = pygame.image.load('imgs/blfg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 50))
        self.som = pygame.mixer.Sound('sons/sou_eu_bola_de_fogo.wav')

    def att(self):
        # Atualizar a posição da bola de fogo movendo-a para a direita
        self.x += self.velo

    def desenhar(self):
        # Desenhar a bola de fogo na tela
        self.app.screen.blit(self.image, (self.x, self.y))

class Player(pygame.sprite.Sprite):
    def __init__(self, app, groups, image, posicao: tuple, parametros: dict):
        super().__init__(groups)
        #  Sprites
        self.app = app
        self.sprite_atual = 0
        self.sprites = image
        self.image = self.sprites['mago_idle'][self.sprite_atual]
        self.rect = self.image.get_rect(topleft=posicao)

        #Parametros
        if parametros:
            self.grupo_blocos = parametros['grupo_blocos']
            self.grupo_inimigos = parametros['grupo_inimigos']
            self.grupo_bola = parametros['grupo_bola']

        # Status
        self.hp = 1
        self.ultimohit = 0
        self.cooldownhit = 3000


        # Velocidade
        self.velocity = pygame.math .Vector2()

        # Animacao
        self.esquerda = False
        self.ultimo_check = 0

        # Atacando
        self.atacando = 0
        self.bolas = []


    def animar(self, acao):
        cooldown_ani = 50
        if pygame.time.get_ticks() - self.ultimo_check > cooldown_ani:
            self.sprite_atual +=1
            self.ultimo_check = pygame.time.get_ticks()
        if self.sprite_atual >= len(self.sprites[acao]):
            self.sprite_atual = 0
            self.atacando = 0
        if self.esquerda:
            self.image = pygame.transform.flip(self.sprites[acao][int(self.sprite_atual)], self.esquerda, False)
            if self.atacando == 1:
                temprect = self.image.get_rect()
                print(self.rect)
                print(self.rect)
        else:
            self.esquerda = False
            self.image = self.sprites[acao][int(self.sprite_atual)]
            if self.atacando == 1:
                print(self.rect)
                print(self.rect)
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.velocity.x = -1
            self.esquerda = True
        if keys[pygame.K_d]:
            self.velocity.x = 1
            self.esquerda = False
        if keys[pygame.K_s]:
            self.velocity.y = 1
        if keys[pygame.K_w]:
            self.velocity.y = -1
        if not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity.x = 0
            self.velocity.y = 0
        if keys[pygame.K_j]:
            self.atacando = 1

    def ataque(self):
        self.animar('mago_ataque')
        nova_blfg = BolaDeFogo(self.app, self.rect.x, self.rect.y, 5, self.grupo_bola)
        nova_blfg.som.play()
        self.bolas.append(nova_blfg)

    def move(self):
        self.checar_tela()
        self.rect.x += self.velocity.x * PLAYER_SPEED
        self.checar_colisoes('horizontal')
        self.rect.y += self.velocity.y * PLAYER_SPEED
        self.checar_colisoes('vertical')
        
        if self.velocity.x == 0 and self.velocity.y == 0:
            self.animar('mago_idle')
        else:
            self.animar('mago_run')
        self.velocity.x = 0
        self.velocity.y = 0


    def checar_tela(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x + 64 > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - 64
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + 64 > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - 64


    def checar_colisoes(self, direcao):
        if direcao == "horizontal":
            for block in self.grupo_blocos:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0: # Movimento para direita
                        self.rect.right = block.rect.left
                    else:                   # Movimento para esquerda
                        self.rect.left = block.rect.right
        if direcao == "vertical":
            for block in self.grupo_blocos:
                if block.rect.colliderect(self.rect):
                    if self.velocity.y > 0: # Movimento para cima
                        self.rect.bottom = block.rect.top
                    else:                   # Movimento para baixo
                        self.rect.top = block.rect.bottom

    def hit(self):
        if self.hp == 0:
            self.kill()
        if pygame.time.get_ticks() - self.ultimohit > self.cooldownhit:
            self.animar('mago_hit')
            self.hp -= 1
            self.ultimohit = pygame.time.get_ticks()

    def update(self):
        self.input()
        if self.atacando == 0:
            self.move()
        elif self.atacando == 1:
            self.animar('mago_ataque')
            self.ataque()
        for bola in self.bolas:
            bola.att()
        for bola in self.bolas:
            bola.desenhar()
        for bola in self.bolas:
            for inimigo in self.grupo_inimigos:
                if abs(bola.x - self.grupo_inimigos.x) <= 25 and abs(bola.y - self.grupo_inimigos.y) <= 38:
                    inimigo.kill()