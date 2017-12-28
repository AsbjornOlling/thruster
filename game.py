# container file for game states, rooms, etc.
import pygame as pg
import player
import events

# debug
import pdb

class Game:
    marginw = 150

    def __init__(self, screensize, eventmanager):
        # eventmanager
        self.evm = eventmanager
        self.evm.add_listener(self)

        # sprite groups
        self.allsprites = pg.sprite.RenderUpdates()
        self.player = pg.sprite.GroupSingle()
        self.hardcollide = pg.sprite.Group()

        # init time, initial tick (for dt)
        self.clock = pg.time.Clock()
        self.tick()

        # screen size
        self.screenw, self.screenh = self.screensize = screensize
        # room size
        self.roomsize = self.roomw, self.roomh = (self.screenw - 2*self.marginw,
                                                  self.screenh)

    def update(self):
        self.allsprites.update()

    def notify(self, event):
        if isinstance(event, events.RoomExit):
            self.move_rooms(event.direction)

    def tick(self):
        # tick at 60fps
        self.dt = self.clock.tick(60)

    def start(self):
        # make empty 512x512 grid
        # grid uses same coord convention as screen
        dimension = 512
        self.visitedrooms = []
        for i in range(0, dimension):
            column = [None] * dimension
            self.visitedrooms.append(column)

        # make the spawn room
        self.currentroom = Room((255, 255), self)

        # make player
        self.p = player.Player(self)

    def move_rooms(self, direction):
        # get coord of the new room
        # and coord of new player position
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
                            self.screenh - self.p.height/2)
        elif direction == "S":
            targetcoord = (self.currentroom.coord[0], 
                           self.currentroom.coord[1] + 1)
            # entrypoint at N gate
            newplayerpos = (self.currentroom.center[0] - self.p.width/2,
                            0 - self.p.height/2)

        print("CUR:"+str(self.currentroom.coord))
        print("TAR:"+str(targetcoord))

        # check if new room already created
        targetroom = self.visitedrooms[targetcoord[0]][targetcoord[1]]
        if targetroom == None:
            # if not, make a new room
            newroom = Room(targetcoord, self, self.currentroom)
        else:
            newroom = self.visitedrooms[targetcoord[0]][targetcoord[1]] 

        # set the new room
        self.currentroom = newroom

        self.p.posx, self.p.posy = newplayerpos

# contains a sprite group w/ walls
class Room:
    wallthickness = 20
    gatelength = 200

    def __init__(self, coord, game, prev=None):
        # game model
        self.gm = game
        
        # set coord, and add to grid
        self.coord = coord
        game.visitedrooms[coord[0]][coord[1]] = self
        print("MAKING NEW ROOM")
        print(game.visitedrooms[coord[0]][coord[1]])

        # room dimension vars
        self.width, self.height = game.roomsize
        self.left = game.marginw
        self.right = self.left + self.width
        self.center = (self.left + self.width/2, self.height/2)

        # sprite groups
        self.walls = pg.sprite.Group()

        # make gates to previously discovered rooms open
        opengates = []
        neighbor_shift = [(-1, 0, "W"), (1, 0, "E"), 
                          (0, -1, "N"), (0, 1, "S")]
        for relpos in neighbor_shift:
            # if neighbor room exists, make that gate open
            if self.gm.visitedrooms[self.coord[0] + relpos[0]]\
                                   [self.coord[1] + relpos[1]] != None:
                opengates.append(relpos[2])

        # outer walls w/ gates
        self.make_outerwalls(opengates)

        # random destructible block
        self.wall_c = WallDestructible((self.left + self.width/3, 
                                       self.height/3), 
                                       (50, 50),
                                       self, game)

    def make_outerwalls(self, opengates):
        # west wall
        nongateh = (self.height - self.gatelength)/2
        wall_wtop = Wall((self.left, 0), 
                         (self.wallthickness, nongateh), 
                         self, self.gm)
        wall_wbottom = Wall((self.left, self.gatelength + nongateh),
                            (self.wallthickness, nongateh),
                            self, self.gm)
        # east wall
        wall_etop = Wall((self.right - self.wallthickness, 0), 
                         (self.wallthickness, nongateh), 
                         self, self.gm)
        wall_ebottom = Wall((self.right - self.wallthickness, self.gatelength + nongateh),
                            (self.wallthickness, nongateh),
                            self, self.gm)
        # north wall
        nongatew = (self.width - self.gatelength)/2
        wall_nleft = Wall((self.left, 0), 
                         (nongatew, self.wallthickness),
                         self, self.gm)
        wall_nright = Wall((self.right - nongatew, 0), 
                            (nongatew, self.wallthickness),
                            self, self.gm)
        # south wall
        wall_sleft = Wall((self.left, self.height - self.wallthickness), 
                         (nongatew, self.wallthickness),
                         self, self.gm)
        wall_sright = Wall((self.right - nongatew, self.height - self.wallthickness), 
                         (nongatew, self.wallthickness),
                         self, self.gm)

        # gates
        if "W" not in opengates:
            wall_wgate = WallDestructible((self.left, nongateh), 
                                          (self.wallthickness, self.gatelength), 
                                          self, self.gm)
        if "E" not in opengates:
            wall_egate = WallDestructible((self.right - self.wallthickness, nongateh), 
                                          (self.wallthickness, self.gatelength), 
                                          self, self.gm)
        if "N" not in opengates:
            wall_ngate = WallDestructible((self.left + nongatew, 0), 
                                          (self.gatelength, self.wallthickness),
                                          self, self.gm)
        if "S" not in opengates:
            wall_sgate = WallDestructible((self.left + nongatew, self.height - self.wallthickness), 
                                          (self.gatelength, self.wallthickness),
                                          self, self.gm)


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
