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
        pygame.display.set_caption("THRUSTER")

        # initial render
        settings.screen.fill(settings.color_bg)
        pygame.display.update()

        # make player and group
        self.p = player.Player()


    def on_render(self):
        # background
        
        # allsprites
        pygame.display.update(settings.allsprites.draw(settings.screen))

        # temp fix for thruster rendering
        thrusterrects = []
        for thruster in settings.thrustergroup:
            thrusterrects.append(thruster.rect)
        pygame.display.update(thrusterrects)
        pygame.display.update()

        settings.screen.fill(settings.color_bg)

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
        settings.keys = pygame.key.get_pressed()
        # arrow keys for movement
        if settings.keys[K_RIGHT]:
            self.p.thrust("E")
        elif settings.keys[K_LEFT]:
            self.p.thrust("W")
        elif settings.keys[K_UP]:
            self.p.thrust("N")
        elif settings.keys[K_DOWN]:
            self.p.thrust("S")


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
