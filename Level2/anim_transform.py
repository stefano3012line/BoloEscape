import pygame as pg


def rotate_animation(animation, deg):
    # This is wrong, please don't use it, unless you know
    # that it is horribly wrong.
    animation.frames[:]=[
        pg.transform.rotate(surf, deg)
        for surf in animation.frames
    ]
