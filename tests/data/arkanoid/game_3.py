import pygame
import sys
import random

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

minefield = [[0 for x in range(10)] for y in range(10)]
mines = 10

for i in range(mines):
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    minefield[x][y] = -1

for x in range(10):
    for y in range(10):
        if minefield[x][y] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if x + i >= 0 and x + i < 10 and y + j >= 0 and y + j < 10 and minefield[x + i][y + j] == -1:
                        minefield[x][y] += 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    for x in range(10):
        for y in range(10):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x * 64, y * 48, 64, 48), 1)
            if minefield[x][y] == -1:
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x * 64, y * 48, 64, 48))
            else:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x * 64, y * 48, 64, 48))

    pygame.display.flip()
