"""shader Class

For a given ray (and its corresponding pixel (i , j) in the image), the constructor computes the color for the
pixel (i , j) by applying a shading model.

Author: Milos Arsik
Student Number: 250953645
Email: marsik@uwo.ca
"""

class shader:
    def __init__(self,intersection,direction,camera,objectList,light):
            """ Computes the shaded color for pixel (i , j) as instance variable self.__color

            Args:
                intersection: s the first (k ,t0) tuple from the intersection list
                direction: is the vector describing the direction of the ray
                camera: is the vector to the light source
                objectList:  is a list of objects composing the scene
                light: is a lightSource object
            
            Returns:
                None
            """

            # Consider tuple (k ,t0) from intersection 
            k = intersection[0]

            # object = objectList [k]
            temp = objectList.index(k)
            self.__object = objectList[temp]

            # t0 is the t-value associated with object from tuple (k ,t0)
            t0 = intersection[1]

            # M−1 = inverse of matrix T associated with object
            self.__matrixInverse = self.__object.getT().inverse()

            # Ts = light position transformed with M−1
            self.__Ts = self.__matrixInverse * light.getPosition()

            # Transform the ray with M−1 in the following way: Te=M−1e , where e is
            # the position of the camera, and Td=M−1*d , where d is the direction of the ray
            self.__Te = self.__matrixInverse * camera.getE()
            self.__Td = self.__matrixInverse * direction

            # Compute the intersection point as I=Te+Td*t0
            self.__I = self.__Te + self.__Td.scalarMultiply(t0)

            # Compute vector from intersection point to light source position as 
            # S=(Ts−I) , and normalize it
            sub = self.__Ts - self.__I
            self.__S = sub.normalize()

            # Compute normal vector at intersection point as N = object.normalVector (I)
            self.__N = self.__object.normalVector(self.__I)

            # Compute specular reflection vector as R=−S+(2 S⋅N )N
            transpremove = (self.__S.removeRow(3).transpose() * self.__N.removeRow(3))
            self.__R = (self.__N.scalarMultiply(2 * transpremove.get(0,0)) - self.__S)
            
            # Compute vector to center of projection V =Te−I, and normalize it
            self.__V = (self.__Te - self.__I).normalize()

            # Compute Id=max {N⋅S ,0} and Is=max {R⋅V ,0}
            self.__Is = max(((self.__R.removeRow(3).transpose() * self.__V.removeRow(3)).get(0,0)), 0)
            self.__Id = max(((self.__N.removeRow(3).transpose() * self.__S.removeRow(3)).get(0,0)), 0 )
            
            # r = object.getReflectance(), c = object.getColor(), Li = light.getIntensity()
            self.__Li = light.getIntensity()
            self.__c = self.__object.getColor()            
            self.__r = self.__object.getReflectance()

            # Temporary values
            self.__color = (0,0,0)
            self.__f = 0.0

            # If the intersection point is not shadowed by other objects e.g. this is a call 
            # to helper method __shadowed(object, I , S ,objectList):
            if self.__shadowed(self.__object, self.__I, self.__S,objectList):
                self.__f = self.__r[0]
            
            # Compute f =r[0]+r[1] I d+r[2] I s r[3]
            else:
                left = self.__r[0]
                mid = (self.__r[1] * self.__Id)
                right = (self.__r[2] * (self.__Is ** self.__r[3]))

                self.__f =  left + mid + right
        
            # Compute tuple self.__color = ( f (c [0] Li[0], c[1] Li[1], c [2] Li[2]))
            r = int(self.__f * self.__c[0] * self.__Li[0])
            g = int(self.__f * self.__c[1] * self.__Li[1])
            b = int(self.__f * self.__c[2] * self.__Li[2])

            self.__color = (r, g, b)

    def __shadowed(self,object,I,S,objectList):
        """ This method Returns true if the ray from the intersection point to the light source
            intersects with an object from the scene, and returns false otherwise.

        Args:
            object: is that which there is an intersection with
            I: is the intersection point
            S: is the vector to the light source
            objectList: is a list of object composing the scene

        Returns:
            bool: true if the ray from the intersection point to the light source intersects with an object 
                from the scene, and returns false otherwise.
        """
        
        # M = matrix T associated with object
        M = object.getT()

        # Compute I=M(I+ϵ S) where ϵ=0.001. This operation detaches the intersection 
        # point from its surface, and then transforms it into world coordinates
        I = M * (I + S.scalarMultiply(0.001))

        # Compute S=M*S. This transforms S into world coordinates
        S = M * S

        # For object in objectList
        for k in objectList:
            # M−1 = inverse of matrix T associated with object
            matrixInverse = k.getTinv()
            
            # Compute I=M−1*I . This transforms the intersection point into the generic coordinates of the object 
            Itemp = matrixInverse * I

            # Compute S=M−1*S and normalize S . This transforms the vector to the 
            # light source into the generic coordinates of the object
            Stemp = (matrixInverse * S).normalize()

            # If object.intersection (I , S) ≠ −1.0 : (this means there is an 
            # intersection with another object) then return True
            if k.intersection(Itemp,Stemp) != -1.0:
                return True

        # Return False
        return False

    def getShade(self):
        return self.__color
