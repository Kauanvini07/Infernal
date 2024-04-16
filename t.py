import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Definir as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Medidor de Vida estilo Diablo")

# Definir cores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Definir as coordenadas e o raio do círculo do medidor de vida
meter_x = 50
meter_y = 50
meter_radius = 30

# Definir a largura da borda do círculo do medidor de vida
meter_border_width = 3

# Definir a largura inicial da vida do personagem
initial_health = 100

# Definir a velocidade de perda de vida (em porcentagem por segundo)
health_loss_speed = 2

# Definir o tempo inicial do jogo
start_time = pygame.time.get_ticks()

# Função para calcular a porcentagem da vida restante
def calculate_health_percentage():
    current_time = pygame.time.get_ticks()  # Obter o tempo atual
    elapsed_time = (current_time - start_time) / 1000  # Converter para segundos
    remaining_health = initial_health - health_loss_speed * elapsed_time
    return max(remaining_health, 0) / initial_health

# Loop principal do jogo
while True:
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calcular a porcentagem de vida restante
    health_percentage = calculate_health_percentage()

    # Limpar a tela
    screen.fill(BLACK)

    # Desenhar o círculo externo do medidor de vida
    pygame.draw.circle(screen, WHITE, (meter_x, meter_y), meter_radius + meter_border_width)

    # Desenhar o círculo interno do medidor de vida
    pygame.draw.circle(screen, RED, (meter_x, meter_y), int(meter_radius * health_percentage))

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros por segundo (FPS)
    pygame.time.Clock
