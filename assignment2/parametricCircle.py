from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCircle(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),radius=1.0,color=(0,0,0),reflectance=(0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        # Set the values that were passed in
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        
        # Set the radius
        self.__radius = radius

    def getPoint(self,u,v):
        # Creating a 4x1 identity matrix to store the point
        P = matrix(np.ones((4,1)))
        
        # Setting the matrix with the equations of a circle
        P.set(0,0,self.__radius*u*cos(v))   
        P.set(1,0,self.__radius*u*sin(v))
        P.set(2,0,0)

        return P
    
    # Radius getter
    def getRadius(self):
        return self.__radius

    # Radius setter
    def setRadius(self,radius):
        self.__radius = radius
