import pygame
import math

class Player:
    x = 0
    y = 0
    speed = 0 # temp solution for speed
    speed_mod = 0.05
    health = 100
    angle = 0

    def __init__(self):

        # load and scale image assets
        self.img = pygame.image.load("ship_placeholder.png").convert()
        self.img = pygame.transform.scale(self.img, (50, 50))

    def move(self):
        self.x += math.cos(self.angle) * self.speed * 0.0005
        self.y += math.sin(self.angle) * self.speed * 0.0005

    def accelerate(self, change):
        self.speed += change


