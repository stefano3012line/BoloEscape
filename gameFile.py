
import time
import os
import pygame as game
import numpy as np
import itertools as iter 
from pygame import mixer

import time
import os
import pygame as game
import numpy as np
import itertools as iter 
from pygame import mixer

from objects import *

mixer.init()

#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('Media/LEVEL 1/unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
counter = 0
score = 0
soundtrack = mixer.Sound('Media/audios/21. Loonboon IN-GAME.mp3')




#funzione che calcola se sei colpito o meno 
#attenzione il primo oggetto che si passa alla funzione è quello a cui si applica l'effetto
def hit(obj1, obj2,key=None,t=None,damage=True, both=False):
    if obj1.hp > 0 and obj2.hp > 0:
        # aggiorna rect
        obj1.rect.topleft = obj1.position
        obj2.rect.topleft = obj2.position
        #offset necessario per overlap
        #offset = (int(obj2.rect.x - obj1.rect.x), int(obj2.rect.y - obj1.rect.y))
        if obj1.mask.overlap(obj2.mask,(int(obj2.rect.x - obj1.rect.x), int(obj2.rect.y - obj1.rect.y))):
            if obj1.hittable: 
                if damage:
                    obj1.hp -= 1
                    obj1.status_effects.append(status(30,'invincible')) #di default ti rende invincibile per mezzo secondo 
                if t is not None:        #aggiunge un altro effetto se voluto
                    if key is not None:
                        for i,j in zip(t,key):
                            obj1.status_effects.append(status(i,j,image=('Media/fotoStatus/' + j + '.png'), size = 50))
                            print('bolo effettuato')
                            if both:
                                obj2.status_effects.append(status(i,j))
                    else: 
                        for i,j in zip(t,obj2.type):
                            obj1.status_effects.append(status(i,j,image=('Media/fotoStatus/' + j + '.png'), size = 50))
                            if both:
                                obj2.status_effects.append(status(i,j))


            
                        #print('fotoStatus/' + j + 'png')
            if obj2.hittable: 
                obj2.hp -= 1
            return True


#girelle
girella = Character('Media/girella.png',40,0,1,(np.random.randint(xlim-40),np.random.randint(ylim -40)), (0,0))

#oggetto player
player = Character("Media/player.png",50,20,5,[xlim/2 - 25, ylim/2 - 25], [0,0])
#player.status_effects.append(status(9000000000000, 'invincible')) #per diventare invincibile

#oggetto bolognesi
Bolognesi = Stefano("Media/LEVEL 1/bolognesi.jpeg",200,300,0,[-300,0],[0,0], sound =['Media/audios/bolognesi-passing (mp3cut.net).mp3'],volume = 0.3, spawn=0)
#Bolo_passing = mixer.Sound('audios/bolognesi-passing.mp3')
#Bolo_passing.set_volume(0.3)
#oggetto scudi
Alba = Character('Media/LEVEL 1/alba.png',90,0,0,[0,0],[0,0])
Alba_spawn_value = 10
Claudio_image = []
shield_list=[]
with os.scandir('Media/LEVEL 1/fotoClaudio') as d:
    for e in d:
        Claudio_image.append('Media/LEVEL 1/fotoClaudio/'+ e.name)
#print(image)

#oggetto rossini
Rossini = Character('Media/rossini.png',85,15,0,[0,0],[0,0])
Rossini_spawn_value= 4

#oggetto meggiolaro e lista dei proiettili
negative_stauts_list = ['confusion','slowness','enlarge'] #se si vuole randomizzare sulla scelta degli effetti si usa questa lista
Meggiolaro = shooter("Media/LEVEL 1/meggioladro.png",200,0,0,[xlim -200,ylim -200],[0,0],0,30, negative_stauts_list, sound=['Media/audios/meggio shooting.mp3'],volume=1)
Meggiolaro_spawn_value = 2



#oggetto Lamanna
Lamanna = Character('Media/LEVEL 1/lamanna.jpeg',90,0,0,[0,0],[0,0])
lamanna_spawn_value = 10

#immaginie e size cuori
heart_size = 60
heart = game.transform.smoothscale(game.image.load("Media/massimino.png"),(heart_size,heart_size))

#evento jumpscare
jumpscare=game.image.load('Media/LEVEL 1/bolo_jumpscare.jpg')
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(5,10)



#######################################################################################################################################

#lista in cui salviamo le posizioni del player serve per Rossini e servirà anche per meggiolaro e lamanna
#deve essere una lista perché il modo in cui funziona np.append appiattisce in 1D e quindi le posizioni non funzionano più
#usiamo lista e append nativo di pyton
last_n_position = []

soundtrack.play(999)
#inizializzazione gioco
game.init()
running = True
while running:
    #counter += 1/60
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    screen.blit(background,(0,0))

    #game speed
    clock.tick(30)
    
    #game event jumpscare
    if event_jumpscare == counter:
        screen.blit(jumpscare,(0,0))
        game.display.update()
        game.time.delay(300)
        #time.sleep(0.3)
        event_jumpscare+=np.random.randint(5,15)
        #counter+=1
    ###################################################################################################################
    

    ###################################################################################################################

                                                    #PLAYER#

    ###################################################################################################################
    #disegno il player

    #la funzione update_status effect li applica e rimuove in automatico perché siamo persone per bene
    player.update_status_effects(ylim, screen, draw=True)


    player.draw(screen)
    #si ridefinisce la posizione ogni frame
    player.direction = np.array([0,0])
    direction_pressed = [True,True]
    #player movement

    if not(player.confused):
        if game.key.get_pressed()[game.K_s]and player.position[1]<= ylim - (player.size + player.speed):
            player.direction[1] = 1
            direction_pressed[1] = not direction_pressed[1] 
        if game.key.get_pressed()[game.K_w]and player.position[1]>= player.speed:
            player.direction[1] = -1
            direction_pressed[1] = not direction_pressed[1]
        if game.key.get_pressed()[game.K_d] and player.position[0]<= xlim -(player.size+ player.speed):
            player.direction[0] = 1
            direction_pressed[0] = not direction_pressed[0]
        if game.key.get_pressed()[game.K_a] and player.position[0] >= player.speed:
            player.direction[0] = -1
            direction_pressed[0] = not direction_pressed[0]
        if direction_pressed[0]:
            player.direction[0] = 0
        if direction_pressed[1]:
            player.direction[1] = 0

    elif player.confused:
        if game.key.get_pressed()[game.K_w]and player.position[1]<= ylim - (player.size + player.speed):
            player.direction[1] = 1
            direction_pressed[1] = not direction_pressed[1] 
        if game.key.get_pressed()[game.K_s]and player.position[1]>= player.speed:
            player.direction[1] = -1
            direction_pressed[1] = not direction_pressed[1]
        if game.key.get_pressed()[game.K_a] and player.position[0]<= xlim -(player.size+ player.speed):
            player.direction[0] = 1
            direction_pressed[0] = not direction_pressed[0]
        if game.key.get_pressed()[game.K_d] and player.position[0] >= player.speed:
            player.direction[0] = -1
            direction_pressed[0] = not direction_pressed[0]
        if direction_pressed[0]:
            player.direction[0] = 0
        if direction_pressed[1]:
            player.direction[1] = 0


    player.update_position()

    last_n_position.append(player.position)
    if len(last_n_position) > 30:
        last_n_position = last_n_position[1:]
    
    #####################################################################################################################
    #girelle
    girella.draw(screen)
    if hit(player,girella,damage=False):
        girella.position = (np.random.randint(xlim-40),np.random.randint(ylim -40))
        girella.hp = 1 
        score +=1
    #####################################################################################################################
    
    #####################################################################################################################

                                                  #Rossini#

    #####################################################################################################################
    #aggiungo claudio Rossini
    
    if int(counter) == Rossini_spawn_value:
        Rossini_spawn_value = counter + np.random.randint(7,13) 
        Rossini.hp = 1
        #print('Rossini',counter, Rossini_spawn_value)
    if Rossini.hp == 1:
        Rossini.direction = np.sign(last_n_position[0] - Rossini.position)/np.linalg.norm(np.sign(last_n_position[0] - Rossini.position))
    if Rossini.hp == 0:
        angles = [[0,0],[0,ylim],[xlim,0],[xlim,ylim]]
        Rossini.position = np.array(angles[np.random.randint(0,4)],dtype=float) #per farlo spawnare in punti randomici #randint esclude l'upperbound
    
    Rossini.draw(screen)
    Rossini.update_position()
    
    # checko l'hit con Rossini
    hit(player,Rossini)
    #print(player.hp)
    #print(Rossini.direction)
    #####################################################################################################################

    #####################################################################################################################

                                                  #LAMANNA#

    #####################################################################################################################
    #aggiungo Lamanna
    
    '''if int(counter) == lamanna_spawn_value:
        Lamanna.position = [np.random.randint(0,xlim-Lamanna.size),np.random.randint(0,ylim - Lamanna.size)]
        lamanna_spawn_value = counter +  1 #np.random.randint(10,17)
        Lamanna.hp = 1
    if Lamanna.hp == 0:
        Lamanna.position = [0,0]
    Lamanna.draw(screen)
    Lamanna.aura('Media/LEVEL 1/heal.png',3*Lamanna.size, 35)
    heal(player,Lamanna,1)
    '''

    #####################################################################################################################
    
                                                    #ALBA#

    #####################################################################################################################
    if int(counter) == Alba_spawn_value:
        Alba.position = [np.random.randint(0,xlim-Alba.size),np.random.randint(0,ylim - Alba.size)]
        Alba_spawn_value = counter +  np.random.randint(10,17)
        Alba.hp = 1
    if Alba.hp == 0:
        Alba.position = [0,0]
    Alba.aura('Media/LEVEL 1/sun-Photoroom.png',3*Lamanna.size, 35, screen)
    Alba.draw(screen)
    
    if hit(player,Alba,damage=False):
        C1 = player.centre
        shield_list.append(shield(np.random.choice(Claudio_image),30,90,0,3,1))
        shield_list.append(shield(np.random.choice(Claudio_image),30,90,120,3,1))
        shield_list.append(shield(np.random.choice(Claudio_image),30,90,240,3,1))

    index = 0
    while len(shield_list) > index:
        shield_list[index].update_coordinates(player)
        shield_list[index].draw(screen)
        hit(shield_list[index],Bolognesi)
        hit(shield_list[index],Rossini)
        for j in Meggiolaro.projectiles:
            hit(shield_list[index],j)
        if shield_list[index].hp <= 0:
            del shield_list[index]
        else:
            index += 1

    #####################################################################################################################

                                                  #BOLOGNESI#

    #####################################################################################################################
    #Bolognesi.update_status_effects() #per ora non decommentare perché ci sono problemi se bolo viene slowato

    # check if he is off-screen → RESPAWN
    #ho tolto un due
    if outofbound(Bolognesi,xlim,ylim):
        Bolognesi.accelerate(counter)
    
        #print(Bolognesi.speed)
        counter+=1
   
    # choose new spawn side
        Bolognesi.spawn = np.random.randint(0,3)
    
    # random size
        Bolognesi.size = np.random.randint(50, 300)
        Bolognesi.update_mask()
        Bolognesi.hp = 1
        Bolognesi.soundon()

    

    # set initial spawn position
        if Bolognesi.spawn == 0:  #north
            Bolognesi.position = np.array([np.random.randint(0, xlim-Bolognesi.size), -Bolognesi.size], dtype=float)
        elif Bolognesi.spawn == 1: #south
            Bolognesi.position = np.array([np.random.randint(0, xlim-Bolognesi.size), ylim + Bolognesi.size], dtype=float)
        elif Bolognesi.spawn == 2: #east
            Bolognesi.position = np.array([xlim + Bolognesi.size,np.random.randint(0, ylim-Bolognesi.size)], dtype=float)
        elif Bolognesi.spawn == 3: #west
            Bolognesi.position = np.array([-Bolognesi.size,np.random.randint(0, ylim-Bolognesi.size)], dtype=float)

    #print("Spawn =", Bolognesi.spawn,"| Direction =", Bolognesi.direction,"| Pos =", Bolognesi.position,"| Size =", Bolognesi.size "|speed =" Bolognesi.speed)
    # move Bolognesi
    Bolognesi.update_position()
    # draw
    Bolognesi.draw(screen)
    #checking hit
    if hit(player, Bolognesi):
        Bolognesi.soundoff()
    hit(Bolognesi,Lamanna,damage = False)
    if hit(Bolognesi, Rossini):
        counter +=1
        Bolognesi.soundoff()
    ################################################################################################################################


    ################################################################################################################################
                                            
                                            #MEGGIOLARO#

    ################################################################################################################################

    if counter == Meggiolaro_spawn_value:
        Meggiolaro.hp = 1
        
    if Meggiolaro.hp == 1:
        Meggiolaro.addtimer()
        #print(Proiettili)
        #print(Meggiolaro.timer)
        if Meggiolaro.timer == 60:
            Meggiolaro.load_projectile(player.position,2)  #possiamo settare quanti proiettili spara ogni volta  in questo caso 2
            Meggiolaro.soundon()
            #print(Meggiolaro_spawn_value)
        if Meggiolaro.timer == 75:
            Meggiolaro.load_projectile(player.position,3)
            Meggiolaro.soundon()
            #print(Meggiolaro_spawn_value)
        if Meggiolaro.timer == 90:
            Meggiolaro.load_projectile(player.position,4)
            Meggiolaro.soundon()
            #print(Meggiolaro_spawn_value)
        
        #print(Proiettili) # per controllare che vengano rimossi correttamente
        if Meggiolaro.timer == 30*4: #30 è il numero di frame quindi 30*4 = 4 secondi
            Meggiolaro.hp = 0
            Meggiolaro.timer = 0
            Meggiolaro_spawn_value = counter + 15
        Meggiolaro.draw(screen)
    ################################################################################################################################
    #routine di sparo
    if len(Meggiolaro.projectiles) >0:
        for i in Meggiolaro.projectiles:
            i.update_position()
            #print(i.direction)
            i.draw(screen)
            if outofbound(i,xlim,ylim) or hit(player,i,t=[120]) or hit(Bolognesi,i,t=[30],damage= False):
                Meggiolaro.projectiles.remove(i)

    #print(Meggiolaro.projectiles) #per controllare che i proiettili vengano effettivamente rimossi come devono
    ################################################################################################################################




    if player.hp == 0:
        running=False


    
    ################################################################################################################################
    #informazioni testo
    font = game.font.SysFont('Monocraft', 40)
    text_color = (0, 0, 0)

    #blit del counter
    counter_text = font.render(f"counter: {int(counter)}", True, text_color)
    screen.blit(counter_text, (20, 20))  # posizione (x=20, y=20)
    girelle_text = font.render(f'girelle: {score}',True,text_color)
    screen.blit(girelle_text,(20,50))
    #blit degli hp
    for i in range(1,player.hp+1):
        screen.blit(heart,(xlim - i*heart_size,10))
    ################################################################################################################################


    game.display.update()
    

#end game routine
background=game.image.load('Media/LEVEL 1/death_screen.jpg')
background=game.transform.smoothscale(background,(xlim,ylim))
screen.blit(background,(0,0))
text_color = (255, 255, 255)
font = game.font.SysFont('Monocraft', 70)
girelle_text = font.render(f"girelle: {int(score)}", True, text_color)
screen.blit(girelle_text, (300, 480))

game.display.update()
mixer.stop()
game.time.delay(3000)
game.quit()



#add pause
#play audio
#adattare la size schermo

