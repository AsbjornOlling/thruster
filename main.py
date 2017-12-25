# Thruster game WIP 
import pygame as pg
from pygame.locals import *

# other game files
import events

import game
import view
import controls

class App:
    # design resolution
    WIDTH, HEIGHT = RES = (1366, 768)

    def __init__(self, eventmanager):
        pg.init()
        # window title
        pg.display.set_caption("THRUSTER")

        # event manager
        self.evm = eventmanager
        self.evm.add_listener(self)

    # receive events from evm
    def notify(self, event):
        if isinstance(event, events.Quit):
            self.cleanup()

    def cleanup(self):
        pg.quit()
        quit()


if __name__ == "__main__":
    # mediator
    evm = events.EventManager()

    # main app object
    app = App(evm)

    # model
    g = game.Game(app.RES, evm)

    # viewer
    vw = view.Viewer(g, app.RES, evm)

    # controller
    kb = controls.KeyboardController(evm)
    

    # main loop
    while True:
        # handle keyboard events
        kb.update()
        # update all sprites
        g.allsprites.update()
        # draw everything
        vw.update()

        # tick TODO move this into model
        g.dt = g.clock.tick(view.vw.fps)
