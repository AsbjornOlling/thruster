import pygame as pg
import math
import utils

# other game files
import game
import events
import animation as ani

class Player(pg.sprite.Sprite):
    # sprite size
    width = 32
    height = 32

    # movement constants
    speedmod = 100
    bounce_factor = -0.8  # must be between -1 and 0
    brake_factor = -0.1  # small negative number
    brake_minspeed = 1.5  # length of speedvector
    maxfuel = 100.0
    fuel_refillrate = 5  # per time unit


    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)

        # gamestate
        self.gm = game

        # event listener
        self.evm = game.evm
        self.evm.add_listener(self)

        # sprite groups
        game.allsprites.add(self)
        game.onscreen.add(self)
        self.allsprites = pg.sprite.Group()
        self.thrusters = pg.sprite.Group()
        self.brakeshots = pg.sprite.Group()

        # start in good conditions
        self.fuel = self.maxfuel
        self.dead = False

        # spawn at room center
        self.posx = game.currentroom.CENTER[0] - self.width/2
        self.posy = game.currentroom.CENTER[1] - self.height/2

        # speed vector and initial position
        self.speed = pg.math.Vector2()

        # image and bounding box
        self.image = pg.image.load("ship_placeholder.png").convert()
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.move()


    # run on every tick
    def update(self):
        self.move()
        # update bounding box position
        self.rect.x = self.posx
        self.rect.y = self.posy

        # refill fuel
        if not self.dead:
            self.add_fuel(self.fuel_refillrate * self.gm.dt)

        # detect leaving room
        if self.rect.right < self.gm.currentroom.LEFT:
            self.evm.notify(events.RoomExit("W"))
        elif self.posx > self.gm.currentroom.RIGHT:
            self.evm.notify(events.RoomExit("E"))
        elif self.rect.bottom < 0:
            self.evm.notify(events.RoomExit("N"))
        elif self.rect.top > self.gm.HEIGHT:
            self.evm.notify(events.RoomExit("S"))


    # run on event receive
    def notify(self, event):
        if isinstance(event, events.PlayerThrust) and not self.dead:
            self.thrust(event.direction)
        elif isinstance(event, events.PlayerBrake) and not self.dead:
            self.brake()


    # thruster sprite and acceleration
    def thrust(self, direction):
        # look for existing thruster
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


    # "brakeshot" - stops momentum, deals a lot of damage
    def brake(self):
        if self.speed.length() > self.brake_minspeed:
            newspeed = self.brake_factor * self.speed
            self.speed = newspeed
            self.brakeshots.add(BrakeShot(self.speed, self.gm))
        else:
            print("Going too slow to brake")


    # adds a vector to the speed vector
    def accelerate(self, change):
        self.speed += tuple(c * self.gm.dt for c in change)


    # add an amount of fuel
    def add_fuel(self, amount):
        if self.fuel < self.maxfuel:
            self.fuel += amount


    # remove fuel if there's any
    def remove_fuel(self, amount):
        # if there's enough fuel left
        if self.fuel - amount > 0:
            self.fuel -= amount
        elif not self.dead:
            print("DEATH")
            self.fuel = 0
            self.dead = True


    # calculate new position, including bouncing
    def move(self):
        delta = self.speed * self.gm.dt * self.speedmod
        self.posx += delta[0]
        self.posy += delta[1]

        # bounce off of stuff
        hardcolls = pg.sprite.spritecollide(self, self.gm.hardcollide, 0)
        for obj in hardcolls: 
            if obj in self.gm.onscreen:
                self.bounce(obj)


    # bounce off of walls
    # TODO take damage
    def bounce(self, obj):
        # find closest point on collision object
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

        # determine which side hit
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


# thruster animation attached to main player
# grows, shrinks and collides - but doesnt't accelerate shit
class Thruster(pg.sprite.Sprite):
    length = 20.0  # could be height or width
    width = 10.0
    max_length = 75
    shrinkrate = -200  # used on every update
    growthrate = 220  # used only when key held
    width_growth_ratio = 0.20  # times length growth rate
    damage_mod = 1
    fuel_consumption = 5


    def __init__(self, direction, game, eventmanager):
        pg.sprite.Sprite.__init__(self)

        # event listener
        self.evm = eventmanager
        self.evm.add_listener(self)

        # gamestate
        self.gm = game

        # the sprite that thruster is attached to
        self.player = self.gm.p

        # sprite groups
        game.allsprites.add(self)
        game.pvedamage.add(self)
        self.player.allsprites.add(self)
        self.player.thrusters.add(self)

        # mount-side and size
        self.side = direction

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
            and event.direction == self.side
            and self.length <= self.max_length
            and not self.player.dead):
            self.scale(self.growthrate)
            self.consume_fuel()


    # return damage dealt per time unit
    def get_damage(self):
        return int(self.length * self.damage_mod)

    
    # use fuel when powered up
    def consume_fuel(self):
        self.player.remove_fuel(self.fuel_consumption * self.gm.dt)
        

    # extend or shorten the thruster
    def scale(self, amount):
        self.length += amount * self.gm.dt
        self.width += amount * self.width_growth_ratio * self.gm.dt


    # make box considering player pos, thruster size, and side mounted
    def make_box(self):
        if self.side == "W" or self.side == "E":
            self.posy = (self.player.posy 
                         + self.player.rect.height/2 
                         - self.width/2)
            if self.side == "W":
                self.posx = self.player.posx - self.length
            elif self.side == "E":
                self.posx = self.player.posx + self.player.rect.width
            # return horizontal thruster
            return pg.Rect((self.posx, self.posy), 
                           (self.length, self.width))

        elif self.side == "N" or self.side == "S":
            self.posx = (self.player.posx 
                         + self.player.rect.width/2
                         - self.width/2)
            if self.side == "N":
                self.posy = self.player.posy - self.length
            elif self.side == "S":
                self.posy = self.player.posy + self.player.rect.height
            # return vertical thruster
            return pg.Rect((self.posx, self.posy),
                           (self.width, self.length))


# sprite for the velocity-cancelling brakeshot
class BrakeShot(pg.sprite.Sprite):
    size_mod = -750
    damage_mod = 1000

    def __init__(self, speedvector, game):
        pg.sprite.Sprite.__init__(self)

        # game objects
        self.gm = game
        self.player = game.p
        self.evm = game.evm
        self.evm.add_listener(self)

        # make vector in opposite direction from player 
        self.vector = -1 * speedvector

        # spritegroups
        self.gm.allsprites.add(self)
        self.gm.onscreen.add(self)
        self.gm.pvedamage.add(self)
        self.gm.p.allsprites.add(self)
        self.gm.p.brakeshots.add(self)

        # get angle to positive x-axis
        self.angle_d = self.vector.angle_to(pg.math.Vector2((1, 0)))
        self.angle_r = math.radians(self.angle_d)

        # load animation
        self.animation = ani.Animation("brakeblast.png", 64)
        self.image = self.animation.get_frame_no(0).convert_alpha()

        # find center for new rect by rotating a pre-defined center
        # TODO generalize this magic constant to enable scaling
        center_rightx =  self.player.rect.centerx + 50
        center_righty = self.player.rect.centery
        center_right = (center_rightx, center_righty)
        newcenter = utils.rotate_point(self.player.rect.center, center_right, -1 * self.angle_r)

        # get rect from image
        self.rect = pg.transform.rotate(self.image, self.angle_d).get_rect(center = newcenter)

        print(str(self.vector.length()))
        print(self.rect)


        # bool to ensure only dealing damage once
        self.damage_dealt = False


    # run on every tick
    def update(self):
        # get frame from animation
        self.image = self.animation.step_forward()
        # rotate frame 
        self.image = pg.transform.rotate(self.image, self.angle_d)

        # kill timer
        if self.animation.frameno == self.animation.noofframes - 1:
            self.evm.notify(events.ObjDeath(self.rect))
            self.kill()


    # deal with eventmanager events
    def notify(self, event):
        pass


    # return damage - only once
    def get_damage(self):
        return self.vector.length() * self.damage_mod
