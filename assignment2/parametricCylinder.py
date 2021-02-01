from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCylinder(parametricObject):
     
    def __init__(self,T=matrix(np.identity(4)),height=1.0,radius=1.0,color=(0,0,0),reflectance=(0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        # Set the values that were passed in
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)

        # Set the radius and height
        self.__height = height
        self.__radius = radius

    def getPoint(self,u,v):
        # Creating a 4x1 identity matrix to store the point
        P = matrix(np.ones((4,1)))

        # Setting the matrix with the equations of a cylinder
        P.set(0,0,self.__radius*cos(v))
        P.set(1,0,self.__radius*sin(v))
        P.set(2,0,self.__height*u)

        return P
    
    # Radius setter
    def setRadius(self,radius):
        self.__radius = radius
    
    # Radius getter
    def getRadius(self):
        return self.__radius
    
    # Height setter
    def setHeight(self,height):
        self.__height = height
    
    # Height getter
    def getHeight(self):
        return self.__height