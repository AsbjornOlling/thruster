# Thruster game WIP 
import pygame as pg

# game files
import events
import game
import view
import controls

class App:
    # design resolution
    WIDTH, HEIGHT = RES = (1280, 720)

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
    gm = game.Game(app.RES, evm)

    # viewer
    vw = view.Viewer(app.RES, gm, evm)

    # controller
    kb = controls.KeyboardController(evm)
    
    # load objects and start game
    gm.start()

    # main loop
    while True:
        # handle keyboard events
        kb.update()
        # update all sprites
        gm.update()
        # draw everything
        vw.update()

        gm.tick()
