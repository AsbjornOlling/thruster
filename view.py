# viewer module
import math
import random

import pygame as pg
import events
import animation as ani
import colors

class Viewer():
    # colors
    # main game screen
    color_bg = colors.get_rgb(colors.wb7)
    color_wall = colors.get_rgb(colors.wb6)    # gray
    color_flame = colors.get_rgb(colors.pp3)
    # hud ui
    color_margin = colors.get_rgb(colors.by3)
    color_dial = colors.get_rgb(colors.gb4)

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

        # bool to control only updating margins once
        self.margins_updated = False


    # run on every tick
    def update(self):
        # lay background first
        self.screen.fill(self.color_bg)

        # draw main visible content
        self.draw_thrusters()
        self.draw_sprites()
        self.draw_walls()
        self.draw_margins()

        # update changed rects only
        pg.display.update(self.update_rects)
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
        pg.draw.rect(self.screen, self.color_margin, margin_L)

        # right cover
        margin_R = pg.Rect((self.gm.currentroom.right, 0), 
                           (self.gm.marginw, self.screenh))
        pg.draw.rect(self.screen, self.color_margin, margin_R)

        # add margins to update list
        # only on first run
        if not self.margins_updated:
            self.update_rects.append(margin_R)
            self.update_rects_next.append(margin_R)
            self.update_rects.append(margin_L)
            self.update_rects_next.append(margin_L)
            self.margins_updated = True

        # draw fuel bar on left margin
        self.draw_fuelbar()
        # speed information on right margin
        self.draw_velocitypanel()


    # draw red bar on left panel, length based on player fuel
    def draw_fuelbar(self):
        bar_height = self.screenh * 0.5
        bar_width = 40
        fuel_height = self.gm.p.fuel / self.gm.p.maxfuel * bar_height

        fuelposx = self.gm.marginw/2 - bar_width/2
        fuelposy = (self.screenh - bar_height)/2 + (bar_height - fuel_height)

        # make rect and draw bar
        fuel = pg.Rect((fuelposx, fuelposy), (bar_width, fuel_height))
        pg.draw.rect(self.screen, self.color_flame, fuel)

        barposx = fuelposx
        barposy = (self.screenh - bar_height)/2 

        # add the entire fuelbar to update rects
        bar = pg.Rect((barposx, barposy), (bar_width, bar_height))
        self.update_rects.append(bar)
        self.update_rects_next.append(bar)


    def draw_velocitypanel(self):
        # angle-meter
        posx = (self.gm.marginw 
                + self.gm.currentroom.width 
                + self.gm.marginw//2)
        posy = self.screenh//3
        radius = 48
        pg.draw.circle(self.screen, self.color_dial, (posx, posy), radius)

        # speed vector length
