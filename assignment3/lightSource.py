"""lightSource Class

This is a python class that will store information about a light source. 
The light source class has 3 attributes:
    - Position: This is the position of the light source a matrix with 4 points
    - Color: In this model (R ,G , B) is color for the light
    - Intensity: When incident light reaches a surface, some of it is radiated diffusely and reaches the eye of
        the observer with intensity
"""

import numpy as np
from matrix import matrix

class lightSource:

    def __init__(self,position=matrix(np.zeros((4,1))),color=(0,0,0),intensity=(1.0,1.0,1.0)):
        self.__position = position
        self.__color = color
        self.__intensity = intensity

    def getPosition(self):
        """Return a 4x1 2D matrix

        The position of the light source
        """
        return self.__position

    def getColor(self):
        """Return a triple

        The color of the light source as an RGB value stored in a triple
        """
        return self.__color

    def getIntensity(self):
        """Return a float triple

        This is the intensity of the light source given as IR, IG, and IB 
        """
        return self.__intensity

    def setPosition(self,position):
        """Set the position of the light source

        Args:
            position: The position of the light source as a 4x1 matrix

        Returns:
            None
        """
        self.__position = position

    def setColor(self,color):
        """Set the color of the light source

        Args:
            color: The color of the light source as a triple 

        Returns:
            None
        """
        self.__color = color

    def setIntensity(self,intensity):
        """Set the intensity of the light source

        Args:
            intensity: The intensity of the light source as a float triple 

        Returns:
            None
        """
        self.__intensity = intensity