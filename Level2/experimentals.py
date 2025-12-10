import time
import os
import pygame as game
import numpy as np
import itertools as iter 
from pygame import mixer

from andreagay import *
from classes import * 
from anim_laser import * 

mixer.init()
game.font.init()
#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
#font
font = game.font.SysFont('Monocraft', 40)
text_color = "#FFFFFF"
#background=game.image.load('Media/LEVEL 1/unipipi.jpeg')
#background=game.transform.smoothscale(background,(xlim,ylim))
background = game.Surface((xlim,ylim))
background.fill("#000708FF")
counter = 0
score = 0
soundtrack = mixer.Sound('Media/audios/21. Loonboon IN-GAME.mp3')


#girelle
girella = Character(['Media/girella.png'],40,0,1,(np.random.randint(xlim-40),np.random.randint(ylim -40)), (0,0))
#oggetto player
player = Character(["Media/player.png"],50,20,5,[xlim/2 - 25, ylim/2 - 25], [0,0])
last_n_position=[]
#player.status_effects.append(status(9000000000000, 'invincible')) #per diventare invincibile
#tredicucci
tredicucci =shooter(['Level2/Media2/tredicucci.jpg'],60,0,1,(0,0),(0,0),0,0,['andreagay'])
LASER_o_blue = AnimationLaser(xlim,25,0.2)
LASER_v_blue = AnimationLaser(ylim,25,0.2)
LASER_o_red = AnimationLaser(xlim,25,0.2,rgba_core="#F6A2A2",rgba_cutoff="#FF20209E")
LASER_v_red =  AnimationLaser(xlim,25,0.2,rgba_core="#F6A2A2",rgba_cutoff="#FF20209E")
LASER_o_green = AnimationLaser(xlim,25,0.2,rgba_core="#0EE76F",rgba_cutoff="#2FA12777")
LASER_v_green = AnimationLaser(xlim,25,0.2,rgba_core="#0EE76F",rgba_cutoff="#2FA12777")
LASER_o_gialo = AnimationLaser(xlim,25,0.2,rgba_core="#EBFB75",rgba_cutoff="#FFB70095")
LASER_v_gialo = AnimationLaser(xlim,25,0.2,rgba_core="#EBFB75",rgba_cutoff="#FFB70095")
rotate_animation(LASER_v_blue,90)
rotate_animation(LASER_v_red,90)
rotate_animation(LASER_v_green,90)
rotate_animation(LASER_v_gialo,90)
laser_o = [LASER_o_blue,LASER_o_red,LASER_o_green,LASER_o_gialo]
laser_v = [LASER_v_blue,LASER_v_red,LASER_v_green,LASER_v_gialo]
color = 0
#tomadin
tomadin = shooter(['Level2/Media2/tomadin.png'], 200,0,0,(xlim-205,ylim-205),(0,0),0,None,None)
tomadin_spawn_value = 2
#razzo
razzo = Rocket('Level2/Media2/razzo.png',(80,110),10,(0,0),(0,0),0) 

game.init()
running = True

while running:
    #counter += 1/60
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    screen.blit(background,(0,0))

#################################################  PLAYER  ########################################################
    player.update_status_effects(draw=True)
    player.draw(screen)
    #si ridefinisce la posizione ogni frame
    player.direction = np.array([0,0])
    #direction_pressed = [True,True]
    #player movement
    command(player,(xlim,ylim))
    player.update_position()
    last_n_position.append(player.position)
    if len(last_n_position) > 30:
        last_n_position = last_n_position[1:]
############################################## TREDICUCCI ###########################################################
    tredicucci.addtimer()
    if 30 <= tredicucci.timer<= 160:
        screen.blit(laser_o[color](),(0,tredicucci.centre[1]))
    if  90 <= tredicucci.timer<= 180:
        screen.blit(laser_v[color](),(tredicucci.centre[0],0))
    if tredicucci.timer == 200:
        color = np.random.choice([0,1,2,3])
        tredicucci.position=(np.random.randint(xlim), np.random.randint(ylim))
        tredicucci.timer = 0 
        counter +=1
    tredicucci.draw(screen)
##############################################  tomadin  ################################################################
    if counter == tomadin_spawn_value:
        tomadin.hp=1

    
    if tomadin.hp >=1:
        #print(tomadin.timer)
        tomadin.draw(screen)
        tomadin.addtimer()
        if tomadin.timer == 120:
            tomadin.timer = 0
            tomadin.hp = 0
            tomadin_spawn_value = counter + 20
        if tomadin.timer == 60:
            tomadin.load_rocket(rocket_sprite='Level2/Media2/razzo.png')
            #print(tomadin.rockets)

    for r in tomadin.rockets:
        r.tracking(player.centre)
        r.update_position()
        r.draw(screen)





###############################################################################################################
    #blit del counter
    counter_text = font.render(f"counter: {int(counter)}", True, text_color)
    screen.blit(counter_text, (20, 20))  # posizione (x=20, y=20)





    #game speed
    clock.tick(30)

    if player.hp == 0:
        running=False

    game.display.update()