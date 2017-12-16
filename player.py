import pygame
import math
import settings

class Player(pygame.sprite.Sprite):
    health = 100
    speedmod = 0.05

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # init position and speed
        self.pos = (0, 0)
        self.speed = pygame.math.Vector2()

        # load and scale image
        self.image = pygame.image.load("ship_placeholder.png").convert()
        self.image = pygame.transform.scale(self.image, (50, 50))

        # bounding box
        self.rect = self.image.get_rect()

    def move(self):
        new_pos = (self.speed * self.speedmod * settings.dt)
        self.rect.x = new_pos[0]
        self.rect.y = new_pos[1]

    # takes a tuple, adds it to speed vector
    def accelerate(self, change):
        self.speed += tuple(c * settings.dt for c in change)
