import pygame

from bancodados import *
from globais import *


class BolaDeFogo(pygame.sprite.Sprite):
    def __init__(self, app, x, y, velo, groups):
        super().__init__(groups)
        self.app = app
        self.x = x
        self.y = y
        self.velo = velo  # Velocidade de movimento da bola de fogo
        self.image = pygame.image.load('imgs/blfg.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 50))
        self.som = pygame.mixer.Sound('sons/sou_eu_bola_de_fogo.wav')

    def update(self):
        # Atualizar a posição da bola de fogo movendo-a para a direita
        self.x += self.velo


class Player(pygame.sprite.Sprite):
    def __init__(self, app, groups, image, posicao: tuple, parametros: dict,idplayer=1, name="Jogador1", vida=10, dano=10, Class=1,maps='m01',x=0,y=0):
        super().__init__(groups)
        with Banco_de_Dados() as banco:
            self.jogador = banco.visualizar_jogador(idplayer)
            if self.jogador is None:
                banco.adicionar_jogador(idplayer, name, vida, dano, Class)
                self.jogador = banco.visualizar_jogador(idplayer=1)
        
        self.id = self.jogador['idplayer']
        self.name = self.jogador['name']
        self.classe = 'Mago' if self.jogador['Class'] == 1 else 'Gerreiro' if self.jogador['Class'] == 2 else 'Arqueiro'
        self.dano = self.jogador['dano']
        #  Sprites
        self.app = app
        self.sprite_atual = 0
        self.sprites = image
        print(image)
        self.image = self.sprites['mago_idle'][self.sprite_atual]
        if self.jogador['Salve']:
            self.rect = self.image.get_rect(topleft=(self.jogador['x'],self.jogador['y']))
        else:
            self.rect = self.image.get_rect(topleft=posicao)

        # Parametros
        if parametros:
            self.grupo_blocos = parametros['grupo_blocos']
            self.grupo_inimigos = parametros['grupo_inimigos']
            self.grupo_bola = parametros['grupo_bola']

        # Status
        self.hp = self.jogador['vida']
        self.ultimohit = 0
        self.cooldownhit = 3000

        # Velocidade
        self.velocity = pygame.math.Vector2()

        # Animacao
        self.esquerda = False
        self.ultimo_check = 0
        self.ultima_acao = "nenhuma"

        # Atacando
        self.atacando = 0
        self.bolas = []
        self.retangulo_atualizado = True

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
            if not self.atacando and not self.retangulo_atualizado:  # Quando não está atacando, reseta a flag para permitir atualização novamente
                self.retangulo_atualizado = True
                tempy = self.rect.bottom
                self.rect.top = tempy  # Define o canto inferior esquerdo
                acao = "mago_idle"
            self.sprite_atual = 0

        if self.esquerda:  # Se o personagem estiver andando para esquerda, espelha a imagem e atualiza o frame.
            if self.atacando and self.retangulo_atualizado:
                tempy = self.rect.top
                self.rect.bottom = tempy  # Define o canto inferior
                self.retangulo_atualizado = False  # Marca que o retângulo foi atualizado
            self.image = pygame.transform.flip(self.sprites[acao][int(self.sprite_atual)], self.esquerda, False)
        else:
            if self.atacando and self.retangulo_atualizado:
                tempy = self.rect.top
                self.rect.bottom = tempy  # Define o canto inferior esquerdo
                self.retangulo_atualizado = False  # Marca que o retângulo foi atualizado
            self.esquerda = False
            self.image = self.sprites[acao][int(self.sprite_atual)]  # Atualiza o frame.

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
        if keys[pygame.K_k]:
            self.atacando = 2
        if keys[pygame.K_F6]:
            with Banco_de_Dados() as banco:
                banco.upadate_player(self.jogador)

    def ataque(self):
        if self.atacando == 1:
            if len(self.bolas) == 0:
                self.animar('mago_ataque')
                nova_blfg = BolaDeFogo(self.app, self.rect.x, self.rect.y, 5, self.grupo_bola)
                nova_blfg.som.play()
                self.bolas.append(nova_blfg)
        elif self.atacando == 2:
            self.animar('mago_ataque')
            for inimigo in self.grupo_inimigos:
                d = ((inimigo.rect.x - self.rect.x) ** 2 + (inimigo.rect.y - self.rect.y) ** 2) ** (1 / 2)
                if 32 > d:
                    inimigo.kill()

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
        self.jogador['x'] = self.rect.x
        self.jogador['y'] = self.rect.y
 
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
                    if self.velocity.x > 0:  # Movimento para direita
                        self.rect.right = block.rect.left
                    else:  # Movimento para esquerda
                        self.rect.left = block.rect.right
        if direcao == "vertical":
            for block in self.grupo_blocos:
                if block.rect.colliderect(self.rect):
                    if self.velocity.y > 0:  # Movimento para cima
                        self.rect.bottom = block.rect.top
                    else:  # Movimento para baixo
                        self.rect.top = block.rect.bottom

    def hit(self):
        if self.hp == 0:
            self.kill()
        if pygame.time.get_ticks() - self.ultimohit > self.cooldownhit:
            self.animar('mago_hit')
            self.hp -= 1
            self.jogador['vida'] = self.hp
            self.ultimohit = pygame.time.get_ticks()

    def update(self):  
        self.input()
        if self.atacando == 0:
            self.move()
        elif self.atacando:
            self.animar('mago_ataque')
            self.ataque()
        """
        for bola in self.bolas:
            bola.update()
        for bola in self.bolas:
            for inimigo in self.grupo_inimigos:
                if abs(bola.x - self.grupo_inimigos.x) <= 25 and abs(bola.y - self.grupo_inimigos.y) <= 38:
                    inimigo.kill()
        """
