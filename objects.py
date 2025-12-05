import numpy as np
import pygame as game
from pygame import mixer
#from moncapiten_playground.testing_dist.gameFile import screen, ylim
from functions import *

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
        self.image = game.transform.smoothscale(game.image.load(image), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
        self.rect.topleft = self.position
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
        self.image = game.transform.smoothscale(self.image, (new, new))
    
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
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
    
    #disegna l'oggetto nel punto in cui si trova
    def draw(self, screen):
        if self.hp >0:
            screen.blit(self.image, self.position)

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


    def aura(self,pic,dim,frames, screen): #gli diamo il frame dall'esterno così posso controllarlo dentro il while frame per frame ?
        if self.hp > 0:
            im = game.image.load(pic)
            dim_array = np.linspace(self.size,dim,frames)
            self.aura_frame +=1
            if self.aura_frame >= frames:
                self.aura_frame = 0
            a = game.transform.smoothscale(im, (dim_array[self.aura_frame],dim_array[self.aura_frame]))
            screen.blit(a,self.centre -0.5*dim_array[self.aura_frame])



    #controlla se ci sono status effect in caso li applico deapplico quelli scaduti e li rimuovo dalla lista di status effect
    def update_status_effects(self,ylim,screen,draw=False):

        #disegno lo status effect se ha un immagine e una dimensione (checko solo la dimensione quind se gli dai quello e non l'immagine sono cazzi)
        n = 0
        if draw:
            for k in self.status_effects:
                if k.key != 'invincible':
                    k.draw(5 + n*k.size,ylim - k.size, screen)
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
        self.position += self.direction * self.speed/(5*np.sqrt(self.size))
        self.rect.topleft = self.position
    
    #dato che la size cambia devo cambiare anche il rettangolo altrimenti le hitbox si sfasano
    def update_mask(self):
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)

    #accellera bolognesi ogni volta che esce dallo schermo
    def accelerate(self, counter):
        self.speed += int((self.speed/(4*counter+1)))
        self.base_speed += int((self.base_speed/(4*counter+1)))  

class shooter(Character):
    def __init__(self, image, size, speed,hp, position, direction,timer,spread,possible_statuses,sound=None,volume=None):
        super().__init__(image,size,speed,hp,position,direction,sound,volume)
        self.timer= timer    #contatore (gli shooter vogliamo che despawnino indipendentemente dalla vita o meno)
        self.spread = spread #ampiezza angolare dello sparo (in gradi)
        self.possible_statuses = possible_statuses
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
           self.projectiles.append(projectile('Media/heart.png',35,40,1,working_position,k.copy(),type = [np.random.choice(self.possible_statuses)]))  # per adesso applica uno status random
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
    def draw(self,xpos,ypos, screen):
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

    def draw(self, screen):
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