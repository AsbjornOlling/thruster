# viewer module
import pygame
import game

# some constants
width = 500
height = 500
fps = 60

# colors
color_bg = (0, 0, 0)        # just black
color_flame = (128, 0, 0)   # just red

# pygame display surface
screen = pygame.display.set_mode((width, height))
# pygame display surface
screen = pygame.display.set_mode((width, height))


def render():
    # clear screen
    screen.fill(color_bg)

    # draw and update changed rects only
    pygame.display.update(game.allsprites.draw(screen))
