# viewer module
import pygame
import game

# pygame display surface
screen = pygame.display.set_mode((width, height))

# some constants
width = 500
height = 500
fps = 60

# colors
color_bg = (0, 0, 0)        # just black
color_flame = (128, 0, 0)   # just red

def render():
    # draw based on a list of (changed) rects
    pygame.display.update(game.allsprites.draw(screen))

    # temp
    screen.fill(color_bg)
