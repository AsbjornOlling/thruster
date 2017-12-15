import pygame
import math

class Player:
    health = 100

    def __init__(self):
        self.position = pygame.math.Vector2()
        self.speed = pygame.math.Vector2()

        # load and scale image assets
        self.img = pygame.image.load("ship_placeholder.png").convert()
        self.img = pygame.transform.scale(self.img, (50, 50))

    def move(self):
        self.position += self.speed * 0.0005


    def accelerate(self, change):
        self.speed.x += change


