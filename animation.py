import os
import pygame as pg

# for animation objects
class Animation:

    def __init__(self, spritesheet, offset):
        # load image from assets folder
        self.spritesheet = pg.image.load(os.path.join("assets", spritesheet)).convert_alpha()

        # get args
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.offset = offset
        self.framesize = (self.width, self.offset)
        self.noofframes = self.height / self.offset

        # reset frame counter
        self.reset()


    def reset(self):
        self.frameno = 0


    def step_forward(self):
        self.frame = self.get_frame_no(self.frameno)
        self.frameno += 1

        if self.frameno > self.noofframes - 1:
            self.reset()

        return self.frame


    def get_frame_no(self, no):
        # crop image by blitting onto smaller surface
        frame = pg.Surface((self.width, self.offset)).convert_alpha()
        
        area = pg.Rect((0, no * self.offset), (self.width, self.offset))
        frame.blit(self.spritesheet, (0, 0), area)

        frame.blit(self.spritesheet, (0, no * -1 * self.offset), area)
        # print("FRAME: "+str(no))
        # print("COORD: "+str(area.y))
        return frame
