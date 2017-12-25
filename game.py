# container file for game states, rooms, etc.
import pygame as pg
import player
import events

class Game:
    def __init__(self, screensize, eventmanager):
        # time vars
        clock = pg.time.Clock()

        # eventmanager
        # not listening atm, but passes to player
        self.evm = eventmanager

        # sprite groups
        allsprites = pg.sprite.RenderUpdates()
        singleplayer = pg.sprite.GroupSingle()
        hardcollide = pg.sprite.Group()

        # make player
        self.p = player.Player(self.evm)


# contains a sprite group w/ walls
class Room:
    wallthickness = 10

    def __init__(self):
        # sprite groups
        self.walls = pg.sprite.Group()

        # walls along screen edges
        self.wall_w = Wall((0, 0), (self.wallthickness, view.vw.height))
        self.wall_e = Wall((view.vw.width - self.wallthickness, 0), (self.wallthickness, view.vw.height))
        self.wall_n = Wall((0, 0), (view.vw.width, self.wallthickness))
        self.wall_s = Wall((0, view.vw.height - self.wallthickness), (view.vw.width, self.wallthickness))

        #self.walls.add(self.wall_w)
        self.walls.add(self.wall_e)
        self.walls.add(self.wall_n)
        self.walls.add(self.wall_s)

        # a destructible block
        self.wall_c = WallDestructible((150, 150), (50, 50))
        self.walls.add(self.wall_c)

        # make a room (temp)
        # for room testing
        self.currentroom = Room()

# dumb block, for the player to bounce off
class Wall(pg.sprite.Sprite):
    def __init__(self, coordtuple, sizetuple):
        print("Wall creation!")
        pg.sprite.Sprite.__init__(self)

        # sprite groups
        allsprites.add(self)
        hardcollide.add(self)
        
        # empty image
        self.image = pg.image.load("0.png")

        # set color
        self.color = view.vw.color_wall

        # rect using constructor args
        self.rect = pg.Rect(coordtuple, sizetuple)


# a dumb block, that takes damage from thrusters
class WallDestructible(Wall):
    def __init__(self, coordtuple, sizetuple):
        super(WallDestructible, self).__init__(coordtuple, sizetuple)
        self.health = 100
        self.color = view.vw.color_walldestructible

    # run on every tick
    def update(self):
        # check for collision with player thrusters
        collisions = pg.sprite.spritecollide(self, singleplayer.sprite.thrusters, 0)
        for thruster in collisions:
            # subtract health
            self.health -= thruster.length * dt / 1000
            # change color
            self.color = (self.color[0] + thruster.length / 55,
                            self.color[1], self.color[2])

        # kill if no health
        if self.health < 1:
            print("Wall DEATH")
            self.evm.notify(events.ObjDeath(self.rect))
            self.kill()

