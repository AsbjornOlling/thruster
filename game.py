# GAME
# conatainer file for game states, clock etc.

import pygame
import view
import events

# time stuff
clock = pygame.time.Clock()
dt = 0

# sprite groups
allsprites = pygame.sprite.RenderUpdates()
singleplayer = pygame.sprite.GroupSingle()
hardcollide = pygame.sprite.Group()


# contains walls, enemies, pickups, etc
class Room:
    wallthickness = 20

    def __init__(self):
        # list of walls
        self.walls = pygame.sprite.Group()

        # make walls
        self.wall_w = Wall((0, 0), 
                            (self.wallthickness, view.vw.height))
        self.walls.add(self.wall_w)

        self.wall_e = Wall((view.vw.width - self.wallthickness, 0),
                            (self.wallthickness, view.vw.height))
        self.walls.add(self.wall_e)

        self.wall_n = Wall((0, 0),
                            (view.vw.width, self.wallthickness))
        self.walls.add(self.wall_n)

        self.wall_s = Wall((0, view.vw.height - self.wallthickness),
                            (view.vw.width, self.wallthickness))
        self.walls.add(self.wall_s)

        self.wall_c = WallDestructible((150, 150), (50, 50))
        self.walls.add(self.wall_c)


# just a wall sprite, for the player to bounce off
# nothing but position and size
class Wall(pygame.sprite.Sprite):
    def __init__(self, coordtuple, sizetuple):
        pygame.sprite.Sprite.__init__(self)

        # groups
        allsprites.add(self)
        hardcollide.add(self)
        
        # empty image
        self.image = pygame.image.load("0.png")

        # rect using constructor args
        self.rect = pygame.Rect(coordtuple, sizetuple)


class WallDestructible(Wall):
    def __init__(self, coordtuple, sizetuple):
        super(WallDestructible, self).__init__(coordtuple, sizetuple)
        self.health = 100


    def update(self):
        # look for collision with player thrusters
        collisions = pygame.sprite.spritecollide(self, singleplayer.sprite.thrusters, 0)
        for thruster in collisions:
            print("Wall DAMAGE")
            self.health -= thruster.length * dt / 1000

        # kill if no health
        if self.health < 1:
            print("Wall DEATH")
            events.evm.notify(events.WallDeath(self.rect))
            self.kill()


# for room testing
currentroom = Room()
