import pygame as pg
import math

# other game files
import game
import events

class Player(pg.sprite.Sprite):
    # starting position on spawn, float precision
    speedmod = 0.0001
    bounce_factor = -0.5 # must be between -1 and 0
    width = 50
    height = 50

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)

        self.gm = game

        self.posx = game.screenw/2 
        self.posy = game.screenh/2

        # event listener
        self.evm = game.evm
        self.evm.add_listener(self)

        # sprite groups
        game.allsprites.add(self)
        game.player.add(self)
        self.attached = pg.sprite.Group()
        self.thrusters = pg.sprite.Group()

        # speed vector and initial position
        self.speed = pg.math.Vector2()

        # image and bounding box
        self.image = pg.image.load("ship_placeholder.png").convert()
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy

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
            thruster = Thruster(direction, self.gm, self.evm)
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
        self.speed += tuple(c * self.gm.dt for c in change)

    # calculate new position, including bouncing
    def move(self):
        delta = self.speed * self.gm.dt * self.speedmod
        self.posx += delta[0]
        self.posy += delta[1]

        # bounce off of stuff
        hardcolls = pg.sprite.spritecollide(self, self.gm.hardcollide, 0)
        for obj in hardcolls: 
            closestx = self.rect.centerx
            if self.rect.centerx > obj.rect.right:
                closestx = obj.rect.right
            elif self.rect.centerx < obj.rect.left:
                closestx = obj.rect.left
            closesty = self.rect.centery
            if self.rect.centery > obj.rect.bottom:
                closesty = obj.rect.bottom
            elif self.rect.centery < obj.rect.top:
                closesty = obj.rect.top

            # find angle between closest point and player center
            y = closesty - self.rect.centery
            x = closestx - self.rect.centerx
            angle = math.atan2(y, x)

            # debug shit
            print("OBJ:" + str(obj.rect))
            print("SLF:" + str(self.rect))

            # figure out which side hit
            coll_right = math.pi*-1/4 < angle and angle < math.pi/4
            coll_left = ((math.pi*-3/4 > angle and angle >= -1*math.pi) or
                         (math.pi*3/4 < angle and angle <= math.pi))
            coll_up = math.pi*1/4 < angle and angle < math.pi*3/4
            coll_down = math.pi*-1/4 > angle and angle > math.pi*-3/4

            if coll_right or coll_left:
                self.speed[0] *= self.bounce_factor
                if coll_right:
                    print("Colliding right")
                    self.posx = obj.rect.left - self.rect.width - 1
                elif coll_left:
                    print("Colliding left")
                    self.posx = obj.rect.right + 1

            elif coll_up or coll_down:
                self.speed[1] *= self.bounce_factor
                if coll_up:
                    print("Colliding up")
                    self.posy = obj.rect.top - self.rect.height - 1
                if coll_down:
                    self.posy = obj.rect.bottom + 1
                    print("Colliding down")

            # determine side from that

# thruster animation attached to main player
# grows, shrinks and collides - but doesnt't accelerate shit
class Thruster(pg.sprite.Sprite):
    # constants for all classes
    shrinkrate = -0.20
    growthrate = 0.22

    def __init__(self, direction, game, eventmanager):
        pg.sprite.Sprite.__init__(self)

        # event listener
        self.evm = eventmanager
        self.evm.add_listener(self)


        self.gm = game

        # the sprite that thruster is attached to
        self.player = self.gm.player.sprite

        # sprite groups
        game.allsprites.add(self)
        self.player.attached.add(self)
        self.player.thrusters.add(self)

        # mount-side and size
        self.side = direction
        self.length = 40.0 # can be height or width
        self.width = 12.0

        # empty image
        self.image = pg.image.load("0.png").convert_alpha()

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
        self.length += amount * self.gm.dt

    # make bounding box considering player pos, thruster size, and side mounted
    def make_box(self):
        if self.side == "W" or self.side == "E":
            self.posy = self.player.posy + self.player.rect.height/2 - self.width/2
            if self.side == "W":
                self.posx = self.player.posx - self.length
            elif self.side == "E":
                self.posx = self.player.posx + self.player.rect.width
            # return horizontal thruster
            return pg.Rect((self.posx, self.posy), (self.length, self.width))

        elif self.side == "N" or self.side == "S":
            self.posx = self.player.posx + self.player.rect.width/2 - self.width/2
            if self.side == "N":
                self.posy = self.player.posy - self.length
            elif self.side == "S":
                self.posy = self.player.posy + self.player.rect.height
            # return vertical thruster
            return pg.Rect((self.posx, self.posy), (self.width, self.length))
