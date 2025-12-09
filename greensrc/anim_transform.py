import pygame as pg


def rotate_animation(frames, deg):
    # This is wrong, please don't use it, unless you know
    # that it is horribly wrong.
    return [
        pg.transform.rotate(surf, deg)
        for surf in frames
    ]
