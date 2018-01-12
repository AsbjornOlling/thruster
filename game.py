"""Contains all game model classes except player-controlled ones.

This means grid map, rooms, main game object, etc.
"""

import random as r

import pygame as pg

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
<<<<<<< HEAD
    WIDTH = 0  # class field to allow reading from Room class field
    HEIGHT = 0
=======
    WIDTH = None  # class field to allow reading from Room class field
    HEIGHT = None
>>>>>>> 62ef1756c0c048faeda78aac2fdffd7928f58517

    def __init__(self, parent):
        self.parent = parent

        # interactions with parent object
        self.SIZE = parent.SIZE
        self.WIDTH, self.HEIGHT = self.SIZE
        self.evm = parent.evm
        self.evm.add_listener(self)

        self.clock = pg.time.Clock()
        self.clock.tick()

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
            newplayerpos = (self.currentroom.right - self.p.width/2,
                            self.currentroom.center[1] - self.p.height/2)
        elif direction == "E":
            targetcoord = (self.currentroom.coord[0] + 1,
                           self.currentroom.coord[1])
            # entrypoint at W gate
            newplayerpos = (self.currentroom.left + self.p.width/2,
                            self.currentroom.center[1] - self.p.height/2)
        elif direction == "N":
            targetcoord = (self.currentroom.coord[0],
                           self.currentroom.coord[1] - 1)
            # entrypoint at S gate
            newplayerpos = (self.currentroom.center[0] - self.p.width/2,
                            self.HEIGHT - self.p.height/2)
        elif direction == "S":
            targetcoord = (self.currentroom.coord[0],
                           self.currentroom.coord[1] + 1)
            # entrypoint at N gate
            newplayerpos = (self.currentroom.center[0] - self.p.width/2,
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
    """A room contains groups of its contents, and methods to populate itself.
    """
    # concering room contents
    WALLTHICKNESS = 20
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

        # populate room with gates and crates
        self.make_outerwalls(opengates)
        self.make_random_crate()

    def make_random_crate(self):
        """Make crate at random position.

        Get random coords, construct box, and add to group.
        """
        # params for pos
        blockminx = self.left + self.WALLTHICKNESS
        blockmaxx = self.right - self.WALLTHICKNESS - Crate.width
        blockminy = self.WALLTHICKNESS
        blockmaxy = self.gm.screenh - self.WALLTHICKNESS - Crate.height

        # generate random position
        blockx = r.randrange(blockminx, blockmaxx)
        blocky = r.randrange(blockminy, blockmaxy)

        # make the crate and add it to the room
        self.wall_c = Crate((blockx, blocky), self, self.gm)
        self.allsprites.add(self.wall_c)


    def make_outerwalls(self, opengates):
        # west wall
        nongateh = (self.height - self.GATELENGTH)/2
        wall_wtop = Wall((self.left, 0), 
                         (self.WALLTHICKNESS, nongateh), 
                         self, self.gm)
        wall_wbottom = Wall((self.left, self.GATELENGTH + nongateh),
                            (self.WALLTHICKNESS, nongateh),
                            self, self.gm)
        # east wall
        wall_etop = Wall((self.right - self.WALLTHICKNESS, 0), 
                         (self.WALLTHICKNESS, nongateh), 
                         self, self.gm)
        wall_ebottom = Wall((self.right - self.WALLTHICKNESS, self.GATELENGTH + nongateh),
                            (self.WALLTHICKNESS, nongateh),
                            self, self.gm)
        # north wall
        nongatew = (self.width - self.GATELENGTH)/2
        wall_nleft = Wall((self.left, 0), 
                         (nongatew, self.WALLTHICKNESS),
                         self, self.gm)
        wall_nright = Wall((self.right - nongatew, 0), 
                            (nongatew, self.WALLTHICKNESS),
                            self, self.gm)
        # south wall
        wall_sleft = Wall((self.left, self.height - self.WALLTHICKNESS), 
                         (nongatew, self.WALLTHICKNESS),
                         self, self.gm)
        wall_sright = Wall((self.right - nongatew, self.height - self.WALLTHICKNESS), 
                         (nongatew, self.WALLTHICKNESS),
                         self, self.gm)

        # gates
        if "W" not in opengates:
            wall_wgate = WallDestructible((self.left, nongateh), 
                                          (self.WALLTHICKNESS, self.GATELENGTH), 
                                          self, self.gm)
        if "E" not in opengates:
            wall_egate = WallDestructible((self.right - self.WALLTHICKNESS, nongateh), 
                                          (self.WALLTHICKNESS, self.GATELENGTH), 
                                          self, self.gm)
        if "N" not in opengates:
            wall_ngate = WallDestructible((self.left + nongatew, 0), 
                                          (self.GATELENGTH, self.WALLTHICKNESS),
                                          self, self.gm)
        if "S" not in opengates:
            wall_sgate = WallDestructible((self.left + nongatew, self.height - self.WALLTHICKNESS), 
                                          (self.GATELENGTH, self.WALLTHICKNESS),
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
    maxhealth = 100

    def __init__(self, pos, room, game):
        # run parent constructor
        super(Crate, self).__init__(pos, self.size, room, game)

        print("MAKING NEW CRATE @ "+ str(self.posx)+ "x" + str(self.posy))

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
            frameno = (self.animation.noofframes - 1 
                      - int(((self.animation.noofframes - 1) / self.maxhealth) * self.health))
            self.image = self.animation.get_frame_no(frameno)


    def takedamage(self, amount):
        self.health -= amount
        # kill sprite if no health
        if self.health < 1:
            self.dead = True
            self.image = self.animation.get_frame_no(self.animation.noofframes - 1)
