#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" THRUSTER (working title)
is a rogue-lite top-down physics-based sci-fi game.
The objective is to survive as long as possible,
without running out of fuel or crashing your ship.

Written by Asbjørn Olling, winter 2017/2018.
"""

# third party imports
import pygame as pg

# game modules
import events
import game
import view
import controls


class App:
    """Main class.

    Contains the main game objects and runs the program.
    """
    WIDTH, HEIGHT = RES = (1280, 720)

    def __init__(self):
        pg.init()
        pg.display.set_caption("THRUSTER")

        self.evm = events.EventManager()        # communication between objects
        self.evm.add_listener(self)
        self.gm = game.Game(self.RES, self.evm)             # game model
        self.vw = view.Viewer(self.RES, self.gm, self.evm)  # visuals
        self.kb = controls.KeyboardController(self.evm)     # handle keyboard

    def run(self):
        """Start game and run main loop.

        This method is never completed.
        """
        # create room, player
        self.gm.start()
        while True:
            self.kb.update()  # get keyboard events
            self.gm.update()  # update game model
            self.vw.update()  # draw for the player
            self.gm.tick()    # wait 1/60th second

    def notify(self, event):
        """Receive events from eventmanager.

        Receives all events, only acts on some.

        The App object only acts on Quit events.
        """
        if isinstance(event, events.Quit):
            self.cleanup()

    # run on exit
    def cleanup(self):
        """Method to be run for application close.

        At the moment, it just closes pygame then quit.
        """
        pg.quit()
        quit()


if __name__ == "__main__":
    app = App()
    app.run()
