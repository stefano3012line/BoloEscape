import pygame as game
from pygame import mixer
import numpy as np
import time

game.init()
mixer.init()
Bolo_passing =mixer.Sound('bolognesi-passing.mp3')
Bolo_passing.play()  # Play the sound.
game.time.delay(4000)
print('Playing sound')
