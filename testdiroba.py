import pygame as game
from pygame import mixer
import numpy as np
import time

game.init()
mixer.init()
mixer.music.load('bolognesi-passing.mp3')
mixer.music.play()

while game.mixer.music.get_busy(): 
    game.time.Clock().tick(10)
