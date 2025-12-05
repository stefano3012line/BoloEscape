import numpy as np


#funzione che calcola se sei colpito o meno 
#attenzione il primo oggetto che si passa alla funzione è quello a cui si applica l'effetto
def hit(obj1, obj2, key=None, t=None, damage=True, both=False):
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
                            obj1.status_effects.append(status(i,j,image=('fotoStatus/' + j + '.png'), size = 50))
                            print('bolo effettuato')
                            if both:
                                obj2.status_effects.append(status(i,j))
                    else: 
                        for i,j in zip(t,obj2.type):
                            obj1.status_effects.append(status(i,j,image=('fotoStatus/' + j + '.png'), size = 50))
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