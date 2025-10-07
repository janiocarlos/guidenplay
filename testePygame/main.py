import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo do Protagonista")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações do protagonista
player_width = 50
player_height = 50
player_x = 50
player_y = SCREEN_HEIGHT // 2 - player_height // 2
player_speed = 17

# Configurações dos obstáculos
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacle_frequency = 25  # Frequência de aparecimento dos obstáculos
obstacles = []

# Relógio para controlar o FPS
clock = pygame.time.Clock()

# Função para desenhar o protagonista
def draw_player(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, player_width, player_height])

# Função para desenhar os obstáculos
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

# Função principal do jogo
def game_loop():
    global player_y, player_x, obstacles  # Adicionamos 'obstacles' como global

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimentação do protagonista
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_height:
            player_y += player_speed

        # Movimentação dos obstáculos
        for obstacle in obstacles:
            obstacle.x -= obstacle_speed

        # Geração de novos obstáculos
        if random.randint(1, obstacle_frequency) == 1:
            obstacle_y = random.randint(0, SCREEN_HEIGHT - obstacle_height)
            obstacles.append(pygame.Rect(SCREEN_WIDTH, obstacle_y, obstacle_width, obstacle_height))

        # Remover obstáculos que saíram da tela
        obstacles = [obstacle for obstacle in obstacles if obstacle.x > -obstacle_width]

        # Limpa a tela
        screen.fill(WHITE)

        # Desenha o protagonista e os obstáculos
        draw_player(player_x, player_y)
        draw_obstacles(obstacles)

        # Atualiza a tela
        pygame.display.update()

        # Controla o FPS
        clock.tick(30)

    pygame.quit()

# Executa o jogo
game_loop()