# container file for game states, rooms, etc.
import pygame as pg
import player
import events

class Game:
    dt = 0

    def __init__(self, screensize, eventmanager):
        # eventmanager
        # not listening atm, but passes to player
        self.evm = eventmanager

        # screen size
        self.screenw, self.screenh = self.screensize = screensize

        # sprite groups
        self.allsprites = pg.sprite.RenderUpdates()
        self.singleplayer = pg.sprite.GroupSingle()
        self.hardcollide = pg.sprite.Group()

        # time vars
        self.clock = pg.time.Clock()

    def update(self):
        self.allsprites.update()

    def tick(self):
        self.dt = self.clock.tick(self.clock.get_fps())

    def start(self):
        # make player
        self.p = player.Player(self, self.evm)

        # make a room (temp)
        # for room testing
        self.currentroom = Room(self, self.screensize)


# contains a sprite group w/ walls
class Room:
    wallthickness = 10

    def __init__(self, game, screensize):
        WIDTH, HEIGHT = screensize

        self.gm = game

        # make walls along screen edges
        self.wall_w = Wall(game, (0, 0), (self.wallthickness, HEIGHT))
        self.wall_e = Wall(game, (WIDTH - self.wallthickness, 0), (self.wallthickness, HEIGHT))
        self.wall_n = Wall(game, (0, 0), (WIDTH, self.wallthickness))
        self.wall_s = Wall(game, (0, HEIGHT - self.wallthickness), (WIDTH, self.wallthickness))

        # a destructible block
        self.wall_c = WallDestructible(game, (150, 150), (50, 50))

        # sprite groups
        self.walls = pg.sprite.Group()
        
        # add walls to group
        self.walls.add(self.wall_w)
        self.walls.add(self.wall_e)
        self.walls.add(self.wall_n)
        self.walls.add(self.wall_s)
        self.walls.add(self.wall_c)


# dumb block, for the player to bounce off
class Wall(pg.sprite.Sprite):
    def __init__(self, game, coordtuple, sizetuple):
        pg.sprite.Sprite.__init__(self)

        self.gm = game

        # sprite groups
        game.allsprites.add(self)
        game.hardcollide.add(self)
        
        # empty image
        self.image = pg.image.load("0.png")

        # set color TODO move color handling into view
        self.color = (128, 128, 128)

        # rect using constructor args
        self.rect = pg.Rect(coordtuple, sizetuple)


# a dumb block, that takes damage from thrusters
class WallDestructible(Wall):
    def __init__(self, game, coordtuple, sizetuple):
        super(WallDestructible, self).__init__(game, coordtuple, sizetuple)
        self.gm = game
        self.health = 100
        self.color = (200, 150, 150)

    # run on every tick
    def update(self):
        # check for collision with player thrusters
        collisions = pg.sprite.spritecollide(self, self.gm.singleplayer.sprite.thrusters, 0)
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
