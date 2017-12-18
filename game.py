# GAME
# conatainer file for game states, clock etc.

import pygame

# time stuff
clock = pygame.time.Clock()
dt = 0

# sprite groups
allsprites = pygame.sprite.RenderUpdates()
singleplayer = pygame.sprite.GroupSingle()
