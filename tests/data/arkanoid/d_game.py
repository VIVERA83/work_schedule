import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Настройки платформы
platform_width = 100
platform_height = 20
platform_speed = 10
platform = pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - 50, platform_width, platform_height)

# Настройки мяча
ball_radius = 10
ball_speed_x = 5
ball_speed_y = -5
ball = pygame.Rect(WIDTH // 2 - ball_radius, HEIGHT // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# Настройки блоков
block_width = 75
block_height = 30
blocks = []
for i in range(10):
    for j in range(5):
        block = pygame.Rect(10 + i * (block_width + 10), 50 + j * (block_height + 10), block_width, block_height)
        blocks.append(block)

# Основной цикл игры
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if keys[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.right += platform_speed

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Отскок мяча от стен
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    # Отскок мяча от платформы
    if ball.colliderect(platform) and ball_speed_y > 0:
        ball_speed_y = -ball_speed_y

    # Отскок мяча от блоков
    for block in blocks[:]:
        if ball.colliderect(block):
            ball_speed_y = -ball_speed_y
            blocks.remove(block)
            break

    # Проверка на проигрыш
    if ball.bottom >= HEIGHT:
        running = False

    # Отрисовка
    win.fill((0, 0, 0))
    pygame.draw.rect(win, BLUE, platform)
    pygame.draw.ellipse(win, RED, ball)
    for block in blocks:
        pygame.draw.rect(win, GREEN, block)
    pygame.display.flip()

pygame.quit()