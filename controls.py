# handle keyboard (maybe mouse / gamepad in the future)
import pygame
from pygame.locals import *
import events

class KeyboardController:
    def __init__(self):
        self.heldkeys = []

    def update(self):
        # single press key events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    events.eventmanager.notify(events.Quit())
                    # send quit event

        # held keys
        self.heldkeys = pygame.key.get_pressed()
