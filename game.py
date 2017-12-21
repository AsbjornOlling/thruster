# container file for game states, rooms, main clock etc.
import pygame
import view
import events

# time vars
clock = pygame.time.Clock()
dt = 0

# global sprite groups
allsprites = pygame.sprite.RenderUpdates()
singleplayer = pygame.sprite.GroupSingle()
hardcollide = pygame.sprite.Group()

# contains a sprite group w/ walls
class Room:
    wallthickness = 20

    def __init__(self):
        # sprite groups
        self.walls = pygame.sprite.Group()

        # walls along screen edges
        self.wall_w = Wall((0, 0), (self.wallthickness, view.vw.height))
        self.wall_e = Wall((view.vw.width - self.wallthickness, 0), (self.wallthickness, view.vw.height))
        self.wall_n = Wall((0, 0), (view.vw.width, self.wallthickness))
        self.wall_s = Wall((0, view.vw.height - self.wallthickness), (view.vw.width, self.wallthickness))

        self.walls.add(self.wall_w)
        self.walls.add(self.wall_e)
        self.walls.add(self.wall_n)
        self.walls.add(self.wall_s)

        # a destructible block
        self.wall_c = WallDestructible((150, 150), (50, 50))
        self.walls.add(self.wall_c)


# dumb block, for the player to bounce off
class Wall(pygame.sprite.Sprite):
    def __init__(self, coordtuple, sizetuple):
        pygame.sprite.Sprite.__init__(self)

        # sprite groups
        allsprites.add(self)
        hardcollide.add(self)
        
        # empty image
        self.image = pygame.image.load("0.png")

        # rect using constructor args
        self.rect = pygame.Rect(coordtuple, sizetuple)


# a dumb block, that takes damage from thrusters
class WallDestructible(Wall):
    def __init__(self, coordtuple, sizetuple):
        super(WallDestructible, self).__init__(coordtuple, sizetuple)
        self.health = 100

    # run on every tick
    def update(self):
        # detect collision with player thrusters
        collisions = pygame.sprite.spritecollide(self, singleplayer.sprite.thrusters, 0)
        for thruster in collisions:
            # subtract health
            self.health -= thruster.length * dt / 1000

        # kill if no health
        if self.health < 1:
            print("Wall DEATH")
            events.evm.notify(events.ObjDeath(self.rect))
            self.kill()

# make a room (temp)
# for room testing
currentroom = Room()
