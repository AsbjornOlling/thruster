# Thruster game
# WIP

import pygame
from pygame.locals import *

import player
import settings

class Game:
    def __init__(self):
        # pygame stuff
        pygame.init()
        self.clock = pygame.time.Clock()
        # key repeat
        pygame.key.set_repeat(50, 30)
        #display settings
        self.screen = pygame.display.set_mode((settings.width, settings.height))
        pygame.display.set_caption("THRUSTER")

        # initial render
        self.screen.fill(settings.color_bg)
        pygame.display.update()

        # make player and group
        self.p = player.Player()

    def on_render(self):
        # background
        self.screen.fill(settings.color_bg)
        # sprites
        pygame.display.update(settings.allsprites.draw(self.screen))

    def on_event(self):
        # main event handler
        for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT:
                self.on_cleanup()

            # keyhandling w/o holding
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    self.on_cleanup()

        # key handling w/ holding
        keys = pygame.key.get_pressed()
        # arrow keys for movement
        if keys[K_RIGHT]:
            self.p.accelerate((-1, 0))
        elif keys[K_LEFT]:
            self.p.accelerate((1, 0))
        elif keys[K_UP]:
            self.p.accelerate((0, 1))
        elif keys[K_DOWN]:
            self.p.accelerate((0, -1))

    def on_cleanup():
        pygame.quit()
        quit()

    def on_execute(self):
        while True:
            self.on_event()
            settings.allsprites.update()
            self.on_render()

            # tick
            settings.dt = self.clock.tick(settings.fps)

if __name__ == "__main__":
    game = Game()
    game.on_execute() # main game loop
