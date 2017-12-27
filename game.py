# container file for game states, rooms, etc.
import pygame as pg
import player
import events

class Game:
    marginw = 150

    def __init__(self, screensize, eventmanager):
        # eventmanager
        # not listening atm, but passes to player
        self.evm = eventmanager

        # sprite groups
        self.allsprites = pg.sprite.RenderUpdates()
        self.player = pg.sprite.GroupSingle()
        self.hardcollide = pg.sprite.Group()

        # init time
        self.clock = pg.time.Clock()
        self.tick()

        # screen size
        self.screenw, self.screenh = self.screensize = screensize
        # room size
        self.roomsize = self.roomw, self.roomh = (self.screenw - 2*self.marginw,
                                                  self.screenh)

    def update(self):
        self.allsprites.update()

    def tick(self):
        # tick at 60fps
        self.dt = self.clock.tick(60)

    def start(self):
        # make a room (temp)
        # for room testing
        self.currentroom = Room(self)

        # make player
        self.p = player.Player(self)


# contains a sprite group w/ walls
class Room:
    wallthickness = 25
    gatelength = 200

    def __init__(self, game):
        # game model
        self.gm = game

        # room dimensions
        self.width, self.height = game.roomsize
        self.left = game.marginw
        self.right = self.left + self.width
        self.center = (self.left + self.width/2, self.height/2)

        # sprite groups
        self.walls = pg.sprite.Group()

        # make outer walls
        nongateh = (self.height - self.gatelength)/2
        # west wall w/ gate
        wall_wtop = Wall((self.left, 0), 
                         (self.wallthickness, nongateh), 
                         self,
                         game)

        wall_wgate = WallDestructible((self.left, nongateh), 
                                      (self.wallthickness, self.gatelength), 
                                      self,
                                      game)

        wall_wbottom = Wall((self.left, self.gatelength + nongateh),
                            (self.wallthickness, nongateh),
                            self,
                            game)

        # east wall w/ gate
        wall_etop = Wall((self.right - self.wallthickness, 0), 
                         (self.wallthickness, nongateh), 
                         self,
                         game)

        wall_egate = WallDestructible((self.right - self.wallthickness, nongateh), 
                                      (self.wallthickness, self.gatelength), 
                                      self,
                                      game)

        wall_ebottom = Wall((self.right - self.wallthickness, self.gatelength + nongateh),
                            (self.wallthickness, nongateh),
                            self,
                            game)
        
        # north wall w/ gate
        nongatew = (self.width - self.gatelength)/2
        wall_nleft = Wall((self.left, 0), 
                         (nongatew, self.wallthickness),
                         self,
                         game)

        wall_ngate = WallDestructible((self.left + nongatew, 0), 
                                      (self.gatelength, self.wallthickness),
                                      self,
                                      game)

        wall_nright = Wall((self.right - nongatew, 0), 
                            (nongatew, self.wallthickness),
                            self,
                            game)

        # south wall w/ gate
        wall_stop = Wall((self.left, self.height - self.wallthickness), 
                         (nongatew, self.wallthickness),
                         self,
                         game)

        wall_sgate = WallDestructible((self.left + nongatew, self.height - self.wallthickness), 
                                      (self.gatelength, self.wallthickness),
                                      self,
                                      game)

        wall_stop = Wall((self.right - nongatew, self.height - self.wallthickness), 
                         (nongatew, self.wallthickness),
                         self,
                         game)

        # a destructible block in the middle
        self.wall_c = WallDestructible((self.left + self.width/3, self.height/3), 
                                       (50, 50),
                                       self,
                                       game)

        
        # add walls to group
        # TODO do in constructor
        self.walls.add(self.wall_c)


# dumb block, for the player to bounce off
class Wall(pg.sprite.Sprite):
    def __init__(self, pos, size, room, game):
        pg.sprite.Sprite.__init__(self)

        # external objects
        self.gm = game
        self.evm = game.evm

        # sprite groups
        game.allsprites.add(self)
        game.hardcollide.add(self)
        room.walls.add(self)
        
        # empty image
        self.image = pg.image.load("0.png")

        # rect using constructor args
        self.rect = pg.Rect(pos, size)


# a dumb block, that takes damage from thrusters
class WallDestructible(Wall):
    def __init__(self, pos, size, room, game):
        super(WallDestructible, self).__init__(pos, size, room, game)
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
