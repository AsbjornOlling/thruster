# viewer module
import pygame as pg
import events

class Viewer():
    # resolution and framerate
    width = 500
    height = 500

    # colors
    color_bg = (0, 0, 0)            # just black
    color_flame = (128, 0, 0)       # just red
    color_wall = (128, 128, 128)    # gray
    color_walldestructible = (128, 64, 64)    # orange-y

    def __init__(self, screensize, game, eventmanager):
        # display surface
        self.screen = pg.display.set_mode(screensize)

        # event listener
        self.evm = eventmanager
        self.evm.add_listener(self)

        self.gm = game

        # lists of areas to update
        self.update_rects = []
        self.update_rects_next = []

    # run on every tick
    def update(self):
        # lay background first
        self.screen.fill(self.color_bg)
        self.draw_thrusters()
        self.draw_walls()
        self.draw_sprites()

        # draw and update changed rects only
        pg.display.update(self.update_rects)

        # reset lists
        self.update_rects = []
        for rect in self.update_rects_next:
            self.update_rects.append(rect)
        self.update_rects_next = []

    # handle events
    def notify(self, event):
        # make sure to update dead wall
        if isinstance(event, events.ObjDeath):
            self.update_rects.append(event.rect)
    
    # draw sprites and get update rects
    def draw_sprites(self):
        for rect in self.gm.allsprites.draw(self.screen):
            self.update_rects.append(rect)

    # draw the walls of currentroom and get update rects
    def draw_walls(self):
        room = self.gm.currentroom
        # draw the walls
        # TODO don't do this every loop
        for wall in room.walls:
            pg.draw.rect(self.screen, self.color_wall, wall.rect)
            self.update_rects.append(wall.rect)

            # draw damange redness
            if hasattr(wall, "health"):
                reds = pg.Surface(wall.rect.size)
                reds.set_alpha(150 - wall.health)
                reds.fill((255, 0, 0))
                self.screen.blit(reds, (wall.rect.x, wall.rect.y))


    # draw player's thrusters and get update rects
    def draw_thrusters(self):
        for thruster in self.gm.singleplayer.sprite.thrusters:
            pg.draw.ellipse(self.screen, self.color_flame, thruster.rect)
            self.update_rects.append(thruster.rect)
            self.update_rects_next.append(thruster.rect)
