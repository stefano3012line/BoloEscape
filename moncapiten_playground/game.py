
import time
import os
import pygame as game
import numpy as np
import itertools as iter
from pygame import mixer


from characters import *
from useful_functions import *


media_folder = os.path.join(os.getcwd(), '../')


mixer.init()
#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load(os.path.join(media_folder, 'unipipi.jpeg'))
background=game.transform.smoothscale(background,(xlim,ylim))
score= 0
soundtrack = mixer.Sound(os.path.join(media_folder, 'audios/21. Loonboon IN-GAME.mp3'))


#definizione delle classi

#########################################################################################################################################












    

########################################################################################################################################

#creazione degli oggetti
########################################################################################################################################
#lista degli status

#oggetto player
player = Character(os.path.join(media_folder, "player.png"),50,20,3,[xlim/2 - 25, ylim/2 - 25], [0,0])
#player.status_effects.append(status(9000000000000, 'invincible')) #per diventare invincibile
#player.status_effects.append(status(90,'fire'))
#oggetto bolognesi
Bolo_passing =mixer.Sound(os.path.join(media_folder, 'audios/bolognesi-passing.mp3'))
Bolo_passing.set_volume(0.3)
Bolognesi = Stefano(os.path.join(media_folder, "bolognesi.jpeg"),200,300,0,[-300,0],[0,0],0)

#oggetto bonati
Claudio_image = []
with os.scandir(os.path.join(media_folder, 'fotoClaudio')) as d:
    for e in d:
        Claudio_image.append(os.path.join(media_folder, 'fotoClaudio', e.name))
#print(image)
Bonati = Character(np.random.choice(Claudio_image),85,15,0,[0,0],[0,0])
Bonati_spawn_value= 4

#oggetto meggiolaro e lista dei proiettili
Meggiolaro = shooter(os.path.join(media_folder, "meggioladro.png"),200,0,0,[xlim -200,ylim -200],[0,0],0,30, possible_statuses = ['confusion','slowness','enlarge','fire'])
Meggiolaro_spawn_value = 2
Meggiolaro_shot_sound=mixer.Sound(os.path.join(media_folder, 'audios/meggio shooting.mp3'))
#negative_stauts_list = ['confusion','slowness','enlarge'] #se si vuole randomizzare sulla scelta degli effetti si usa questa lista
#oggetto Lamanna

Lamanna = Character(os.path.join(media_folder, "lamanna.jpeg"),90,0,0,[0,0],[0,0])
lamanna_spawn_value = 10

#immaginie e size cuori
heart_size = 60
heart = game.transform.smoothscale(game.image.load(os.path.join(media_folder, "massimino.png")),(heart_size,heart_size))

#evento jumpscare
jumpscare=game.image.load(os.path.join(media_folder, 'bolo_jumpscare.jpg'))
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(5,10)

#playing soundtrack
soundtrack.play(999)

#######################################################################################################################################

#lista in cui salviamo le posizioni del player serve per bonati e servirà anche per meggiolaro e lamanna
#deve essere una lista perché il modo in cui funziona np.append appiattisce in 1D e quindi le posizioni non funzionano più
#usiamo lista e append nativo di pyton
last_n_position = []

#inizializzazione gioco
game.init()
running = True
while running:
    #score += 1/60
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    screen.blit(background,(0,0))

    #game speed
    clock.tick(30)

    #game event jumpscare
    if event_jumpscare == score:
        screen.blit(jumpscare,(0,0))
        game.display.update()
        time.sleep(0.3)
        event_jumpscare+=np.random.randint(5,15)
        score+=1
    ###################################################################################################################
    

    ###################################################################################################################

                                                    #PLAYER#

    ###################################################################################################################
    #disegno il player

    #la funzione update_status effect li applica e rimuove in automatico perché siamo persone per bene
    player.update_status_effects(draw=True)


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

    #####################################################################################################################

                                                  #BONATI#

    #####################################################################################################################
    #aggiungo claudio bonati
    
    if int(score) == Bonati_spawn_value:
        Bonati_spawn_value = score + np.random.randint(7,13) 
        Bonati.hp = 1
    if Bonati.hp == 1:
        Bonati.direction = np.sign(last_n_position[0] - Bonati.position)/np.linalg.norm(np.sign(last_n_position[0] - Bonati.position))
    if Bonati.hp == 0:
        angles = [[0,0],[0,ylim],[xlim,0],[xlim,ylim]]
        Bonati.position = np.array(angles[np.random.randint(0,4)],dtype=float) #per farlo spawnare in punti randomici #randint esclude l'upperbound
    
    Bonati.draw(screen)
    Bonati.update_position()
    
    # checko l'hit con bonati
    hit(player,Bonati)
    #print(player.hp)
    #print(Bonati.direction)
    #####################################################################################################################

    #####################################################################################################################

                                                  #LAMANNA#

    #####################################################################################################################
    #aggiungo Lamanna
    #if int score è solo un proof of concept poi tocca fare una cosa seria per ora bonati spawna quando lo score è divisibile per 17 e despowna quando viene colpito
    if int(score) == lamanna_spawn_value:
        Lamanna.position = [np.random.randint(0,xlim-Lamanna.size),np.random.randint(0,ylim - Lamanna.size)]
        lamanna_spawn_value = score + np.random.randint(10,17)
        Lamanna.hp = 1
    if Lamanna.hp == 0:
        Lamanna.position = [0,0]
    Lamanna.draw(screen)
    Lamanna.aura(screen, os.path.join(media_folder, 'heal.png'),3*Lamanna.size, 35)
    heal(player,Lamanna,1)
    #####################################################################################################################



    #####################################################################################################################

                                                  #BOLOGNESI#

    #####################################################################################################################
    #Bolognesi.update_status_effects() #per ora non decommentare perché ci sono problemi se bolo viene slowato

    # check if he is off-screen → RESPAWN
    #ho tolto un due
    if outofbound(Bolognesi,xlim,ylim):
        Bolognesi.accelerate(score)
        Bolo_passing.play()
        #print(Bolognesi.speed)
        score+=1
   
    # choose new spawn side
        Bolognesi.spawn = np.random.randint(0,3)
    
    # random size
        Bolognesi.size = np.random.randint(50, 300)
        Bolognesi.update_mask()
        Bolognesi.hp = 1

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
    hit(player, Bolognesi)
    hit(Bolognesi,Lamanna,damage = False)
    if hit(Bolognesi, Bonati):
        score +=1
    ################################################################################################################################


    ################################################################################################################################
                                            
                                            #MEGGIOLARO#

    ################################################################################################################################

    if score == Meggiolaro_spawn_value:
        Meggiolaro.hp = 1
        
    if Meggiolaro.hp == 1:
        Meggiolaro.addtimer()

        heart_sprite = os.path.join(media_folder, "heart.png")
        #print(Proiettili)
        #print(Meggiolaro.timer)
        if Meggiolaro.timer == 60:
            Meggiolaro.load_projectile(player.position, 2, heart_sprite)  #possiamo settare quanti proiettili spara ogni volta  in questo caso 2
            Meggiolaro_shot_sound.play()
            #print(Meggiolaro_spawn_value)
        if Meggiolaro.timer == 75:
            Meggiolaro.load_projectile(player.position, 3, heart_sprite)
            Meggiolaro_shot_sound.play()
            #print(Meggiolaro_spawn_value)
        if Meggiolaro.timer == 90:
            Meggiolaro.load_projectile(player.position, 4, heart_sprite)
            Meggiolaro_shot_sound.play()
            #print(Meggiolaro_spawn_value)
        
        #print(Proiettili) # per controllare che vengano rimossi correttamente
        if Meggiolaro.timer == 30*4: #30 è il numero di frame quindi 30*4 = 4 secondi
            Meggiolaro.hp = 0
            Meggiolaro.timer = 0
            Meggiolaro_spawn_value = score + 15
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

    #blit dello score
    score_text = font.render(f"Score: {int(score)}", True, text_color)
    screen.blit(score_text, (20, 20))  # posizione (x=20, y=20)

    #blit degli hp
    for i in range(1,player.hp+1):
        screen.blit(heart,(xlim - i*heart_size,10))
    ################################################################################################################################


    game.display.update()
    

#end game routine
background=game.image.load('death_screen.jpg')
background=game.transform.smoothscale(background,(xlim,ylim))
screen.blit(background,(0,0))
text_color = (255, 255, 255)
font = game.font.SysFont('Monocraft', 70)
score_text = font.render(f"Score: {int(score)}", True, text_color)
screen.blit(score_text, (300, 480))

game.display.update()
mixer.stop()
game.time.delay(3000)
game.quit()


#add pause
#play audio
#adattare la size schermo
#add tredicucci
#rework claudio
#ADD GIRELLE