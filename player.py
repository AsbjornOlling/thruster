import pygame
import math
import settings

class Player(pygame.sprite.Sprite):
    speedmod = 0.0005
    bounce_factor = -0.8
    posx = 0.0
    posy = 0.0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # speed vector
        self.speed = pygame.math.Vector2()

        # load and scale image
        self.image = pygame.image.load("ship_placeholder.png").convert()
        self.image = pygame.transform.scale(self.image, (50, 50))

        # bounding box
        self.rect = self.image.get_rect()


    def update(self):
        # get new position
        self.move()
        # put bounding box to position
        self.rect.x = self.posx
        self.rect.y = self.posy


    def move(self):
        # calculate new position
        delta = self.speed * settings.dt * self.speedmod
        self.posx += delta[0]
        self.posy += delta[1]

        # bouncing off walls
        if self.posx < 0 or self.posx + self.rect.width > settings.width: 
            self.speed[0] *= self.bounce_factor
        if self.posy < 0 or self.posy + self.rect.height > settings.height: 
            self.speed[1] *= self.bounce_factor

    
    # takes a tuple vector, adds it to speed vector
    def accelerate(self, change):
        self.speed += tuple(c * settings.dt for c in change)
        print("Speed: " + str(self.speed))
