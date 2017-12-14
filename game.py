# Thruster game
# WIP
# Asbjørn Olling

import pygame
from pygame.locals import *

pygame.init()

width = 500
height = 500
window_title = "THRUSTER"

# boilerplate stuff to make pygame run, window settings etc.
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("THRUSTER")
display.fill((255,255,255))
clock = pygame.time.Clock()

# load and scale image assets
player_img = pygame.image.load("ship_placeholder.png").convert()
player_img = pygame.transform.scale(player_img, (50, 50))

crashed = False
while not crashed:

    for event in pygame.event.get():
        # exit game
        if event.type == pygame.QUIT:
            crashed = True

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                display.fill((199,199,199))
            elif event.key == K_q:
                crashed = True

    display.blit(player_img, (0,0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
