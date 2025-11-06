import pygame as game
import numpy as np
import time


#funzione che trova i centri dei personaggi
def centro(x,y,size):
    cx = x + size/2
    cy = y + size/2
    return cx,cy
#funzione che calcola se sei colpito o meno
'''def overlap(c1,c2,s1,s2):
    
    if  np.abs(c1[0]-c2[0]) <= (s1+s2)/2 and np.abs(c1[1]-c2[1]) <= (s1+s2)/2:
        return True
    else:
        return False

def hit(x1,x2,y1,y2,size1,size2):
    c1 = centro(x1,y1,size1)
    c2 = centro(x2,y2,size2)
    return overlap(c1,c2,size1,size2)'''

def hit(obj1,obj2):
    if np.abs(obj1.x +obj1.size/2 - obj2.x +obj2.size/2) <= (obj1.size +obj2.size)/2 and np.abs(obj1.y- obj2.y +obj1.size/2 + obj2.size/2) <= (obj1.size +obj2.size)/2:
        return True
    else :
        return False
#definizione della classe dei nemici semplici e player

class character:
    def __init__(self, image, size , speed, x, y):
        # Instance variables
        self.image = game.transform.smoothscale(game.image.load(image), (size,size))
        self.size = size
        self.speed = speed
        self.x = x
        self.y = y
        self.centre = centro(x,y,size)
    def updatecentre(self,x,y):
        self.centre = centro(x,y,self.size)
        return
class bolognesi(character):
    def __init__(self, image, size , speed, x, y,dir):
        super().__init__(image,size,speed,x,y)
        self.dir= dir
        self.accel = speed/5
#inizializzazione gioco
game.init()
running = True
#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
score=0

#evento jumpscare
jumpscare=game.image.load('bolo_jumpscare.jpg')
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(5,10)

#oggetto player
player = character("player.png",50,20,xlim/2 - 25, ylim/2 - 25)
#oggetto bolognesi
Bolognesi = bolognesi("bolognesi.jpeg",200,200,np.random.randint(200,xlim-200),400,1)
#oggetto bonati
Claudio = character("bonati_Claudio-Bonati.jpg",70,5,0,0)
#un nemico dovrebbe avere una size, delle coordinate a lui associate e un'immagine ben definita

#info bolognesi
#B_size =200
#B_x= np.random.randint(B_size,xlim-B_size)
#B_y= - 2*B_size
#B_dir= 1
#B_speed=200
#B_accell=B_speed/5
#Bolognesi=game.image.load("bolognesi.jpeg")
#Bolognesi=game.transform.smoothscale(Bolognesi,(B_size,B_size))

#roba per fare bonati
#Cla_size=70
#Cla_speed=5
#Cla_x=0
#Cla_y=0
#Claudio=game.image.load("bonati_Claudio-Bonati.jpg")
#Claudio=game.transform.smoothscale(Claudio,(Cla_size,Cla_size))
#array posizioni del players
last_n_Xposition = np.array([])
last_n_Yposition = np.array([])
#tetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculotetteculo
while running:

    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    game.display.flip()
    screen.blit(background,(0,0))



    #game speed
    clock.tick(60)


#andrea devi esplodereeeeee

    #game event jumpscare
    if event_jumpscare == score:
        screen.blit(jumpscare,(0,0))
        game.display.update()
        time.sleep(0.3)
        event_jumpscare+=np.random.randint(5,15)
        score+=1

    #player movement
    if  game.key.get_pressed()[game.K_s]and player.y <= ylim - (player.size+player.speed):
        player.y+=player.speed
    if  game.key.get_pressed()[game.K_w]and player.y >= player.speed:
        player.y-=player.speed
    if  game.key.get_pressed()[game.K_d] and player.x <= xlim -(player.size+player.speed):
        player.x+=player.speed
    if  game.key.get_pressed()[game.K_a] and player.x >= player.speed:
        player.x-=player.speed


    #claudio movement
    last_n_Xposition=np.append(last_n_Xposition,player.x)
    last_n_Yposition=np.append(last_n_Yposition,player.y)
    if len(last_n_Xposition) > 24:
        last_n_Xposition=last_n_Xposition[1:]
        last_n_Yposition=last_n_Yposition[1:]
        #print(last_n_Xposition)
    Cla_Xdir= np.sign(-Claudio.x + last_n_Xposition[-1])
    Cla_Ydir= np.sign(-Claudio.y + last_n_Yposition[-1])
    if score >5:
        screen.blit(Claudio.image,(Claudio.x,Claudio.y))
        Claudio.x+=Claudio.speed*Cla_Xdir
        Claudio.y+=Claudio.speed*Cla_Ydir


    #player character
    #game.draw.circle(screen,'black',(x,y),size)

    screen.blit(player.image,(player.x,player.y))



    #Bolognesi movement
    if Bolognesi.dir == 0:#from north
        if Bolognesi.y>= -(2*Bolognesi.size) and Bolognesi.y<=ylim+(Bolognesi.size*2):
            screen.blit(Bolognesi.image,(Bolognesi.x,Bolognesi.y))
            Bolognesi.y+=Bolognesi.speed/(5*np.sqrt(Bolognesi.size))


    elif Bolognesi.dir == 1:#from south
        if Bolognesi.y>= -(2*Bolognesi.size) and Bolognesi.y<=ylim+(Bolognesi.size*2):
            screen.blit(Bolognesi.image,(Bolognesi.x,Bolognesi.y))
            Bolognesi.y -= Bolognesi.speed/(5*np.sqrt(Bolognesi.size))


    elif Bolognesi.dir == 2:#from est
        if Bolognesi.x>= -(2*Bolognesi.size) and Bolognesi.x<=xlim+(2*Bolognesi.size):
            screen.blit(Bolognesi.image,(Bolognesi.x,Bolognesi.y))
            Bolognesi.x -= Bolognesi.speed/(5*np.sqrt(Bolognesi.size))



    elif Bolognesi.dir == 3:#from west
        if Bolognesi.x>= -(2*Bolognesi.size) and Bolognesi.x<=xlim+(2*Bolognesi.size):
            screen.blit(Bolognesi.image,(Bolognesi.x,Bolognesi.y))
            Bolognesi.x += Bolognesi.speed/(5*np.sqrt(Bolognesi.size))


        #giving random dir
    if Bolognesi.y< -(2*Bolognesi.size) or Bolognesi.y>ylim+(Bolognesi.size*2) or Bolognesi.x< -(2*Bolognesi.size) or Bolognesi.x>xlim+(Bolognesi.size*2) :
        Bolognesi.dir = np.random.randint(0,4)
        Bolognesi.size = np.random.randint(10,500)
        Bolognesi.accel=int((Bolognesi.speed/(3.5*score+1)))+1
        score+=1
        print(score,Bolognesi.speed)



#spawn for different directions size and speed
        if Bolognesi.dir == 0:#from north
           # B_size=np.random.randint(size,3*size)
            Bolognesi.x= np.random.randint(0,xlim-Bolognesi.size)
            Bolognesi.y= -(2*Bolognesi.size)
            Bolognesi.speed+= Bolognesi.accel
        elif Bolognesi.dir == 2:#from est
           # B_size=np.random.randint(size,3*size)
            Bolognesi.y= np.random.randint(0,ylim-Bolognesi.size)
            Bolognesi.x= xlim+(2*Bolognesi.size)
            Bolognesi.speed+= Bolognesi.accel
        elif Bolognesi.dir == 1:#from south
           # B_size=np.random.randint(size,3*size)
            Bolognesi.x= np.random.randint(0,xlim-Bolognesi.size)
            Bolognesi.y= ylim +(2*Bolognesi.size)
            Bolognesi.speed+= Bolognesi.accel
        elif Bolognesi.dir == 3:#from west
           # B_size=np.random.randint(size,3*size)
            Bolognesi.y= np.random.randint(0,ylim-Bolognesi.size)
            Bolognesi.x= -(2*Bolognesi.size)
            Bolognesi.speed+= Bolognesi.accel
    #Bolognesi=game.transform.smoothscale(Bolognesi,(Bolognesi.size,Bolognesi.size)) 

    #getting hit
    if  hit(player, Bolognesi) == True or hit(player, Claudio) == True:
        player.size = player.size/2
        Bolognesi.y = ylim +1000

    if player.size <= 20 or player.size>=100:
        running=False

    # Font per il punteggio
    font = game.font.SysFont('Arial', 40)
    text_color = (0, 0, 0)

    # Mostra il punteggio a schermo
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (20, 20))  # posizione (x=20, y=20)

    game.display.update()
    

#end game routine
background=game.image.load('death_screen.jpg')
background=game.transform.smoothscale(background,(xlim,ylim))
screen.blit(background,(0,0))
text_color = (255, 255, 255)
font = game.font.SysFont('Aptos', 70)
score_text = font.render(f"Score: {score}", True, text_color)
screen.blit(score_text, (300, 480))

game.display.update()
time.sleep(5)
game.quit()


#add shooting meggio
#add pause
#play audio
#path relativi immagini
