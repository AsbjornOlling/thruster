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

def render():
    # clear screen
    screen.fill(color_bg)

    # list of areas to update
    update_rects = []
    update_rects_next = []

    # draw all sprites and get rects
    for rect in game.allsprites.draw(screen):
        update_rects.append(rect)

    # draw player thrusters
    for thruster in game.singleplayer.sprite.thrusters:
        pygame.draw.ellipse(screen, color_flame, thruster.rect)
        update_rects.append(thruster.rect)
        update_rects_next.append(thruster.rect)

    # needs to also update previous location of thruster

    # draw and update changed rects only
    pygame.display.update(update_rects)



