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

        # init time
        self.clock = pg.time.Clock()
        self.tick()

    def update(self):
        self.allsprites.update()

    def tick(self):
        self.dt = self.clock.tick(60)

    def start(self):
        # make a room (temp)
        # for room testing
        self.currentroom = Room(self)

        # make player
        self.p = player.Player(self, self.evm)


# contains a sprite group w/ walls
class Room:
    wallthickness = 10

    def __init__(self, game):
        WIDTH, HEIGHT = game.screensize
        self.gm = game

        # make walls along screen edges
        self.wall_w = Wall((0, 0), 
                           (self.wallthickness, HEIGHT), 
                           game)

        self.wall_e = Wall((WIDTH - self.wallthickness, 0), 
                           (self.wallthickness, HEIGHT),
                           game)

        self.wall_n = Wall((0, 0), 
                           (WIDTH, self.wallthickness),
                           game)


        self.wall_s = Wall((0, HEIGHT - self.wallthickness), 
                           (WIDTH, self.wallthickness),
                           game)

        # a destructible block
        self.wall_c = WallDestructible((150, 150), 
                                       (50, 50),
                                       game)

        # sprite groups
        self.walls = pg.sprite.Group()
        
        # add walls to group
        # TODO do in constructor
        self.walls.add(self.wall_w)
        self.walls.add(self.wall_e)
        self.walls.add(self.wall_n)
        self.walls.add(self.wall_s)
        self.walls.add(self.wall_c)


# dumb block, for the player to bounce off
class Wall(pg.sprite.Sprite):
    def __init__(self, pos, size, game):
        pg.sprite.Sprite.__init__(self)

        # external objects
        self.gm = game
        self.evm = game.evm

        # sprite groups
        game.allsprites.add(self)
        game.hardcollide.add(self)
        
        # empty image
        self.image = pg.image.load("0.png")

        # rect using constructor args
        self.rect = pg.Rect(pos, size)


# a dumb block, that takes damage from thrusters
class WallDestructible(Wall):
    def __init__(self, pos, size, game):
        super(WallDestructible, self).__init__(pos, size, game)
        self.health = 100

    # run on every tick
    def update(self):
        # check for collision with player thrusters
        collisions = pg.sprite.spritecollide(self, self.gm.player.sprite.thrusters, 0)

        for thruster in collisions:
            # subtract health
            self.health -= thruster.length * self.gm.dt / 1000

        # kill if no health
        if self.health < 1:
            print("Wall DEATH")
            self.evm.notify(events.ObjDeath(self.rect))
            self.kill()
