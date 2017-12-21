# handle input
import pygame
from pygame.locals import *
import events

class KeyboardController:
    # run on every tick
    def update(self):

        # single-press events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Q: exit game
                if event.key == K_q:
                    events.evm.notify(events.Quit())

        # get held keys
        keystate = pygame.key.get_pressed()
        
        # arrow key movement
        if keystate[K_RIGHT]:
            events.evm.notify(events.PlayerThrust("E"))
        elif keystate[K_LEFT]:
            events.evm.notify(events.PlayerThrust("W"))
        if keystate[K_UP]:
            events.evm.notify(events.PlayerThrust("N"))
        elif keystate[K_DOWN]:
            events.evm.notify(events.PlayerThrust("S"))
