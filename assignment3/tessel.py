"""tessel Class

This is a python class that will draw the entire image using the objects, camera position and light source 
The tessel class has 3 attributes:
    - Object List: A list of objects, each having there own position, color, and reflectance
    - Camera: This is the camera object that has the information on how to view the objects with depth and position
    - Light: This will be an object of the light source class that will store the position, color and light 
        intensity of the light source
"""

import numpy as np
from matrix import matrix

class tessel:

    def __init__(self,objectList,camera,light):
        """This will initialize a practical lighting model using the passed in objects
            objectList, camera and light source

        Args:
            objectList: A list of objects such as a cone, torus, cylinder, etc.
            camera: A camera matrix that has the information on how we view every object in the scene
            light: A light source object that stores the position, color and intensity of the light

        Returns:
            None
        """

        EPSILON = 0.001
        
        #Create an empty list of faces. This is an instance variable for this class
        self.__faceList = []
        
        #Create an empty list for the points forming a face
        facePoints = []
        
        #Transform the position of the light into viewing coordinates (use method worldToViewingCoordinates from class cameraMatrix)
        lightViewingCoordinates = camera.worldToViewingCoordinates(light.getPosition())

	    #Get light intensity values
        lightIntensity = light.getIntensity() #Obtain light intensity
        
        #For each object in objectList:
        for object in objectList:
            #Get the object color
            color = object.getColor()

            #u becomes the start value of the u-parameter range for the object
            u = object.getURange()[0]
	        
            #While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON:
            while u + object.getUVDelta()[0] < object.getURange()[1] + EPSILON:
        		#v become the start value of the v-parameter range for the object
                v = object.getVRange()[0]
        		
                #While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON:
                while v + object.getUVDelta()[1] < object.getVRange()[1] + EPSILON:
                    #Collect surface points transformed into viewing coordinates in the following way:
            		    #Get object point at (u,v), (u, v + delta v), (u + delta u, v + delta v), and (u + delta u, v)
		                #Transform these points with the transformation matrix of the object
		                #Transform these points from world to viewing coordinates
		                #Append these points (respecting the order) to the list of face points                    
                    facePoints.append(camera.worldToViewingCoordinates(object.getT()*object.getPoint(u,v)))
                    facePoints.append(camera.worldToViewingCoordinates(object.getT()*object.getPoint(u,v+object.getUVDelta()[1])))
                    facePoints.append(camera.worldToViewingCoordinates(object.getT()*object.getPoint(u+object.getUVDelta()[0],v+object.getUVDelta()[1])))
                    facePoints.append(camera.worldToViewingCoordinates(object.getT()*object.getPoint(u+object.getUVDelta()[0],v)))
                    
                    #Make sure we don't render any face with one or more points behind the near plane in the following way:
		                #Compute the minimum Z-coordinate from the face points
		                #If this minimum Z-value is not greater than -(Near Plane) (so the face is not behind the near plane):                    
                    if not self.__minCoordinate(facePoints,2) > -camera.getNp():
            			#Compute the centroid point of the face points
                        centroid = self.__centroid(facePoints) #Find centroid point of face
			            
                        #Compute the normal vector of the face, normalized
                        normal = self.__vectorNormal(facePoints) #Find normal vector to face

	            		#Compute face shading, excluding back faces (normal vector pointing away from camera) in the following way:
                        if not self.__backFace(centroid,normal):
	            		    #S is the vector from face centroid to light source, normalized
                            S = self.__vectorToLightSource(lightViewingCoordinates,centroid)  # Find vector from centroid to light source
            			    
                            #R is the vector of specular reflection
                            R = self.__vectorSpecular(S,normal)  # Find specular reflection vector
            
			                #V is the vector from the face centroid to the origin of viewing coordinates
                            V = self.__vectorToEye(centroid)  # Find vector from origin of viewing coordinates to surface centroid
                            
                            # Compute color index
                            index = self.__colorIndex(object,normal,S,R,V)
                            
                            #Obtain face color (in the RGB 3-color channels, integer values) as a tuple:
			                    #(object color (red channel) * light intensity (red channel) * index,
			                    # object color (green channel) * light intensity (green channel) * index,
			                    # object color (blue channel) * light intensity (blue channel) * index)
                            faceColor = (int(color[0]*lightIntensity[0]*index),int(color[1]*lightIntensity[1]*index),int(color[2]*lightIntensity[2]*index))
                            
                            #Transform 3D points expressed in viewing coordinates into 2D pixel coordinates
                            pixelFacePoints = []
                
                            #For each face point:
                            for point in facePoints:
                                #Transform point into 2D pixel coordinates and append to a pixel face point list
                                pixelFacePoints.append(camera.viewingToPixelCoordinates(point))
                            
                            #Add all face attributes to the list of faces in the following manner:
				                #append pixel Z-coordinate of face centroid, the pixel face point list, and the face color                            
                            self.__faceList.append((camera.viewingToPixelCoordinates(centroid).get(2,0),pixelFacePoints,faceColor))
                    
                    #Re-initialize the list of face points to empty
                    facePoints = []
		            
                    #v become v + delta v
                    v += object.getUVDelta()[1]
                
                #u becomes u + delta u
                u += object.getUVDelta()[0]

    def __minCoordinate(self,facePoints,coord):
        min = facePoints[0].get(coord,0)
        for point in facePoints:
            if point.get(coord,0) < min:
                min = point.get(coord,0)
        return min

    def __backFace(self,C,N):
        return C.dotProduct(N) > 0.0

    def __centroid(self,facePoints):
        sum = matrix(np.zeros((4,1)))
        for point in facePoints:
            sum += point
        return sum.scalarMultiply(1.0/float(len(facePoints)))

    def __vectorNormal(self,facePoints):
        U = (facePoints[3] - facePoints[1]).removeRow(3).normalize()
        V = (facePoints[2] - facePoints[0]).removeRow(3).normalize()
        return U.crossProduct(V).normalize().insertRow(3,0.0)

    def __vectorToLightSource(self,L,C):
        return (L.removeRow(3) - C.removeRow(3)).normalize().insertRow(3,0.0)

    def __vectorSpecular(self,S,N):
        return  S.scalarMultiply(-1.0) + N.scalarMultiply(2.0*(S.dotProduct(N)))

    def __vectorToEye(self,C):
        return C.removeRow(3).scalarMultiply(-1.0).normalize().insertRow(3,0.0)

    def __colorIndex(self,object,N,S,R,V):
        Id = (N.transpose()*S).get(0,0) #Compute local components of shading
        Is = (R.transpose()*V).get(0,0)
        if Id < 0.0: Id = 0.0
        if Is < 0.0: Is = 0.0
        r = object.getReflectance()
        index = r[0] + r[1]*Id + r[2]*Is**r[3]
        return index

    def getFaceList(self):
        return self.__faceList