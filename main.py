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

    def __init__(self):
        pg.init()
        pg.display.set_caption("THRUSTER")

        self.evm = events.EventManager()                    # communication between objects
        self.evm.add_listener(self)
        self.gm = game.Game(self.RES, self.evm)             # game model
        self.vw = view.Viewer(self.RES, self.gm, self.evm)  # visuals
        self.kb = controls.KeyboardController(self.evm)     # handle keyboard events


    def run(self):
        # create room, player
        self.gm.start()
        while True:
            self.kb.update()  # get keyboard events
            self.gm.update()  # update game model
            self.vw.update()  # draw for the player
            self.gm.tick()    # wait 1/60th second


    # handle events received
    def notify(self, event):
        if isinstance(event, events.Quit):
            self.cleanup()


    # run on exit
    def cleanup(self):
        pg.quit()
        quit()


if __name__ == "__main__":
    app = App()
    app.run()
