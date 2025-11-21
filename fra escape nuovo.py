import pygame as game
import numpy as np
import time
import os
#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
score= 0

#funzione che calcola se sei colpito o meno 
#attenzione il primo oggetto che si passa alla funzione è quello a cui si applica l'effetto
def hit(obj1, obj2,key = None,t = None,damage = True):
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
                if (key is not None) and (t is not None):           #aggiunge un altro effetto se voluto
                    for i,j in zip(t,key):
                        obj1.status_effects.append(status(i,j,image=('fotoStatus/' + j + '.png'), size = 50))
                        #print('fotoStatus/' + j + 'png')
            if obj2.hittable: 
                obj2.hp -= 1
            return True
#funzione che ruopta i vettori #serve per meggiolaro

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
    def __init__(self, image, size, speed,hp, position, direction):

        # Instance variable
        self.hittable = True
        self.confused = False
        self.hp = hp
        self._size = size
        self.speed = speed
        self.base_speed = speed
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        # Load and scale the image
        self.image = game.transform.smoothscale(game.image.load(image), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
        self.rect.topleft = self.position
        #status effects
        self.status_effects = []
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, new):
        self._size = new
        self.image = game.transform.smoothscale(self.image, (new, new))
    
    @property   
    def centre(self):
        #Return the center point of the character
        return self.position + np.array([self.size / 2, self.size / 2])
    def update_position(self):
        #Move the character based on direction and speed
        if self.hp> 0:
            self.position += self.direction * self.speed
            self.rect.topleft = self.position
    def draw(self):
        #Draw the character on the given screen.
        if self.hp >0:
            screen.blit(self.image, self.position)

    def update_status_effects(self):
        #self.hittable = True
        #self.confused = False
        #self.speed = self.base_speed
        self.status_effects = [eff for eff in self.status_effects if eff.apply(self)]
        n = 1
        for k in self.status_effects:
            if k.size is not None:
                k.draw(5 + n*k.size,ylim - k.size)
                n +=1
'''
        expired = []
        for effect in self.status_effects:
            if effect.apply(self):     # returns False if expired
                expired.append(effect)

        # remove ended effects
        for e in expired:
            self.status_effects.remove(e)'''

class Stefano(Character):
    def __init__(self, image, size, speed,hp, position, direction, spawn):
        super().__init__(image,size,speed,hp,position,direction)
        self.spawn = spawn
    def update_position(self):
        #Move the character based on direction and speed
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
    def update_mask(self):
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
    def accelerate(self):
        #accellera bolognesi ogni volta che esce dallo schermo
        self.speed += int((Bolognesi.speed/(4*score+1))) 

class shooter(Character):
    def __init__(self, image, size, speed,hp, position, direction,timer,spread):
        super().__init__(image,size,speed,hp,position,direction)
        self.timer= timer
        self.spread = spread #ampiezza angolare dello sparo (in gradi)
    def addtimer(self):
        if self.hp > 0:
            self.timer +=1
    def load_projectile(self,point):
        working_position = self.position.copy() +(0,self.size/2)  #+ self.size/2 serve solo a far sparare dal punto della pistola
        V1 = (point - working_position)/np.linalg.norm(point - working_position)
        V2 = rotate_Vector(V1.copy(),self.spread/2)
        V3 = rotate_Vector(V1.copy(),-self.spread/2)
        direction = [V1,V2,V3] 
        #print(direction)
        proj = []
        for i in direction:
           proj.append(Character('heart.png',40,50,1,working_position,i.copy())) #+ self.size/2 serve solo a far sparare dal punto della pistola
        return proj

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
        self.duration -=1

        if self.duration > 0:
            return True
        if self.duration <= 0:
            obj.hittable = True
            obj.speed = obj.base_speed
            obj.confused = False
            return False
    def draw(self,xpos,ypos):
        #if self.image is not None:
        #print(self.image)
        screen.blit(self.image,(xpos,ypos))


    

########################################################################################################################################

#creazione degli oggetti
########################################################################################################################################
#lista degli status

#oggetto player
player = Character("player.png",50,20,7,[xlim/2 - 25, ylim/2 - 25], [0,0])
#player.status_effects.append(status(9000000000000, 'invincible')) #per diventare invincibile
#player.status_effects.append(status(90,'fire'))
#oggetto bolognesi
Bolognesi = Stefano("bolognesi.jpeg",200,300,0,[-300,0],[0,0],0)

#oggetto bonati
Claudio_image = []
with os.scandir('fotoClaudio') as d:
    for e in d:
        Claudio_image.append('fotoClaudio/'+ e.name)
#print(image)
Bonati = Character(np.random.choice(Claudio_image),85,10,0,[0,0],[0,0])
Bonati_spawn_value= 4

#oggetto meggiolaro e lista dei proiettili
Meggiolaro = shooter("meggioladro.png",200,0,0,[xlim -200,ylim -200],[0,0],0,30)
Meggiolaro_spawn_value= 2
Proiettili = []

#immaginie e size cuori
heart_size = 60
heart = game.transform.smoothscale(game.image.load("massimino.png"),(heart_size,heart_size))

#evento jumpscare
jumpscare=game.image.load('bolo_jumpscare.jpg')
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(5,10)

#lista status effect immage


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
    #game.display.flip()
    screen.blit(background,(0,0))

    #game speed
    clock.tick(30)
    
    #game event jumpscare
    #if event_jumpscare == score:
        #screen.blit(jumpscare,(0,0))
        #game.display.update()
        #time.sleep(0.3)
        #event_jumpscare+=np.random.randint(5,15)
        #score+=1
    ###################################################################################################################
    #effects

    ###################################################################################################################

                                                    #PLAYER#

    ###################################################################################################################
    #disegno il player
    player.update_status_effects()
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
    if len(last_n_position) > 20:
        last_n_position = last_n_position[1:]
    #####################################################################################################################

    #####################################################################################################################

                                                  #BONATI#

    #####################################################################################################################
    #aggiungo claudio bonati
    #if int score è solo un proof of concept poi tocca fare una cosa seria per ora bonati spawna quando lo score è divisibile per 17 e despowna quando viene colpito
    if int(score) == Bonati_spawn_value:
        Bonati.hp = 1
        Bonati_spawn_value = score + np.random.randint(7,13)
    if Bonati.hp ==1:
        Bonati.direction = np.sign(last_n_position[0] - Bonati.position)#/np.linalg.norm(last_n_position[0] - Bonati.position)
    if Bonati.hp == 0:
        Bonati.position = np.array([0,0],dtype=float)
    Bonati.draw()
    

    Bonati.update_position()
    
    # checko l'hit con bonati
    hit(player,Bonati)
    #print(player.hp)
    #print(Bonati.direction)
    #####################################################################################################################


    #####################################################################################################################

                                                  #BOLOGNESI#

    #####################################################################################################################

    # check if he is off-screen → RESPAWN
    #ho tolto un due
    if outofbound(Bolognesi,xlim,ylim):
        Bolognesi.accelerate()
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
    Bolognesi.draw()
    #checking hit
    hit(player, Bolognesi)
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
        #print(Proiettili)
        #print(Meggiolaro.timer)
        if Meggiolaro.timer == 60:
            Proiettili += (Meggiolaro.load_projectile(player.position))
            #print(Meggiolaro_spawn_value)
        if Meggiolaro.timer == 75:
            Proiettili += (Meggiolaro.load_projectile(player.position))
            #print(Meggiolaro_spawn_value)
        if Meggiolaro.timer == 90:
            Proiettili += (Meggiolaro.load_projectile(player.position))
            #print(Meggiolaro_spawn_value)
        #print(Proiettili)
        if Meggiolaro.timer == 30*4: #30 è il numero di frame quindi 30*4 = 4 secondi
            Meggiolaro.hp = 0
            
            Meggiolaro.timer = 0
            Meggiolaro_spawn_value = score + 15
        Meggiolaro.draw()
    ################################################################################################################################

    if len(Proiettili) >0:
        for i in Proiettili:
            i.update_position()
            #print(i.direction)
            i.draw()
            if hit(player,i,['confusion'],[120]) or outofbound(i,xlim,ylim):
                Proiettili.remove(i)
    
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
font = game.font.SysFont('Aptos', 70)
score_text = font.render(f"Score: {int(score)}", True, text_color)
screen.blit(score_text, (300, 480))

game.display.update()
time.sleep(1)
game.quit()


#add projectile types
#add pause
#play audio
#adattare la size schermo
#add tredicucci
