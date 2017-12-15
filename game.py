# Thruster game
# WIP
# Asbjørn Olling

import pygame
from pygame.locals import *

import player
import settings

pygame.init()

# boilerplate stuff to make pygame run, window settings etc.
display = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption("THRUSTER")
display.fill((255,255,255))
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 30)

# make player
p = player.Player()

crashed = False
while not crashed:

    for event in pygame.event.get():
        # exit game
        if event.type == pygame.QUIT:
            crashed = True

        elif event.type == KEYDOWN:
            if event.key == K_q:
                crashed = True

    # key handling w/ holding
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        p.accelerate(1)
    elif keys[K_LEFT]:
        p.accelerate(-1)

    # player handling
    p.move()

    display.blit(p.img, p.position)


    pygame.display.update()
    clock.tick(clock.get_fps())

pygame.quit()
quit()
