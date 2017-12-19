import math
import pygame
import game
import view
import events
import settings

class Player(pygame.sprite.Sprite):
    posx = 250.0 # double precision pos
    posy = 250.0
    speedmod = 0.0005
    bounce_factor = -0.8 # must be between -1 and 0
    

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # add listener
        events.evm.add_listener(self)

        # groups
        game.allsprites.add(self)
        game.singleplayer.add(self)
        self.attached = pygame.sprite.Group()
        self.thrusters = pygame.sprite.Group()

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
        delta = self.speed * game.dt * self.speedmod
        self.posx += delta[0]
        self.posy += delta[1]

        # walls - these should probably be their own sprites
        if self.posx < 0 or self.posx + self.rect.width > view.vw.width: 
            self.speed[0] *= self.bounce_factor
        if self.posy < 0 or self.posy + self.rect.height > view.vw.height: 
            self.speed[1] *= self.bounce_factor


    # thruster sprite and acceleration
    def thrust(self, direction):
        # look for thruster
        thruster_found = False
        for thruster in self.thrusters:
            if thruster.side == direction:
                thruster_found = True
                thruster.scale(1)
        # make one if it wasn't there
        if not thruster_found:
            thruster = Thruster(direction)
            self.thrusters.add(thruster)

        # accelerate
        if direction == "W":
            self.accelerate((1, 0))
        elif direction == "E":
            self.accelerate((-1, 0))
        elif direction == "N":
            self.accelerate((0, 1))
        elif direction == "S":
            self.accelerate((0, -1))
        
    
    # takes a tuple vector, adds it to speed vector
    def accelerate(self, change):
        self.speed += tuple(c * game.dt for c in change)


    def notify(self, event):
        if isinstance(event, events.PlayerThrust):
            self.thrust(event.direction)


# thruster animation attached to main player
class Thruster(pygame.sprite.Sprite):
    # inits and constants
    posx = 0.0
    posy = 0.0
    length = 20.0 # can be height or width
    width = 10.0
    shrinkrate = -0.5 


    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)
        
        self.side = direction
        self.player = game.singleplayer.sprite

        # groups
        game.allsprites.add(self)
        self.player.attached.add(self)
        self.player.thrusters.add(self)

        # image because apparently there needs to be one
        # just a 1x1 alpha pixel png
        self.image = pygame.image.load("0.png").convert_alpha()

        # find thruster position
        if self.side == "W" or self.side == "E":
            self.posy = self.player.posy + self.player.rect.height/2 - self.width/2
            if self.side == "W":
                self.posx = self.player.posx - self.length
            elif self.side == "E":
                self.posx = self.player.posx + self.player.rect.width

        elif self.side == "N" or self.side == "S":
            self.posx = self.player.posx + self.player.rect.width/2 - self.width/2
            if self.side == "N":
                self.posy = self.player.posy - self.length
            if self.side == "S":
                self.posy = self.player.posy + self.player.rect.width

        # make bounding box
        self.rect = self.make_box()


    # make bounding box
    def make_box(self):
        if self.side == "W" or self.side == "E":
            self.posy = self.player.posy + self.player.rect.height/2 - self.width/2
            if self.side == "W":
                self.posx = self.player.posx - self.length
            elif self.side == "E":
                self.posx = self.player.posx + self.player.rect.width
            # return horizontal thruster
            return pygame.Rect((self.posx, self.posy), (self.length, self.width))

        elif self.side == "N" or self.side == "S":
            self.posx = self.player.posx + self.player.rect.width/2 - self.width/2
            if self.side == "N":
                self.posy = self.player.posy - self.length
            elif self.side == "S":
                self.posy = self.player.posy + self.player.rect.height
            # return vertical thruster
            return pygame.Rect((self.posx, self.posy), (self.width, self.length))


    def update(self):
        # shrink flame a little
        self.scale(-0.5)
        # remove sprite when gone
        if self.length < 1:
            self.kill()

        self.rect = self.make_box()


    # extend or shorten the thruster
    def scale(self, amount):
        self.length += amount

        # make new bounding box
        self.make_box()
