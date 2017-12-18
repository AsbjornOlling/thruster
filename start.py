# Thruster game
# WIP

import pygame
from pygame.locals import *
import settings
import game
import player

class App:
    def __init__(self):
        # pygame stuff
        pygame.init()
        pygame.key.set_repeat(50, 30)

        #display settings
        pygame.display.set_caption("THRUSTER")

        # make player obj
        self.p = player.Player()


    # Clear, update, draw
    def on_render(self):
        pygame.display.update(settings.allsprites.draw(game.screen))

        # temp fix for thruster rendering
        pygame.display.update()
        game.screen.fill(settings.color_bg)


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


if __name__ == "__main__":
    app = App()
    game = game.Game()
    # main loop
    while True:
        # handle keyboard events
        app.on_event()
        # update all sprites
        app.allsprites.update()
        # draw everything
        app.on_render()

        # tick
        game.dt = game.clock.tick(settings.fps)
