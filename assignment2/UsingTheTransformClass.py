from math import *
import numpy as np
from matrix import matrix
from transform import transform

#Creating a translation matrix M
M1 = transform().translate(10.0,20.0,30.0)
print(M1)

#Creating a scaling matrix M
M2 = transform().scale(10.0,20.0,30.0)
print(M2)

#creating a rotation matrix M with angle pi/2.0 around axis (1,1,1)
M = transform().rotate(matrix(np.ones((3,1))),pi/2.0)
print(M)