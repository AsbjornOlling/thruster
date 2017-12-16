# Thruster game
# WIP

import pygame
from pygame.locals import *

import player
import settings

pygame.init()

# boilerplate stuff to make pygame run, winsettings etc.
display = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption("THRUSTER")
display.fill((255,255,255))
clock = pygame.time.Clock()
pygame.key.set_repeat(50, 30)

# make player sprite and group
p = player.Player()
moving_actors = pygame.sprite.RenderUpdates()
moving_actors.add(p)

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
        p.accelerate((-1, 0))
    elif keys[K_LEFT]:
        p.accelerate((1, 0))
    elif keys[K_UP]:
        p.accelerate((0, 1))
    elif keys[K_DOWN]:
        p.accelerate((0, -1))
    keys = []

    # player handling
    p.move()


    #display.blit(p.img, p.position)
    moving_actors.draw(display)

    pygame.display.update()
    settings.dt = clock.tick(settings.fps)

pygame.quit()
quit()
