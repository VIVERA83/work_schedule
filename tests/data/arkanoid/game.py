from random import choice

import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
ball_speed_x = 1 * choice((1, -1))
ball_speed_y = 1 * choice((1, -1))

paddle = pygame.Rect(screen_width / 2 - 90, screen_height - 20, 180, 10)
paddle_speed = 0

block_width = 60
block_height = 20
blocks = [
    pygame.Rect(x * block_width, y * block_height, block_width, block_height)
    for x in range(10)
    for y in range(6)
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_speed = -8
            if event.key == pygame.K_RIGHT:
                paddle_speed = 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_speed = 0

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(paddle):
        ball_speed_y *= -1

    for block in blocks:
        if ball.colliderect(block):
            blocks.remove(block)
            ball_speed_y *= -1

    paddle.x += paddle_speed
    if paddle.left <= 0:
        paddle.left = 0
    if paddle.right >= screen_width:
        paddle.right = screen_width

    screen.fill((0, 0, 0))
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    pygame.draw.rect(screen, (255, 255, 255), paddle)
    for block in blocks:
        pygame.draw.rect(screen, (255, 255, 255), block)

    pygame.display.flip()
