# this file contains settings and constants that need to be acessible from all game files
import pygame

# constants
width = 500
height = 500
fps = 60
# colors
color_bg = (0, 0, 0)


# dynamic game objects
# delta time 
dt = 0
# sprite groups
allsprites = pygame.sprite.RenderUpdates()
playergroup = pygame.sprite.GroupSingle()
playerattached = pygame.sprite.Group()
thrustergroup = pygame.sprite.Group()
