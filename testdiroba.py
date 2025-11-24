import pygame as game
from pygame import mixer
import numpy as np
import time
from matplotlib import pyplot as plt
import os
'''
game.init()
mixer.init()
Bolo_passing =mixer.Sound('bolognesi-passing.mp3')
Bolo_passing.play()  # Play the sound.
game.time.delay(4000)
print('Playing sound')'''

y = np.array([600,720,800,861,911,954,992,1026,1053,1076,1097,1117,1135,1151,1166,1181,1195,1209,1222,1234,1246,1257,1268,1278,1288,1297,1306,1315,1324,1332,1340,1348,1356,1364,1371,1378,1385,1392,1399,1406,1413,1420,1426,1432,1438,1444,1450,1456,1462,1468,1474,1480,1485,1490,1495,1500,1505,1510,1515,1520,1525,1530,1535,1540,1545,1550])
x = np.arange(len(y))

plt.figure()
plt.subplot(1,1,1)
plt.plot(x,y)
plt.show()
"""
a = [1,2,3]
b=a.copy()
b *= 2
print(a,b)

def rotate_Vector(V,theta):
    #theta = np.radians(phi)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    print(R)
    return  R@V

v1 = np.array((0,1))
v2 = rotate_Vector(v1,np.pi/2)
print(v2)

import os
with os.scandir('fotoClaudio') as d:
    for e in d:
        print('fotoClaudio/'+ e.name)
"""
"""
import itertools as it
n = 15
i = 0

for j in it.cycle(['andrea','è','gay']):
    print(j)
    i +=1
    if i == 15:
        break
"""