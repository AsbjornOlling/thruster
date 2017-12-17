import pygame
import math
import settings

class Player(pygame.sprite.Sprite):
    speedmod = 0.0005
    bounce_factor = -0.8 # must be between -1 and 0
    posx = 0.0
    posy = 0.0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # groups
        settings.allsprites.add(self)
        settings.playergroup.add(self)

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
        # update bounding box position
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
        thurst_sprite = Thruster("N")
        thurst_sprite = Thruster("W")
        thurst_sprite = Thruster("E")
        thurst_sprite = Thruster("S")


class Thruster(pygame.sprite.Sprite):
    posx = 0.0
    posy = 0.0
    length = 50
    width = 10

    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        settings.allsprites.add(self)

        self.side = direction

        # image
        self.image = pygame.image.load("flame-single_placeholder.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.length))
        # rotation
        if self.side == "W":
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.side == "E":
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.side == "S":
            self.image = pygame.transform.rotate(self.image, 180)

        # bounding box
        self.rect = self.image.get_rect()



    def update(self):
        # find position relative to player
        player = settings.playergroup.sprite
        if self.side == "W" or self.side == "E":
            self.posy = player.posy + player.rect.height/2 - self.rect.height/2
            if self.side == "W":
                self.posx = player.posx - self.rect.width
            elif self.side == "E":
                self.posx = player.posx + self.rect.width
        elif self.side == "N" or self.side == "S":
            self.posx = player.posx + player.rect.width/2 - self.rect.width/2
            if self.side == "N":
                self.posy = player.posy - self.rect.height
            if self.side == "S":
                self.posy = player.posy + player.rect.width

        self.rect.x = self.posx
        self.rect.y = self.posy

