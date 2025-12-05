import numpy as np




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