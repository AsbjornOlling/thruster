import pygame

class Game:
    dt = 0

    def __init__(self):
        self.clock = pygame.time.Clock()

        # make sprite groups
        self.allsprites = pygame.sprite.RenderUpdates()

        # display surface
        self.screen = pygame.display.set_mode((width, height))
