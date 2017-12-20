# GAME
# conatainer file for game states, clock etc.

import pygame
import view

# time stuff
clock = pygame.time.Clock()
dt = 0

# sprite groups
allsprites = pygame.sprite.RenderUpdates()
singleplayer = pygame.sprite.GroupSingle()
hardcollide = pygame.sprite.Group()


# contains walls, enemies, pickups, etc
class Room:
    wallthickness = 15

    def __init__(self):
        # make walls
        self.wall_w = Wall((0, 0), 
                            (self.wallthickness, view.vw.height))
        self.wall_e = Wall((view.vw.width - self.wallthickness, 0),
                            (self.wallthickness, view.vw.height))
        self.wall_n = Wall((0, 0),
                            (view.vw.width, self.wallthickness))
        self.wall_s = Wall((0, view.vw.height - self.wallthickness),
                            (view.vw.width, self.wallthickness))

        self.walls = [self.wall_w, self.wall_e, self.wall_n, self.wall_s]


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


# for room testing
currentroom = Room()
