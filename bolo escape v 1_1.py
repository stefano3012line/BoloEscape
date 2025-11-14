import pygame as game
import numpy as np
import time

#dimensioni schermo
xlim,ylim=1280,720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
score=-1/60

#funzione che calcola se sei colpito o meno 
def hit(obj1, obj2):
    overlap = np.abs(obj1.centre - obj2.centre) - (obj1.size + obj2.size)/2
    
    if overlap[0]<=0 and overlap[1]<=0 and obj1.hp>0 and obj2.hp>0:
        obj1.hp -=1
        obj2.hp -=1

#definizione della classe dei nemici semplici e player
#personaggio definito come: immagine,taglia,velocità, hitpoints, vettore posizione,vettore direzione in questo ordine

class Character:
    def __init__(self, image, size, speed,hp, position, direction):
        # Load and scale the image
        self.image = game.transform.smoothscale(game.image.load(image), (size, size))
        # Instance variables
        self.hp = hp
        self.size = size
        self.speed = speed
        self.position = np.array(position, dtype=float)
        self.direction = np.array(direction, dtype=float)
    @property   
    def centre(self):
        #Return the center point of the character
        return self.position + np.array([self.size / 2, self.size / 2])
    def update_position(self):
        #Move the character based on direction and speed
        if self.hp> 0:
            self.position += self.direction * self.speed
    def draw(self):
        #Draw the character on the given screen.
        if self.hp >0:
            screen.blit(self.image, self.position)
#i metodi delle classi sono 
#definizioni degli oggetti per quale motivo questo era sotto l'inzializzazione del gioco un po' di ordine Andrea che cazzo

#oggetto player
player = Character("player.png",50,20,3,[xlim/2 - 25, ylim/2 - 25], [0,0])
#oggetto bolognesi
#Bolognesi = Character("bolognesi.jpeg",200,200,[np.random.randint(200,xlim-200),400],[0,0])
#oggetto bonati
Bonati_spawn_value=np.random.randint(5,15)
Bonati = Character("bonati_Claudio-Bonati.jpg",70,10,0,[0,0],[0,0])
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
    score += 1/60
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
        Bonati_spawn_value+= np.random.randint(5,15)


   
    Bonati.draw()
    Bonati.direction = (last_n_position[0] - Bonati.position)/np.linalg.norm(last_n_position[0] - Bonati.position)
    Bonati.update_position()
    # checko l'hit con bonati
    
    hit(Bonati,player)
    #print(Bonati.direction)
    #####################################################################################################################

    if player.hp == 0:
        running=False

    # Font per il punteggio
    font = game.font.SysFont('Arial', 40)
    text_color = (0, 0, 0)

    # Mostra il punteggio a schermo
    score_text = font.render(f"Score: {int(score)}", True, text_color)
    screen.blit(score_text, (20, 20))  # posizione (x=20, y=20)

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
