
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

#fuznione che ti cura quando hitti un oggetto # il primo oggetto è il destinatario dell'healing
def heal(obj1,obj2,n):
    if obj1.hp > 0 and obj2.hp > 0: #per l'healing non serve in effetti
        # aggiorna rect
        obj1.rect.topleft = obj1.position
        obj2.rect.topleft = obj2.position
        #offset necessario per overlap
        #offset = (int(obj2.rect.x - obj1.rect.x), int(obj2.rect.y - obj1.rect.y))
        if obj1.mask.overlap(obj2.mask,(int(obj2.rect.x - obj1.rect.x), int(obj2.rect.y - obj1.rect.y))):
            obj1.hp += n
            obj2.hp -= 1
            return True
                

#funzione che ruota i vettori #serve per meggiolaro

def rotate_Vector(V,phi):
    theta = phi*np.pi/180
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return R@V
#funzione che calcola se un oggetto è out of bound
def outofbound(obj,x,y):
    if (obj.position[0] < -obj.size or 
       obj.position[0] > x + obj.size or
        obj.position[1] < -obj.size or
        obj.position[1] > y + obj.size):
        return True
#definizione delle classi

#########################################################################################################################################

class Character:
    def __init__(self, image, size, speed,hp, position, direction, sound = None,volume= None, aura_frame = 0):

        #instance variable
        self.hp = hp
        self._size = size
        self.base_size = size
        self.speed = speed
        self.base_speed = speed
        #movement variables
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        #status variables
        self.status_effects =[]
        self.hittable = True
        self.confused = False
        # Load and scale the image and mask it
        self.image = [game.transform.smoothscale(game.image.load(im), (self.size, self.size)) for im in image]
        #self.rect = [im.get_rect() for im in self.image ]
        self.rect = self.image[0].get_rect()
        #self.mask = [game.mask.from_surface(im) for im in self.image]
        
        self.rect.topleft = self.position
        self.mask = game.mask.from_surface(self.image[0])
        #sound variables
        if sound is not None:
            self.sound = [ mixer.Sound(s) for s in sound ]
        self.volume = volume 
        #frame per aura effects
        self.aura_frame = aura_frame
                                 ######### definzione dei metodi ##########

    #riaggiornare la size dentro il dizionario per ridefinire anche mask e rettangolo in automatico
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, new):
        self._size = new
        self.image = [game.transform.smoothscale(im, (new, new)) for im in self.image]
    
    #centro dell'oggetto (usato in passato per calcolare le hitbox ma ora non serve più)
    @property   
    def centre(self):
        #Return the center point of the character
        return self.position + np.array([self.size / 2, self.size / 2])
    
    #usata per muovere l'oggetto (non so perché non l'ho semplicemente chiamato move)
    def update_position(self):
        if self.hp> 0: #controllo che l'hp dell'oggetto sia maggiore di zero se no si ferma (boh non so se è necessario ci sta un botto di double check in sto codice)
            self.position += self.direction * self.speed
            self.rect.topleft = self.position
    #per updatare la maskera quando l'effetto enlarge ti cambia size
    def update_mask(self):
        self.rect = self.image[0].get_rect()
        self.mask = game.mask.from_surface(self.image[0])
    
    #disegna l'oggetto nel punto in cui si trova
    def draw(self, n=None):
        if n is not None:
            i = n
        else: 
            i = 0
        if self.hp >0:
            screen.blit(self.image[i], self.position)

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


    def aura(self,pic,dim,frames): #gli diamo il frame dall'esterno così posso controllarlo dentro il while frame per frame ?
        if self.hp > 0:
            im = game.image.load(pic)
            dim_array = np.linspace(self.size,dim,frames)
            self.aura_frame +=1
            if self.aura_frame >= frames:
                self.aura_frame = 0
            a = game.transform.smoothscale(im, (dim_array[self.aura_frame],dim_array[self.aura_frame]))
            screen.blit(a,self.centre -0.5*dim_array[self.aura_frame])



    #controlla se ci sono status effect in caso li applico deapplico quelli scaduti e li rimuovo dalla lista di status effect
    def update_status_effects(self,draw=False):

        #disegno lo status effect se ha un immagine e una dimensione (checko solo la dimensione quind se gli dai quello e non l'immagine sono cazzi)
        n = 0
        if draw:
            for k in self.status_effects:
                if k.key != 'invincible':
                    k.draw(5 + n*k.size,ylim - k.size)
                    n +=1
        
        #per questioni di come pyton conta gli indici tocca creare una tabella temporanea per gli effetti scaduti
        expired = []
        for eff in self.status_effects:
            if not(eff.apply(self)): #applico gli effetti quando controllo se sono scaduti    # returns False if expired
                expired.append(eff)
                #print(eff)

        # remove ended effects
        for e in expired:
            e.deapply(self)  #deapplico gli effetti scaduti
            self.status_effects.remove(e)  #rimuovo gli effetti scaduti dalla lista di effetti

class Stefano(Character):
    def __init__(self, image, size, speed,hp, position, direction,spawn,sound=None, volume=None):
        super().__init__(image,size,speed,hp,position,direction,sound,volume)
        self.spawn = spawn
    def update_position(self):
        #Move the character based on direction and speed
        #non controllo se sia vivo o meno perché per farlo spawnare ho bisogno che bolo esca dallo schermo quindi in reltà continua a muoversi anche da morto
        #il motivo è che così in automatico dopo che ti colpisce hai un attimo di pausa prima che un altro bolognesi spawni (il tempo che quello vecchio esca dallo schermo)
        if self.spawn == 0: #north
            self.direction = np.array([0, 1], dtype=float)
        elif self.spawn == 1: #south
            self.direction = np.array([0, -1], dtype=float)
        elif self.spawn == 2: #east
            self.direction = np.array([-1, 0], dtype=float)
        elif self.spawn == 3: #west
            self.direction = np.array([1, 0], dtype=float)
        self.position += self.direction * self.speed/(5*np.sqrt(Bolognesi.size))
        self.rect.topleft = self.position

    #accellera bolognesi ogni volta che esce dallo schermo
    def accelerate(self):
        self.speed += int((Bolognesi.speed/(4*counter+1)))
        self.base_speed += int((Bolognesi.base_speed/(4*counter+1)))  

class shooter(Character):
    def __init__(self, image, size, speed,hp, position, direction,timer,spread,sound=None,volume=None):
        super().__init__(image,size,speed,hp,position,direction,sound,volume)
        self.timer= timer    #contatore (gli shooter vogliamo che despawnino indipendentemente dalla vita o meno)
        self.spread = spread #ampiezza angolare dello sparo (in gradi)
        self.projectiles =[]
    def addtimer(self):
        if self.hp > 0:
            self.timer +=1
    #funzione per caricare i proiettili in una lista
    def load_projectile(self,point,n): #n è il numero di proiettili da sparare dentro lo spread
        working_position = self.position.copy() +(0,self.size/2)  #+ self.size/2 serve solo a far sparare dal punto della pistola 
                                                                  #(potrei sostituirla con il centro o renderlo un parametro esterno per generalizzarlo ad altri personaggi)
        V1 = (point - working_position)/np.linalg.norm(point - working_position)
        directions =[]
        for i in np.linspace(-self.spread/2,self.spread/2,n):
            directions.append(rotate_Vector(V1.copy(),i))
        #print(direction)
        for k in directions:
           self.projectiles.append(projectile(['Media/heart.png'],35,40,1,working_position,k.copy(),type = [np.random.choice(negative_stauts_list)]))  # per adesso applica uno status random
        #return proj #ho effettivamente bisogno di returnarla? no potrebbe essere un array contenuto nella classe e avrebbe più senso

#classe dei proiettili che hanno un tipo e presumibilmente altre cose in futuro
class projectile(Character):
    def __init__(self, image, size, speed,hp, position, direction,  sound=None, volume=None,type=None):
        super().__init__(image,size,speed,hp,position,direction,sound,volume)
        self.type = type

class status:
    def __init__(self,duration,key,image = None ,size =None):
        self.duration = duration
        self.size = size
        if image is not None:
            self.image = game.transform.smoothscale(game.image.load(image), (self.size, self.size))
        else: 
            self.image = None
        self.key = key
    def apply(self,obj):
        if self.key == 'fire':
            if self.duration %30 == 0:
                obj.hp -= 1
        elif self.key == 'slowness':
            obj.speed = obj.base_speed/2
        elif self.key == 'invincible':
            obj.hittable = False
        elif self.key == 'confusion':
            obj.confused = True
        elif self.key == 'enlarge':
            obj.size = 3*obj.base_size
            obj.update_mask()
        self.duration -=1 

        return self.duration > 0 #True se è in vigore 
    def deapply(self,obj):

        if self.key == 'slowness':
            obj.speed = obj.base_speed
        elif self.key == 'invincible':
            obj.hittable = True
        elif self.key == 'confusion':
            obj.confused = False
        elif self.key == 'enlarge':
            obj.size = obj.base_size
            obj.update_mask()
        return False #serve per la list comprension
    def draw(self,xpos,ypos):
        #if self.image is not None:
        #print(self.image)
        screen.blit(self.image,(xpos,ypos))

class shield:
    def __init__(self,image,size,radius,angle,angular_velocity,hp,sound=None, volume=None):
        self.hittable = True
        self.size = size 
        self.radius = radius 
        self.angle = angle 
        self.position = np.array([0,0])
        self.angular_velocity = angular_velocity
        self.hp = hp
        self.status_effects=[]
        # Load and scale the image and mask it
        self.image = game.transform.smoothscale(game.image.load(image), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
        self.rect.topleft = self.position
        #sound variables
        if sound is not None:
            self.sound = [ mixer.Sound(s) for s in sound ]
        self.volume = volume 

    def update_coordinates(self,obj):
        self.angle = (self.angle + self.angular_velocity)%360
        r = np.array([0,1])
        r = rotate_Vector(r,self.angle)
        self.position = obj.centre + r*self.radius

    def draw(self):
        if self.hp >0:
            screen.blit(self.image,self.position - self.size/2)

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

    

########################################################################################################################################

#creazione degli oggetti
########################################################################################################################################
#lista degli status
#girelle
girella = Character(['Media/girella.png'],40,0,1,(np.random.randint(xlim-40),np.random.randint(ylim -40)), (0,0))

#oggetto player
player = Character(["Media/player.png"],50,20,5,[xlim/2 - 25, ylim/2 - 25], [0,0])
#player.status_effects.append(status(9000000000000, 'invincible')) #per diventare invincibile

#oggetto bolognesi
Bolognesi = Stefano(["Media/LEVEL 1/bolognesi.jpeg"],200,300,0,[-300,0],[0,0], sound =['Media/audios/bolognesi-passing (mp3cut.net).mp3'],volume = 0.3, spawn=0)
#Bolo_passing = mixer.Sound('audios/bolognesi-passing.mp3')
#Bolo_passing.set_volume(0.3)
#oggetto scudi
Alba = Character(['Media/LEVEL 1/alba.png'],90,0,0,[0,0],[0,0])
Alba_spawn_value = 10
Claudio_image = []
shield_list=[]
with os.scandir('Media/LEVEL 1/fotoClaudio') as d:
    for e in d:
        Claudio_image.append('Media/LEVEL 1/fotoClaudio/'+ e.name)
#print(image)

#oggetto rossini
Rossini_image = []
with os.scandir('Media/LEVEL 1/hand_rub/frames') as d:
    for e in d:
        Rossini_image.append('Media/LEVEL 1/hand_rub/frames/'+ e.name)
Rossini = Character(Rossini_image,85,15,0,[0,0],[0,0])
Rossini_spawn_value = 4
Rossini_frame = 0
#oggetto meggiolaro e lista dei proiettili
Meggiolaro = shooter(["Media/LEVEL 1/meggioladro.png"],200,0,0,[xlim -200,ylim -200],[0,0],0,30, sound=['Media/audios/meggio shooting.mp3'],volume=1)
Meggiolaro_spawn_value = 2
negative_stauts_list = ['confusion','slowness','enlarge'] #se si vuole randomizzare sulla scelta degli effetti si usa questa lista


#oggetto Lamanna
Lamanna = Character(['Media/LEVEL 1/lamanna.jpeg'],90,0,0,[0,0],[0,0])
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
    player.update_status_effects(draw=True)


    player.draw()
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
    girella.draw()
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
        Rossini_frame += 0.5
        Rossini_frame %= len(Rossini_image)
        Rossini.direction = np.sign(last_n_position[0] - Rossini.position)/np.linalg.norm(np.sign(last_n_position[0] - Rossini.position))
    if Rossini.hp == 0:
        Rossini_frame = 0
        angles = [[0,0],[0,ylim],[xlim,0],[xlim,ylim]]
        Rossini.position = np.array(angles[np.random.randint(0,4)],dtype=float) #per farlo spawnare in punti randomici #randint esclude l'upperbound
    
    Rossini.draw(int(Rossini_frame))
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
    Lamanna.draw()
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
    Alba.aura('Media/LEVEL 1/sun-Photoroom.png',3*Lamanna.size, 35)
    Alba.draw()
    
    if hit(player,Alba,damage=False):
        C1 = player.centre
        shield_list.append(shield(np.random.choice(Claudio_image),30,90,0,3,1))
        shield_list.append(shield(np.random.choice(Claudio_image),30,90,120,3,1))
        shield_list.append(shield(np.random.choice(Claudio_image),30,90,240,3,1))

    index = 0
    while len(shield_list) > index:
        shield_list[index].update_coordinates(player)
        shield_list[index].draw()
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
        Bolognesi.accelerate()
    
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
    Bolognesi.draw()
    #checking hit
    if hit(player, Bolognesi):
        Bolognesi.soundoff()
    #hit(Bolognesi,Lamanna,damage = False)
    if hit(Bolognesi, Rossini):
        counter +=1
        Bolognesi.soundoff()
    
    hit(Bolognesi,Alba,damage=False)
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
        Meggiolaro.draw()
    ################################################################################################################################
    #routine di sparo
    if len(Meggiolaro.projectiles) >0:
        for i in Meggiolaro.projectiles:
            i.update_position()
            #print(i.direction)
            i.draw()
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


#schermo adattivo
#add pause
#play audio
#adattare la size schermo

