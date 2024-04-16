import pygame
from random import random
import sys

# Definir as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Alvo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemy_image = pygame.image.load('imgs/inimigo.png').convert_alpha()
        self.enemy = pygame.transform.scale(self.enemy_image, (50,75))
        self.enemy_image_hit = pygame.image.load('imgs/inimigo_hit.png').convert_alpha()
        self.enemy_hit = pygame.transform.scale(self.enemy_image_hit, (50,75))
        self.som_hit = pygame.mixer.Sound('sons/ze_da_manga.wav')

    def desenhar(self, screen, atingido = False):
        if atingido:
            screen.blit(self.enemy_hit, (self.x, self.y))
        else:
            screen.blit(self.enemy, (self.x, self.y))

    def att(self):
        if random() <= 0.5:
            self.x = (self.x + 1) % SCREEN_WIDTH
        if random() <= 0.5:
            self.y = (self.y + 1) % SCREEN_HEIGHT
class BolaDeFogo:
    def __init__(self, x, y, velo):
        self.x = x
        self.y = y 
        self.velo = velo  # Velocidade de movimento da bola de fogo
        self.blfg_img =pygame.image.load('imgs/blfg.png').convert_alpha()
        self.blfg = pygame.transform.scale(self.blfg_img, (45,50))
        self.som = pygame.mixer.Sound('sons/sou_eu_bola_de_fogo.wav')
        
    def att(self):
        # Atualizar a posição da bola de fogo movendo-a para a direita
        self.x += self.velo

    def desenhar(self, screen):
        # Desenhar a bola de fogo na tela
        screen.blit(self.blfg, (self.x, self.y))


# Inicializar o Pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infernal")

bg_img = pygame.image.load('imgs/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

musica_tema = pygame.mixer.Sound('sons/tema.wav')
musica_tema.play(-1)

clock = pygame.time.Clock()

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Definir o tamanho do jogador e sua posição inicial
player_size = 20
player_x = (SCREEN_WIDTH - player_size) // 2
player_y = (SCREEN_HEIGHT - player_size) // 2
player_speed = 10  # Velocidade de movimento do jogador

player_image = pygame.image.load('imgs/player.png').convert_alpha()
player = pygame.transform.scale(player_image, (50,75))

player_width = 50
player_height = 75

tempo_stam = 0
tempo_man = 0
tempo_dec = 0
tempo_dec_man = 0

rolando = False
stamina = 10
mana = 20
cooldown = False
bolas = []
alvo = Alvo(SCREEN_WIDTH - 50, SCREEN_HEIGHT//2)

# Loop principal do jogo
while True: 
    tempo_stam = pygame.time.get_ticks()
    tempo_man = pygame.time.get_ticks()
    
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturar teclas pressionadas
    keys = pygame.key.get_pressed()
    
    if tempo_stam - tempo_dec >= 500:
        stamina = stamina + 1 if stamina <= 10 else stamina
        mana = mana + 1 if mana  <= 20 else mana
        tempo_dec = tempo_stam
    
    if tempo_man - tempo_dec_man >= 1700:
        cooldown = False
        tempo_dec_man = tempo_man
        
    # Atualizar a posição do jogador com base nas teclas pressionadas
    if keys[pygame.K_LSHIFT]:
        player_speed = 5
    if not rolando:
        if keys[pygame.K_SPACE] and stamina >= 5:
            player_x = player_x + 2
            stamina -= 5
            rolando = True
    else:
        rolando = False
    if keys[pygame.K_j] and not cooldown:
        nova_blfg = BolaDeFogo(player_x + 25, player_y + 25, 5)
        nova_blfg.som.play()
        bolas.append(nova_blfg)
        cooldown = True
        
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    
    player_speed = 10
    
    if player_x < 0:
        player_x = 0
    elif player_x + player_width > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_width
    if player_y < 0:
        player_y = 0
    elif player_y + player_height > SCREEN_HEIGHT:
        player_y = SCREEN_HEIGHT - player_height
    
    for bola in bolas:
        bola.att()
    
    alvo.att()
    
    # Limpar a tela
    screen.blit(bg, (0, 0))

    alvo.desenhar(screen)
    
    for bola in bolas:
        bola.desenhar(screen)
    
    for bola in bolas:
        if abs(bola.x - alvo.x) <= 25 and abs(bola.y - alvo.y) <= 38:
            alvo.desenhar(screen,True)
            alvo.som_hit.play()
    
    screen.blit(player, (player_x, player_y))
    
    # Atualizar a tela
    pygame.display.flip()
    
    clock.tick(60)
