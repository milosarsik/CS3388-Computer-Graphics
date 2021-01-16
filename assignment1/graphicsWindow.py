import operator
from PIL import Image

class graphicsWindow:

    def __init__(self,width=640,height=480):
        self.__mode = 'RGB'
        self.__width = width
        self.__height = height
        self.__canvas = Image.new(self.__mode,(self.__width,self.__height))
        self.__image = self.__canvas.load()

    def drawPoint(self,point,color):
        if 0 <= point[0] < self.__width and 0 <= point[1] < self.__height:
            self.__image[point[0],point[1]] = color

    def drawLine(self,point1,point2,color): 
        # Getting the x1 and x2 point
        x1 = point1.get(0,0)
        x2 = point2.get(0,0)

        # Getting the y1 and y2 point
        y1 = point1.get(1,0)
        y2 = point2.get(1,0)

        # Calculating the difference in x and the difference in y
        dx = x2 - x1
        dy = y2 - y1

        # Setting the slope by default to 1        
        slopeX = 1
        slopeY = 1

        # Checking if slope is lower than 0, if it is then we set it to -1 for slopeX
        if(dx < 0):
            slopeX = -1
        
        # Checking if slope is lower than 0, if it is then we set it to -1 for slopeY
        if(dy < 0):
            slopeY = -1

        # Check the condition, is absolute dy less than absolute dx, if it is why find the parts of the equation m and b
        if (abs(dy) < abs(dx)):

            # Here we find variables m and b, to get the equation y = mx+b, m is the dx and dy divided
            # and b is found by rearranging y = mx + b
            m = dy/dx
            b = y1 - m * x1

            # The while loop will iterate until x1 (the start point) has incremented all the the way until the destination point x2
            while x1 != x2:
                tempY = m*x1 + b

                # We call the image which contains the canvas, and we light up a single pixel
                # We pass in the point x1, calculate the point y and round it
                # A color is also passed in
                self.__image[x1, int(round(tempY))] = color

                # x1 is incremented by the x-axis slope to get the next point
                x1 = x1 + slopeX
        else:

            # This is run if dy is greater than dx, or they are equal, the equation must be changed to use the y instead of the x
            # Again, we calculate the m of the equation and the b
            m = dx/dy
            b = x1 - m*y1

            # Iterate until y1 is the same as the destination point and then end the loop
            while y1 != y2:
                tempX = m*y1 + b

                # Get the canvas and light up the pixel based off of the x we get (calculated with rearranged equation above) and the y1 we already have
                self.__image[int(round(tempX)), y1] = color

                # y1 is incremented by the y-axis slope to get the next point
                y1 = y1 + slopeY

    def saveImage(self,fileName):
        self.__canvas.save(fileName)

    def showImage(self):
        self.__canvas.show()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height