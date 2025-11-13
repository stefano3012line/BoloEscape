import pygame as game
import numpy as np
import time
xx = np.array([1,0,5,6,7,8])
xx = np.append(xx,12)
print(xx)
print(xx[1:])

y = np.array([2,3])
x = np.array([5,1])
z = y- x
print(z)
print(np.sign(z))


X = np.array([[1,1],[1,1],[1,1],[1,1]])
Y = np.array([2,2])
X = np.append(X,Y)
print(X)