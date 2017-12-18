# Thruster game
# WIP

import pygame
from pygame.locals import *
import game
import view
import player
import settings

class App:
    def __init__(self):
        # pygame stuff
        pygame.init()
        pygame.key.set_repeat(50, 30)

        #display settings
        pygame.display.set_caption("THRUSTER")

        # make player obj
        self.p = player.Player()


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

        # TODO all this should be a controller object
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


if __name__ == "__main__":
    app = App()
    # main loop
    while True:
        # handle keyboard events
        app.on_event()
        # update all sprites
        game.allsprites.update()
        # draw everything
        view.render()

        # tick
        game.dt = game.clock.tick(view.fps)
