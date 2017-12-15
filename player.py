import pygame
import math
import settings

class Player:
    health = 100
    speedmod = 0.0005

    def __init__(self):
        self.position = pygame.math.Vector2()
        self.speed = pygame.math.Vector2()

        # load and scale image assets
        self.img = pygame.image.load("ship_placeholder.png").convert()
        self.img = pygame.transform.scale(self.img, (50, 50))

    def move(self):
        self.position += self.speed * self.speedmod * settings.dt

    def accelerate(self, change):
        self.speed += tuple(c * settings.dt for c in change)
