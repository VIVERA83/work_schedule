import pygame
import sys
import random

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = [10, 0]

food_pos = [
    random.randrange(1, (screen_width // 10)) * 10,
    random.randrange(1, (screen_height // 10)) * 10,
]
food_spawn = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_speed = [0, -10]
            if event.key == pygame.K_DOWN:
                snake_speed = [0, 10]
            if event.key == pygame.K_LEFT:
                snake_speed = [-10, 0]
            if event.key == pygame.K_RIGHT:
                snake_speed = [10, 0]

    snake_pos[0] += snake_speed[0]
    snake_pos[1] += snake_speed[1]

    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [
            random.randrange(1, (screen_width // 10)) * 10,
            random.randrange(1, (screen_height // 10)) * 10,
        ]
    food_spawn = True

    screen.fill((0, 0, 0))
    for pos in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.display.flip()
