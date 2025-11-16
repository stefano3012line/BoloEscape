import pygame as game
import numpy as np
import time

#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
score= 0

#funzione che calcola se sei colpito o meno 

def hit(obj1, obj2):
    if obj1.hp > 0 and obj2.hp > 0:
        # aggiorna rect
        obj1.rect.topleft = obj1.position
        obj2.rect.topleft = obj2.position
        #offset necessario per overlap
        #offset = (int(obj2.rect.x - obj1.rect.x), int(obj2.rect.y - obj1.rect.y))
        if obj1.mask.overlap(obj2.mask,(int(obj2.rect.x - obj1.rect.x), int(obj2.rect.y - obj1.rect.y))):
            obj1.hp -= 1
            obj2.hp -= 1
            return True
#funzione che ruopta i vettori #serve per meggiolaro

def rotate_Vector(V,phi):
    theta = np.radians(phi)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return R@V
#definizione delle classi
#########################################################################################################################################

class Character:
    def __init__(self, image, size, speed,hp, position, direction):

        # Instance variables
        self.hp = hp
        self._size = size
        self.speed = speed
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
        # Load and scale the image
        self.image = game.transform.smoothscale(game.image.load(image), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
        self.rect.topleft = self.position

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

class shooter:
    def __init__(self,image,size,hp,position,timer,spread):
        
        self.timer= timer
        self.spread = spread #ampiezza angolare dello sparo (in gradi)
        self.hp = hp
        self.size = size
        self.position = np.array(position, dtype=float)
        #se gli shooter non avranno hitbox òa roba di mask e rect non serve ma per ora la lascio
        self.image = game.transform.smoothscale(game.image.load(image), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
        self.rect.topleft = self.position
    def addtimer(self):
        if self.hp > 0:
            self.timer +=1
    '''
    def target(self,point):
        V1 = (point - self.position)/np.linalg.norm(point - self.position)
        V2 = rotate_Vector(V1,self.spread/2)
        V3 = rotate_Vector(V1,-self.spread/2)
        return V1,V2,V3
    '''
    def load_projectile(self,point):
        working_position = self.position.copy()
        V1 = (point - working_position)/np.linalg.norm(point - working_position)
        V2 = rotate_Vector(V1,self.spread/2)
        V3 = rotate_Vector(V1,-self.spread/2)
        direction = [V1,V2,V3] 
        proj = []
        for i in direction:
           proj.append(projectile('heart.png',40,20,1,working_position,i))
        return proj
    
    def draw(self):
        #Draw the character on the given screen.
        if self.hp >0:
            screen.blit(self.image, self.position)

class projectile:
    def __init__(self,image,size,speed,hp,position,direction):
        self.outofbound = False
        self.size = size
        self.speed = speed
        self.hp = hp
        self.position = position
        self.direction = direction
        self.image = game.transform.smoothscale(game.image.load(image), (size,size))
        self.rect = self.image.get_rect()
        self.mask = game.mask.from_surface(self.image)
        self.rect.topleft = self.position
    def update_position(self):
        #Move the character based on direction and speed
        if self.hp> 0:
            self.position += self.direction * self.speed
            self.rect.topleft = self.position
    def draw(self):
        #Draw the character on the given screen.
        if self.hp >0:
            screen.blit(self.image, self.position)
#funzione per sparare
########################################################################################################################################

#creazione degli oggetti
########################################################################################################################################
#oggetto player
player = Character("player.png",50,20,5,[xlim/2 - 25, ylim/2 - 25], [0,0])

#oggetto bolognesi
Bolognesi = Stefano("bolognesi.jpeg",200,300,0,[-300,0],[0,0],0)

#oggetto bonati
Bonati = Character("bonati_Claudio-Bonati.jpg",70,15,0,[0,0],[0,0])
Bonati_spawn_value= 4
#un nemico dovrebbe avere una size, delle coordinate a lui associate e un'immagine ben definita
Meggiolaro = shooter("meggioladro.png",100,0,[0,0],0,90)
Meggiolaro_spawn_value= 11
Proiettili = []
#immaginie e size cuori
heart_size = 60
heart = game.transform.smoothscale(game.image.load("massimino.png"),(heart_size,heart_size))

#evento jumpscare
jumpscare=game.image.load('bolo_jumpscare.jpg')
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(5,10)

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
    game.display.flip()
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

                                                    #PLAYER#

    ###################################################################################################################
    #disegno il player
    player.draw()
    #si ridefinisce la posizione ogni frame
    player.direction = np.array([0,0])
    direction_pressed = [True,True]
    #player movement
    if game.key.get_pressed()[game.K_s]and player.position[1]<= ylim - (player.size+player.speed):
        player.direction[1] = 1
        direction_pressed[1] = not direction_pressed[1] 
    if game.key.get_pressed()[game.K_w]and player.position[1]>= player.speed:
        player.direction[1] = -1
        direction_pressed[1] = not direction_pressed[1]
    if game.key.get_pressed()[game.K_d] and player.position[0]<= xlim -(player.size+player.speed):
        player.direction[0] = 1
        direction_pressed[0] = not direction_pressed[0]
    if game.key.get_pressed()[game.K_a] and player.position[0] >= player.speed:
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
        Bonati.direction = (last_n_position[0] - Bonati.position)/np.linalg.norm(last_n_position[0] - Bonati.position)
    if Bonati.hp == 0:
        Bonati.position = np.array([0,0],dtype=float)
    Bonati.draw()
    

    Bonati.update_position()
    
    # checko l'hit con bonati
    hit(Bonati,player)
    #print(player.hp)
    #print(Bonati.direction)
    #####################################################################################################################


    #####################################################################################################################

                                                  #BOLOGNESI#

    #####################################################################################################################

    # check if he is off-screen → RESPAWN
    #ho tolto un due
    if (Bolognesi.position[0] < -Bolognesi.size or 
        Bolognesi.position[0] > xlim + Bolognesi.size or
        Bolognesi.position[1] < -Bolognesi.size or
        Bolognesi.position[1] > ylim + Bolognesi.size):
        Bolognesi.accelerate()
        print(Bolognesi.speed)
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
    hit(Bolognesi, player)
    if hit(Bolognesi, Bonati):
        score +=1
    ################################################################################################################################


    ################################################################################################################################
                                            
                                            #MEGGIOLARO#

    ################################################################################################################################
    if score == Meggiolaro_spawn_value:
        Meggiolaro.hp = 1
        Meggiolaro_spawn_value += 40
    if Meggiolaro.hp == 1:
        Meggiolaro.addtimer()
        #print(Meggiolaro.timer)
    if Meggiolaro.timer == 60:
        Proiettili += (Meggiolaro.load_projectile(player.position))
        print(Proiettili)
    if Meggiolaro.timer == 30*4: #30 è il numero di frame quindi 30*4 = 4 secondi
        Meggiolaro.hp = 0
    Meggiolaro.draw()
    ################################################################################################################################
    if len(Proiettili) >0:
        for i in Proiettili:
            i.update_position()
            i.draw()
            hit(i,player)
            if i.hp == 0:
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


#add shooting meggio
#add pause
#play audio
#path relativi immagini
