import pygame as game
import numpy as np
import time
#inizializzazione gioco
game.init()
running = True
xlim=1280
ylim=720
screen = game.display.set_mode((xlim,ylim))
clock = game.time.Clock()
background=game.image.load('C:\\Users\\Dell\\Desktop\\programmi python\\bolo escape\\unipipi.jpeg')
background=game.transform.smoothscale(background,(xlim,ylim))
score=0

#evento jumpscare
jumpscare=game.image.load('C:\\Users\\Dell\\Desktop\\programmi python\\bolo escape\\bolo_jumpscare.jpg')
jumpscare=game.transform.smoothscale(jumpscare,(xlim,ylim))
event_jumpscare= np.random.randint(2,5)
#info giocatore
size = 50
x=xlim/2 - size/2
y=ylim/2 - size/2
size = 50
speed= 15

#un nemico dovrebbe avere una size, delle coordinate a lui associate e un'immagine ben definita

#info bolognesi
B_size=200
B_x= np.random.randint(B_size,xlim-B_size)
B_y= - 2*B_size
B_dir= 1
B_speed=200
B_accell=B_speed/5
Bolognesi=game.image.load("C:\\Users\\Dell\\Desktop\\programmi python\\bolo escape\\bolognesi.jpeg")
Bolognesi=game.transform.smoothscale(Bolognesi,(B_size,B_size))




while running:

    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
    #sistema di coordinate centrato in alto a sinistra e background
    game.display.flip()
    screen.blit(background,(0,0))



    #game speed
    clock.tick(60)

    #game event jumpscare
    if event_jumpscare == score:
        screen.blit(jumpscare,(0,0))
        game.display.update()
        time.sleep(.5)
        event_jumpscare+=score + np.random.randint(5,10)
        score+=1


    #player movement
    if  game.key.get_pressed()[game.K_s]and y <= ylim - (size+speed):
        y+=speed
    if  game.key.get_pressed()[game.K_w]and y >= speed:
        y-=speed
    if  game.key.get_pressed()[game.K_d] and x <= xlim -(size+speed):
        x+=speed
    if  game.key.get_pressed()[game.K_a] and x >= speed:
        x-=speed




    #player character
    #game.draw.circle(screen,'black',(x,y),size)

    Player=game.image.load("C:\\Users\\Dell\\Desktop\\programmi python\\bolo escape\\player.png")
    Player=game.transform.smoothscale(Player,(size,size))
    screen.blit(Player,(x,y))





    #Bolognesi movement
    if B_dir == 0:#from north
        if B_y>= -(2*B_size) and B_y<=ylim+(B_size*2):
            screen.blit(Bolognesi,(B_x,B_y))
            B_y+=B_speed/(5*np.sqrt(B_size))


    elif B_dir == 1:#from south
        if B_y>= -(2*B_size) and B_y<=ylim+(B_size*2):
            screen.blit(Bolognesi,(B_x,B_y))
            B_y -= B_speed/(5*np.sqrt(B_size))


    elif B_dir == 2:#from est
        if B_x>= -(2*B_size) and B_x<=xlim+(2*B_size):
            screen.blit(Bolognesi,(B_x,B_y))
            B_x -= B_speed/(5*np.sqrt(B_size))



    elif B_dir == 3:#from west
        if B_x>= -(2*B_size) and B_x<=xlim+(2*B_size):
            screen.blit(Bolognesi,(B_x,B_y))
            B_x += B_speed/(5*np.sqrt(B_size))


        #giving random dir
    if B_y< -(2*B_size) or B_y>ylim+(B_size*2) or B_x< -(2*B_size) or B_x>xlim+(B_size*2) :
        B_dir = np.random.randint(0,4)
        B_size = np.random.randint(10,500)
        B_accell=int((B_speed/(3.5*score+1)))+1
        score+=1
        print(score,B_speed)



#spawn for different directions size and speed
        if B_dir == 0:#from north
           # B_size=np.random.randint(size,3*size)
            B_x= np.random.randint(0,xlim-B_size)
            B_y= -(2*B_size)
            B_speed+= B_accell
        elif B_dir == 2:#from est
           # B_size=np.random.randint(size,3*size)
            B_y= np.random.randint(0,ylim-B_size)
            B_x= xlim+(2*B_size)
            B_speed+= B_accell
        elif B_dir == 1:#from south
           # B_size=np.random.randint(size,3*size)
            B_x= np.random.randint(0,xlim-B_size)
            B_y= ylim +(2*B_size)
            B_speed+= B_accell
        elif B_dir == 3:#from west
           # B_size=np.random.randint(size,3*size)
            B_y= np.random.randint(0,ylim-B_size)
            B_x= -(2*B_size)
            B_speed+= B_accell
    Bolognesi=game.transform.smoothscale(Bolognesi,(B_size,B_size))


    #defining player center
    center_x= x + size/2
    center_y= y + size/2

    #defining Bolognesi center
    center_B_y = B_y + B_size/2
    center_B_x = B_x + B_size/2

    #getting hit
    if  np.abs(center_x-center_B_x) <= (size+B_size)/2 and np.abs(center_y-center_B_y) <= (size+B_size)/2 :
        size = size/2
        B_y = ylim +1000

    if size <= 20 or size>=100:
        running=False

    # Font per il punteggio
    font = game.font.SysFont('Arial', 40)
    text_color = (0, 0, 0)

    # Mostra il punteggio a schermo
    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (20, 20))  # posizione (x=20, y=20)

    game.display.update()


#end game routine
background=game.image.load('C:\\Users\\Dell\\Desktop\\programmi python\\bolo escape\\death_screen.jpg')
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
