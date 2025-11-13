import pygame as game
import numpy as np
import time

#funzione che calcola se sei colpito o meno
'''def overlap(c1,c2,s1,s2):
    
    if  np.abs(c1[0]-c2[0]) <= (s1+s2)/2 and np.abs(c1[1]-c2[1]) <= (s1+s2)/2:
        return True
    else:
        return False

def hit(x1,x2,y1,y2,size1,size2):
    c1 = centro(x1,y1,size1)
    c2 = centro(x2,y2,size2)
    return overlap(c1,c2,size1,size2)

def hit(obj1,obj2):
    if np.abs(obj1.x +obj1.size/2 - obj2.x +obj2.size/2) <= (obj1.size +obj2.size)/2 and np.abs(obj1.y- obj2.y +obj1.size/2 + obj2.size/2) <= (obj1.size +obj2.size)/2:
        return True
    else :
        return False'''

#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
score=0

#definizione della classe dei nemici semplici e player
#porca puttana andrea vaffanculo cerchiamo di farlo bene sta volta

#qualsiasi personaggio avràun immagine una taglia una velocità un vetore posizione e un vettore direzione
#attenzione 

#dare posizione e direzioni come tuple
class Character:
    def __init__(self, image, size, speed, position, direction):
        # Load and scale the image
        self.image = game.transform.smoothscale(game.image.load(image), (size, size))
        
        # Instance variables
        self.size = size
        self.speed = speed
        self.position = np.array(position, dtype=float)   # [x, y]
        self.direction = np.array(direction, dtype=float) # [dx, dy]
        
    def centre(self):
        #Return the center point of the character.
        return self.position + np.array([self.size / 2, self.size / 2])

    def update_position(self):
        #Move the character based on direction and speed.
        self.position += self.direction * self.speed

    def draw(self):
        #Draw the character on the given screen.
        screen.blit(self.image, self.position)
#definizioni degli oggetti per quale motivo questo era sotto l'inzializzazione del gioco un po' di ordine Andrea che cazzo

#oggetto player
player = Character("player.png",50,20,[xlim/2 - 25, ylim/2 - 25], [0,0])
#oggetto bolognesi
Bolognesi = Character("bolognesi.jpeg",200,200,[np.random.randint(200,xlim-200),400],[0,0])
#oggetto bonati
Bonati = Character("bonati_Claudio-Bonati.jpg",70,5,[0,0],[0,0])
#un nemico dovrebbe avere una size, delle coordinate a lui associate e un'immagine ben definita


#evento jumpscare
jumpscare=game.image.load('bolo_jumpscare.jpg')
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(5,10)

#lista in cui salviamo le posizioni del player per bonati
#deve essere una lista perché il modo in cui funziona np.append appiattisce in 1D e quindi le posizioni non funzionano più
#usiamo lista e append nativo di pyton
last_n_position = []

#inizializzazione gioco
game.init()
running = True

while running:

    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    game.display.flip()
    screen.blit(background,(0,0))


    #game speed
    clock.tick(30)


#andrea devi esplodereeeeee
    
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

    #player movement
    if  game.key.get_pressed()[game.K_s]and player.position[1] <= ylim - (player.size+player.speed):
        player.direction[1] = 1
    if  game.key.get_pressed()[game.K_w]and player.position[1] >= player.speed:
        player.direction[1] = -1
    if  game.key.get_pressed()[game.K_d] and player.position[0]<= xlim -(player.size+player.speed):
        player.direction[0] = 1
    if  game.key.get_pressed()[game.K_a] and player.position[0] >= player.speed:
        player.direction[0] = -1
    
    player.update_position()
    last_n_position.append(player.position)
    if len(last_n_position) > 5:
        last_n_position = last_n_position[1:]
    #####################################################################################################################

                                                  #BONATI#

    #####################################################################################################################
    #quando aggiungeremo lo score basterà mettere un if score maggiore di qualcosa
    #aggiungo claudio bonati
    Bonati.draw()
    Bonati.direction = np.sign( last_n_position[0] - Bonati.position)
    Bonati.update_position()
    #####################################################################################################################


    '''
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
        running=False'''

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
