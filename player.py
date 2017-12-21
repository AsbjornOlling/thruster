import math
import pygame
import game
import view
import events

class Player(pygame.sprite.Sprite):
    # starting position on spawn, float precision
    speedmod = 0.0001
    bounce_factor = -0.5 # must be between -1 and 0
    width = 50
    height = 50

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # event listener
        events.evm.add_listener(self)

        # sprite groups
        game.allsprites.add(self)
        game.singleplayer.add(self)
        self.attached = pygame.sprite.Group()
        self.thrusters = pygame.sprite.Group()

        # speed vector and initial position
        self.speed = pygame.math.Vector2()
        self.posx = view.vw.width/2
        self.posy = view.vw.height/2

        # image and bounding box
        self.image = pygame.image.load("ship_placeholder.png").convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    # run on every tick
    def update(self):
        self.move()
        # update bounding box position
        self.rect.x = self.posx
        self.rect.y = self.posy

    # run on event receive
    def notify(self, event):
        if isinstance(event, events.PlayerThrust):
            self.thrust(event.direction)

    # thruster sprite and acceleration
    def thrust(self, direction):
        # look for thruster
        thruster_found = False
        for thruster in self.thrusters:
            if thruster.side == direction:
                thruster_found = True
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

    # adds a vector argument to the speed vector
    def accelerate(self, change):
        self.speed += tuple(c * game.dt for c in change)

    # calculate new position, including bouncing
    def move(self):
        delta = self.speed * game.dt * self.speedmod
        self.posx += delta[0]
        self.posy += delta[1]

        # bounce off of stuff
        hardcolls = pygame.sprite.spritecollide(self, game.hardcollide, 0)
        for obj in hardcolls: 
            # collide up
            if (self.rect.top < obj.rect.bottom 
            and self.rect.top > obj.rect.top
            and self.rect.bottom > obj.rect.bottom):
                print("Collide up")
                self.speed[1] *= self.bounce_factor
                self.posy = obj.rect.bottom + 1

            # collide down
            elif (self.rect.bottom > obj.rect.top
            and self.rect.bottom < obj.rect.bottom
            and self.rect.top < obj.rect.top):
                print("Collide down")
                self.speed[1] *= self.bounce_factor
                self.posy = obj.rect.top - self.rect.height

            # collide left
            elif (self.rect.left > obj.rect.left
            and self.rect.left < obj.rect.right
            and self.rect.right > obj.rect.right):
                print("Collide left")
                self.speed[0] *= self.bounce_factor
                self.posx = obj.rect.right + 1

            # collide right
            elif (self.rect.right < obj.rect.right
            and self.rect.right > obj.rect.left
            and self.rect.left < obj.rect.left):
                print("Collide right")
                self.speed[0] *= self.bounce_factor
                self.posx = obj.rect.left - self.rect.width - 1
        

# thruster animation attached to main player
# grows, shrinks and collides - but doesnt't accelerate shit
class Thruster(pygame.sprite.Sprite):
    # constants for all classes
    shrinkrate = -0.2 
    growthrate = 0.22 

    def __init__(self, direction):
        pygame.sprite.Sprite.__init__(self)

        # event listener
        events.evm.add_listener(self)

        # the sprite that thruster is attached to
        self.player = game.singleplayer.sprite

        # sprite groups
        game.allsprites.add(self)
        self.player.attached.add(self)
        self.player.thrusters.add(self)

        # mount-side and size
        self.side = direction
        self.length = 40.0 # can be height or width
        self.width = 12.0

        # empty image
        self.image = pygame.image.load("0.png").convert_alpha()

        # bounding box
        self.rect = self.make_box()

    # run on every tick
    def update(self):
        self.scale(self.shrinkrate)
        if self.length < 1:
            self.kill()
        # make bounding box at new size
        self.rect = self.make_box()

    # handle events
    def notify(self, event):
        # grow when player thrusts
        if (isinstance(event, events.PlayerThrust)
        and event.direction == self.side):
            self.scale(self.growthrate)

    # extend or shorten the thruster
    def scale(self, amount):
        self.length += amount * game.dt

    # make bounding box considering player pos, thruster size, and side mounted
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
