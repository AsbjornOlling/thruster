# viewer module
import pygame
import game
import events

class Viewer():
    # resolution and framerate
    width = 500
    height = 500
    fps = 60

    # colors
    color_bg = (0, 0, 0)            # just black
    color_flame = (128, 0, 0)       # just red
    color_wall = (128, 128, 128)    # gray

    def __init__(self):
        # display surface
        self.screen = pygame.display.set_mode((self.width, self.height))

        # event listener
        events.evm.add_listener(self)

        # lists of areas to update
        self.update_rects = []
        self.update_rects_next = []

    # run on every tick
    def update(self):
        # lay background first
        self.screen.fill(self.color_bg)
        self.draw_sprites()
        self.draw_walls()
        self.draw_thrusters()

        # draw and update changed rects only
        pygame.display.update(self.update_rects)

        # reset lists
        self.update_rects = []
        for rect in self.update_rects_next:
            self.update_rects.append(rect)
        self.update_rects_next = []

    # handle events
    def notify(self, event):
        # make sure to update dead wall
        if isinstance(event, events.WallDeath):
            self.update_rects.append(event.rect)
    
    # draw sprites and get update rects
    def draw_sprites(self):
        for rect in game.allsprites.draw(self.screen):
            self.update_rects.append(rect)

    # draw the walls of currentroom and get update rects
    def draw_walls(self):
        room = game.currentroom
        for wall in room.walls:
            pygame.draw.rect(self.screen, self.color_wall, wall.rect)
            self.update_rects.append(wall.rect)

    # draw player's thrusters and get update rects
    def draw_thrusters(self):
        for thruster in game.singleplayer.sprite.thrusters:
            pygame.draw.ellipse(self.screen, self.color_flame, thruster.rect)
            self.update_rects.append(thruster.rect)
            self.update_rects_next.append(thruster.rect)


# the actual viewer object
vw = Viewer()
