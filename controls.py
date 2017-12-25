# handle input
import pygame as pg
from pygame.locals import *
import events

class KeyboardController:
    def __init__(self, eventmanager):
        self.evm = eventmanager

    # run on every tick
    def update(self):

        # single-press events
        for event in pg.event.get():
            if event.type == KEYDOWN:
                # Q: exit game
                if event.key == K_q:
                    self.evm.notify(events.Quit())

        # get held keys
        keystate = pg.key.get_pressed()
        
        # arrow key movement
        # allow multiple simultaneous
        if keystate[K_RIGHT]:
            self.evm.notify(events.PlayerThrust("E"))
        if keystate[K_LEFT]:
            self.evm.notify(events.PlayerThrust("W"))
        if keystate[K_UP]:
            self.evm.notify(events.PlayerThrust("N"))
        if keystate[K_DOWN]:
            self.evm.notify(events.PlayerThrust("S"))
