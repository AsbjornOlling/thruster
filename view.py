# viewer module
import math
import random

import pygame as pg
import events
import animation as ani

class Viewer():
    # colors
    color_bg = (0, 0, 0)            # just black
    color_flame = (128, 0, 0)       # just red
    color_wall = (128, 128, 128)    # gray

    def __init__(self, screensize, game, eventmanager):
        self.screenw, self.screenh = self.screensize = screensize

        # display surface
        self.screen = pg.display.set_mode(screensize)

        # model obj
        self.gm = game

        # event listener
        self.evm = eventmanager
        self.evm.add_listener(self)

        # lists of areas to update
        self.update_rects = []
        self.update_rects_next = []


    # run on every tick
    def update(self):
        # lay background first
        self.screen.fill(self.color_bg)

        # draw main visible content
        self.draw_thrusters()
        self.draw_sprites()
        self.draw_walls()
        self.draw_margins()
        self.draw_fuelbar()

        # update changed rects only
        # pg.display.update(self.update_rects)
        # update all all
        pg.display.update()

        # reset lists
        self.update_rects = []
        for rect in self.update_rects_next:
            self.update_rects.append(rect)
        self.update_rects_next = []


    # handle events
    def notify(self, event):
        if isinstance(event, events.ObjDeath):
            # make sure to update dead wall
            self.update_rects.append(event.rect)
        elif isinstance(event, events.ClearScreen):
            # update entire room
            screenrect = pg.Rect((self.gm.marginw, 0),
                                 (self.gm.currentroom.width,self.screenh))
            self.update_rects.append(screenrect)
    
    # draw sprites and get update rects
    def draw_sprites(self):
        for rect in self.gm.onscreen.draw(self.screen):
            self.update_rects.append(rect)

    # draw the walls of currentroom and get update rects
    def draw_walls(self):
        room = self.gm.currentroom
        # draw the walls
        # TODO don't update rects every loop
        for wall in room.walls:
            pg.draw.rect(self.screen, self.color_wall, wall.rect)
            self.update_rects.append(wall.rect)

            # draw damange redness
            if hasattr(wall, "health"):
                # make totally red surface
                reds = pg.Surface(wall.rect.size)
                reds.fill((255, 0, 0))
                # transparancy based on health
                reds.set_alpha(256 - wall.health*1.5)
                # draw on screen
                self.screen.blit(reds, (wall.rect.x, wall.rect.y))

    # draw player's thrusters and get update rects
    def draw_thrusters(self):
        for thruster in self.gm.player.sprite.thrusters:
            pg.draw.ellipse(self.screen, self.color_flame, thruster.rect)
            self.update_rects.append(thruster.rect)
            self.update_rects_next.append(thruster.rect)


    # bits to the left and right of room-section
    def draw_margins(self):
        # left cover
        margin_L = pg.Rect((0, 0), 
                           (self.gm.marginw, self.screenh))
        pg.draw.rect(self.screen, self.color_bg, margin_L)

        # right cover
        margin_R = pg.Rect((self.gm.currentroom.right, 0), 
                           (self.gm.marginw, self.screenh))
        pg.draw.rect(self.screen, self.color_bg, margin_R)


    # draw red bar on left panel, length based on player fuel
    def draw_fuelbar(self):
        bar_height = self.screenh * 0.8
        bar_width = 20
        fuel_height = self.gm.p.fuel / self.gm.p.maxfuel * bar_height

        posx = self.gm.marginw/2 - bar_width/2
        posy = (self.screenh - bar_height)/2

        # make rect and draw bar
        fuelbar = pg.Rect((posx, posy), (bar_width, fuel_height))
        pg.draw.rect(self.screen, self.color_flame, fuelbar)

