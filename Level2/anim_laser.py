from dataclasses import dataclass
import pygame as pg
from math import cos
from anim_transform import *
import numpy as np 
from pygame import mixer
class AnimationLaser:
    FPS = 30

    def __init__(self, width, height, pulse, rgba_core="#ccffffff", rgba_cutoff="#0099ee22"):
        # Geometry
        self.width = width
        self.height = height
        self.pulse = pulse
        # Colors
        self.rgba_core = rgba_core
        self.rgba_cutoff = rgba_cutoff
        # State
        self.counter = 0
        self.frames = [
            self.mkframe(height*(0.4 * cos(i) + 1.6)/2)
            for i in range(self.FPS)
        ]

    def __call__(self):
        # Fetch frame
        out = self.frames[int(self.counter)]
        # Push counter
        self.counter += self.pulse
        self.counter %= self.FPS
        return out

    def mkframe(self, dh):
        # Drawing pixels to be smoothed
        kernel = pg.Surface((5, 3), pg.SRCALPHA)
        pg.draw.rect(kernel, self.rgba_cutoff, (0, 0, 5, 3))
        pg.draw.rect(kernel, self.rgba_core, (0, 1, 5, 1))
        # Smoothing buffer
        surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
        surf.blit(
            # Smoothing via smoothscale interpolation
            pg.transform.smoothscale(kernel, (self.width, dh)),
            # Re-centering animation around the laser core
            (0, (self.height - dh) / 2)
        )
        return surf
class Animation_explosion:
    def __init__(self,img,scale,sound=None, volume=1):
        self.img = [pg.transform.scale_by(pg.image.load(im),scale) for im in img]
        self.i_frame = 0
        self.run=False
        if sound is not None:
            self.sound = [ mixer.Sound(s) for s in sound ]
        self.volume = volume 
    def draw(self,screen,c,duration): #duration frames
            if self.run==True:
                exp_rect = self.img[np.int(self.i_frame)].get_rect(center = c)
                #draw image
                screen.blit(self.img[np.int(self.i_frame)], exp_rect)
                self.i_frame += len(self.img)/duration
                if np.int(self.i_frame) == len(self.img):
                    self.run=False
                    self.i_frame=0
            
    def soundon(self,n = 0): #suona l'ennesima track
            if self.sound is not None:
                if type(self.volume) is list:
                    v = self.volume[n]
                else:
                    v = self.volume
                self.sound[n].set_volume(v)
            self.sound[n].play()
    def soundoff(self,n=0):
            if self.hp<=0:
                self.sound[n].stop()

def rotate_animation(animation, deg):
    # This is wrong, please don't use it, unless you know
    # that it is horribly wrong.
    animation.frames[:]=[
        pg.transform.rotate(surf, deg)
        for surf in animation.frames
    ]
if __name__ == "__main__":
    # Demo
    pg.init()
    screen = pg.display.set_mode((800, 600))
    laser = AnimationLaser(500, 40, 0.005)

    laser.frames = rotate_animation(laser.frames, 90)
    while True:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
        screen.fill("#000000")
        screen.blit(laser(), (200, 340))
        pg.display.update()
