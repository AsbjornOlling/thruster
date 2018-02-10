"""Contains all game model classes except player-controlled ones.

This means grid map, rooms, main game object, etc.
"""

import random as r

import pygame as pg

import main
import animation as ani
import player
import events


class Game:
    """Game model class.

    This class contains all sprites and other game-logic
    essential objects, like the game clock or the grid of
    visited rooms.
    """
    MARGINW = 128  # width of HUD-panels
    WIDTH = main.App.WIDTH
    HEIGHT = main.App.HEIGHT

    def __init__(self, parent):
        self.parent = parent

        # interactions with parent object
        self.SIZE = parent.SIZE
        self.WIDTH, self.HEIGHT = self.SIZE
        self.evm = parent.evm
        self.evm.add_listener(self)

        self.clock = pg.time.Clock()
        self.tick()

        # sprite groups
        self.allsprites = pg.sprite.Group()     # all sprites in game
        self.onscreen = pg.sprite.RenderUpdates()  # visible sprites
        self.offscreen = pg.sprite.Group()      # sprites in other rooms
        self.hardcollide = pg.sprite.Group()    # player bounces off these
        self.pvedamage = pg.sprite.Group()      # items take damage from these

    def update(self):
        """Update all of the game model since last tick.

        Just runs the update method on every sprite.
        """
        self.allsprites.update()

    def notify(self, event):
        """Receive events from eventmanager.

        The Game object only cares about the player
        going into a new room.
        """
        if isinstance(event, events.RoomExit):
            self.move_rooms(event.direction)

    def tick(self):
        """Keeps time.

        Keeps game updating at 60fps, and keeps track
        of differences in time. To be run every updateloop.
        """
        self.dt = self.clock.tick(60) / 1000.0

    def start(self):
        """Create objects needed to begin.

        Make a grid to contain map of rooms.
        Then make starting room and player object.
        """
        # make empty 512x512 grid
        # top left is (0,0)
        gridsize = 512
        self.visitedrooms = []
        for i in range(0, gridsize):
            column = [None] * gridsize
            self.visitedrooms.append(column)
        # make room and player
        self.currentroom = Room(self, (255, 255))
        self.p = player.Player(self)

    def move_rooms(self, direction):
        """Move curentroom offscreen and create new room.

        direction: single-char signifying which gate
        the player left through.
        """

        # find gridcoord of room and entrypoint coord for player
        if direction == "W":
            targetcoord = (self.currentroom.coord[0] - 1,
                           self.currentroom.coord[1])
            # entrypoint at E gate
            newplayerpos = (self.currentroom.RIGHT - self.p.width/2,
                            self.currentroom.CENTER[1] - self.p.height/2)
        elif direction == "E":
            targetcoord = (self.currentroom.coord[0] + 1,
                           self.currentroom.coord[1])
            # entrypoint at W gate
            newplayerpos = (self.currentroom.LEFT + self.p.width/2,
                            self.currentroom.CENTER[1] - self.p.height/2)
        elif direction == "N":
            targetcoord = (self.currentroom.coord[0],
                           self.currentroom.coord[1] - 1)
            # entrypoint at S gate
            newplayerpos = (self.currentroom.CENTER[0] - self.p.width/2,
                            self.HEIGHT - self.p.height/2)
        elif direction == "S":
            targetcoord = (self.currentroom.coord[0],
                           self.currentroom.coord[1] + 1)
            # entrypoint at N gate
            newplayerpos = (self.currentroom.CENTER[0] - self.p.width/2,
                            0 - self.p.height/2)

        # check if there's already a room
        targetroom = self.visitedrooms[targetcoord[0]][targetcoord[1]]
        if targetroom is None:
            # if not, make it
            newroom = Room(self, targetcoord)
        else:
            newroom = self.visitedrooms[targetcoord[0]][targetcoord[1]]

        # out with the old, in with the new
        self.currentroom.move_offscreen()
        self.currentroom = newroom
        self.currentroom.move_onscreen()

        # move player
        self.p.posx, self.p.posy = newplayerpos

        # clear screen of old walls and gates
        self.evm.notify(events.ClearScreen())


class Room:
    """A room, containgin walls, gates and enemies.

    Contains groups of its contents, and methods to populate itself.
    """
    # concering room contents
    WALLTHICKNESS = 48
    GATELENGTH = 200
    # room size
    WIDTH = Game.WIDTH - Game.MARGINW * 2
    HEIGHT = Game.HEIGHT
    SIZE = WIDTH, HEIGHT
    # often used positions in room
    LEFT = Game.MARGINW
    RIGHT = WIDTH + Game.MARGINW
    CENTER = (LEFT + WIDTH/2, HEIGHT/2)

    def __init__(self, game, coord):
        self.gm = game

        # sprite groups
        self.allsprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # add to world map grid
        self.coord = coord
        game.visitedrooms[coord[0]][coord[1]] = self

        # check neighbor rooms and open gates to discovered rooms
        opengates = []
        neighbor_shift = [(-1, 0, "W"), (1, 0, "E"),
                          (0, -1, "N"), (0, 1, "S")]
        for relpos in neighbor_shift:
            nx = self.coord[0] + relpos[0]
            ny = self.coord[1] + relpos[1]
            if self.gm.visitedrooms[nx][ny] is not None:
                opengates.append(relpos[2])
                print("OPEN GATE:" + str(relpos[2]))

        # make floor tiles
        self.make_floor()

        # populate room with gates and crates
        self.make_outerwalls()
        self.make_gates(opengates)
        self.make_random_crate()

    def make_floor(self):
        "Makes a surface with a grid of floor tiles"

        self.floor = pg.Surface((self.WIDTH, self.HEIGHT))
        lighttile = pg.image.load("assets/lighttile-48.png")
        blanktile = pg.image.load("assets/tile-48.png")
        tilewidth = 48  # real pixels

        tilesx = (self.WIDTH) // tilewidth
        tilesy = (self.HEIGHT) // tilewidth

        posx = 0
        posy = 0
        # loop through horizontal lines
        for i in range(0, tilesy):
            # tiles on each horiz line
            for j in range(0, tilesx):
                if posy is tilewidth and posx % 2 is 0:
                    self.floor.blit(lighttile, (posx, posy))
                else:
                    self.floor.blit(blanktile, (posx, posy))
                posx += tilewidth
            posx = 0
            posy += tilewidth

    def make_random_crate(self):
        """Make crate at random position.

        Get random coords, construct box, and add to group.
        """
        # params for pos
        blockminx = self.LEFT + self.WALLTHICKNESS
        blockmaxx = self.RIGHT - self.WALLTHICKNESS - Crate.width
        blockminy = self.WALLTHICKNESS
        blockmaxy = self.gm.HEIGHT - self.WALLTHICKNESS - Crate.height

        # generate random position
        blockx = r.randrange(blockminx, blockmaxx)
        blocky = r.randrange(blockminy, blockmaxy)

        # make the crate and add it to the room
        self.wall_c = Crate((blockx, blocky), self, self.gm)
        self.allsprites.add(self.wall_c)


    def make_outerwalls(self):
        """Make four outer walls.

        Actually eight wall objects, leaving gaps for gates.
        Walls add themselves to the appropriate spritegroup.
        This should be run in the constructor for every room.
        """
        # height of wall segments on left and rigth side
        nongateh = (self.HEIGHT - self.GATELENGTH)/2

        # west wall
        Wall((self.LEFT, 0),  # top segment   # position
             (self.WALLTHICKNESS, nongateh),  # size
             self, self.gm)                   # gamestate objects
        Wall((self.LEFT, self.GATELENGTH + nongateh),  # bottom segment
             (self.WALLTHICKNESS, nongateh),
             self, self.gm)
        # east wall
        Wall((self.RIGHT - self.WALLTHICKNESS, 0),  # top
             (self.WALLTHICKNESS, nongateh),
             self, self.gm)
        Wall((self.RIGHT - self.WALLTHICKNESS, self.GATELENGTH + nongateh),
             (self.WALLTHICKNESS, nongateh),
             self, self.gm)

        # width of wall segments on top and bottom
        nongatew = (self.WIDTH - self.GATELENGTH)/2
        # north wall
        Wall((self.LEFT, 0),  # left
             (nongatew, self.WALLTHICKNESS),
             self, self.gm)
        Wall((self.RIGHT - nongatew, 0),  # right
             (nongatew, self.WALLTHICKNESS),
             self, self.gm)
        # south wall
        Wall((self.LEFT, self.HEIGHT - self.WALLTHICKNESS),  # left
             (nongatew, self.WALLTHICKNESS),
             self, self.gm)
        Wall((self.RIGHT - nongatew, self.HEIGHT - self.WALLTHICKNESS),  # righ
             (nongatew, self.WALLTHICKNESS),
             self, self.gm)

    def make_gates(self, opengates):
        """Make gates, excluding the sides mentioned in opengates.

        Should be called from constructor.
        Passed variable opengates should be a list of chars, indicating
        which gates *not* to make.
        """
        # height of wall segments on left and rigth side
        nongateh = (self.HEIGHT - self.GATELENGTH)/2
        # width of wall segments on top and bottom
        nongatew = (self.WIDTH - self.GATELENGTH)/2

        if "W" not in opengates:
            WallDestructible((self.LEFT, nongateh),  # position
                             (self.WALLTHICKNESS/2, self.GATELENGTH),  # size
                             self, self.gm)
        if "E" not in opengates:
            WallDestructible((self.RIGHT - self.WALLTHICKNESS/2, nongateh),
                             (self.WALLTHICKNESS/2, self.GATELENGTH),  # size
                             self, self.gm)
        if "N" not in opengates:
            WallDestructible((self.LEFT + nongatew, 0),
                             (self.GATELENGTH, self.WALLTHICKNESS/2),
                             self, self.gm)
        if "S" not in opengates:
            WallDestructible((self.LEFT + nongatew, self.HEIGHT - self.WALLTHICKNESS/2),
                             (self.GATELENGTH, self.WALLTHICKNESS/2),
                             self, self.gm)

    def move_offscreen(self):
        for sprite in self.allsprites:
            self.gm.onscreen.remove(sprite)
            self.gm.offscreen.add(sprite)

    def move_onscreen(self):
        # move sprites to
        for sprite in self.allsprites:
            self.gm.offscreen.remove(sprite)
            self.gm.onscreen.add(sprite)

# "dumb" block, just for the player to bounce off
class Wall(pg.sprite.Sprite):
    def __init__(self, pos, size, room, game):
        pg.sprite.Sprite.__init__(self)

        # external objects
        self.gm = game
        self.evm = game.evm

        # sprite groups
        game.allsprites.add(self)
        game.onscreen.add(self)
        game.hardcollide.add(self)
        # room sprite groups
        room.allsprites.add(self)
        room.walls.add(self)
        
        # empty image
        self.image = pg.image.load("0.png")

        # get position
        self.posx, self.posy = pos

        # rect using constructor args
        self.rect = pg.Rect(pos, size)


# a dumb block, that takes damage from thrusters
class WallDestructible(Wall):
    def __init__(self, pos, size, room, game):
        super(WallDestructible, self).__init__(pos, size, room, game)
        self.health = 100

    # run on every tick
    def update(self):

        # take damage
        collisions = pg.sprite.spritecollide(self, self.gm.pvedamage, 0)
        for item in collisions:
            damage = item.get_damage()
            self.takedamage(damage * self.gm.dt)


    # take damage 
    def takedamage(self, amount):
        self.health -= amount
        # kill sprite if no health
        if self.health < 1:
            self.evm.notify(events.ObjDeath(self.rect))
            self.kill()


# a crate w/ crate sprite
class Crate(WallDestructible):
    width, height = size = (32, 64)
    maxhealth = 100.0

    def __init__(self, pos, room, game):
        # run parent constructor
        super(Crate, self).__init__(pos, self.size, room, game)

        print("MAKING NEW CRATE @ " + str(self.posx) + "x" + str(self.posy))

        # avoid drawing over with wall graphics
        room.walls.remove(self)

        # load crate animation (one frame)
        self.animation = ani.Animation("crate-32.png", 64)
        self.image = self.animation.get_frame_no(0)
        self.rect = self.image.get_rect()

        # update rect position
        self.rect.x = self.posx
        self.rect.y = self.posy

        # LOOK ALIVE
        self.health = self.maxhealth
        self.dead = False

    # to run on every tick
    def update(self):
        # detect collisions, take damage
        super(Crate, self).update()

        # find frame belonging to health level
        if not self.dead:
            frameno = 22 - int((self.animation.noofframes - 1)
                               / self.maxhealth
                               * self.health)

            self.image = self.animation.get_frame_no(frameno)

    def takedamage(self, amount):
        self.health -= amount
        # kill sprite if no health
        if self.health < 1:
            self.dead = True
            self.image = self.animation.get_frame_no(self.animation.noofframes - 1)
