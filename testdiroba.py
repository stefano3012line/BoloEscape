import pygame as game
from pygame import mixer
import numpy as np
import time

game.init()
mixer.init()
Bolo_passing =mixer.Sound('bolognesi-passing.mp3')


while True:
    inpt = input('Press enter to play the sound: ')
    Bolo_passing.play()  # Play the sound.
    print('Playing sound')
