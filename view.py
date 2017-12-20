# viewer module
import pygame
import game

class Viewer():
    # some constants
    width = 500
    height = 500
    fps = 60

    # colors
    color_bg = (0, 0, 0)            # just black
    color_flame = (128, 0, 0)       # just red
    color_wall = (128, 128, 128)    # gray


    def __init__(self):
        # pygame display surface
        self.screen = pygame.display.set_mode((self.width, self.height))

        # lists of areas to update
        self.update_rects = []
        self.update_rects_next = []


    def render(self):
        # clear screen
        self.screen.fill(self.color_bg)

        # reset lists
        self.update_rects = []
        for rect in self.update_rects_next:
            self.update_rects.append(rect)
        self.update_rects_next = []

        # draw all sprites and get rects
        for rect in game.allsprites.draw(self.screen):
            self.update_rects.append(rect)

        self.draw_walls()
        self.draw_thrusters()

        # draw and update changed rects only
        pygame.display.update(self.update_rects)

    
    # draw player's thrusters, add rects to lists
    def draw_thrusters(self):
        for thruster in game.singleplayer.sprite.thrusters:
            pygame.draw.ellipse(self.screen, self.color_flame, thruster.rect)
            self.update_rects.append(thruster.rect)
            self.update_rects_next.append(thruster.rect)

    
    # draw current room's walls, add rects to lists
    def draw_walls(self):
        room = game.currentroom
        for wall in room.walls:
            pygame.draw.rect(self.screen, self.color_wall, wall.rect)
            self.update_rects.append(wall.rect)


# the actual viewer object
vw = Viewer()
