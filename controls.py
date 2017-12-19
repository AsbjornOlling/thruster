# handle keyboard (maybe mouse / gamepad in the future)
import pygame
from pygame.locals import *
import events

class KeyboardController:
    def __init__(self):
        pass

    def update(self):
        # single press key events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    events.evm.notify(events.Quit())
                    # send quit event

        # handle held keys
        keystate = pygame.key.get_pressed()
        if keystate[K_RIGHT]:
            events.evm.notify(events.PlayerThrust("E"))
        elif keystate[K_LEFT]:
            events.evm.notify(events.PlayerThrust("W"))
        elif keystate[K_UP]:
            events.evm.notify(events.PlayerThrust("N"))
        elif keystate[K_DOWN]:
            events.evm.notify(events.PlayerThrust("S"))
