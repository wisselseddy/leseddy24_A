import math
import cv2
import numpy as np
from numpy.fft import fft, ifft
#import utility
import cv2

arr = []

def FindDevices():
   global arr
   index = 0

   while (index < 255):
      cap = cv2.VideoCapture(index)
      jl = cap.read()
 #     print(jl)
      jk = jl[0]
      if jk:
         if cap.read()[0]:
            arr.append(index)
      cap.release()
      index += 1
   return arr

def drawCircle(pixels,centerx,centery,radius):
   for i in range(-1000,1000):
      fl = i/1000.0 * math.pi
      fl2 = math.sin(fl) * radius
      fl3 = math.cos(fl) * radius
      fl2 += centerx
      fl3 += centery
      pixels[int(fl2),int(fl3)] = (255, 255, 255)

def drawLine(pixels,startx, starty, endx, endy):
   bresenham(pixels,startx, starty, endx, endy)
# function for line generation

def bresenham(pixels,x1, y1, x2, y2):
 
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)
 
    y = y1
    for x in range(x1, x2+1):
 
        #print("(", x, ",", y, ")\n")
        pixels[int(x),int(y)] = (255,255,255)
 
        # Add slope to increment angle formed
        slope_error_new = slope_error_new + m_new
 
        # Slope error reached limit, time to
        # increment y and update slope error.
        if (slope_error_new >= 0):
            y = y+1
            slope_error_new = slope_error_new - 2 * (x2 - x1)

def plotLineLow(pixels,x0, y0, x1, y1, color):
   height, width, channels = pixels.shape
   dx = x1 - x0
   dy = y1 - y0
   yi = 1
   if dy < 0:
      yi = -1
      dy = -dy
   
   D = (2 * dy) - dx
   y = y0

   for x in range( x0 , x1):
      height, width, channels = pixels.shape
      if (x > -1 and x < width and y > -1 and y < height):
         pixels[int(x),int( y)]= color
         if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
         else:
            D = D + 2*dy
          
def plotLineHigh(pixels,x0, y0, x1, y1, color):
   height, width, channels = pixels.shape
   dx = x1 - x0
   dy = y1 - y0
   xi = 1
   if dx < 0:
       xi = -1
       dx = -dx

   D = (2 * dx) - dy
   x = x0

   for y in range( y0 ,y1):
      if (x > -1 and x < width and y > -1 and y < height):
       pixels[int(x),int( y)]= color
       if D > 0:
           x = x + xi
           D = D + (2 * (dx - dy))
       else:
           D = D + 2*dx
   return

def lineEJW(pixels,x0, y0, x1, y1):
     color = (255,255,255)
     if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(pixels,x1, y1, x0, y0, color)
        else:
            plotLineLow(pixels,x0, y0, x1, y1, color)
     else:
        if y0 > y1:
            plotLineHigh(pixels,x1, y1, x0, y0, color)
        else:
            plotLineHigh(pixels,x0, y0, x1, y1, color)
     return

def lineEJWColor(pixels,x0, y0, x1, y1,color):
     if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(pixels,x1, y1, x0, y0, color)
        else:
            plotLineLow(pixels,x0, y0, x1, y1, color)
     else:
        if y0 > y1:
            plotLineHigh(pixels,x1, y1, x0, y0, color)
        else:
            plotLineHigh(pixels,x0, y0, x1, y1, color)
     return

def DrawRect(pixels,x0,y0,x1,y1):
   lineEJW(pixels,x0,y0,x1,y0)
   lineEJW(pixels,x1,y0,x1,y1)
   lineEJW(pixels,x1,y1,x0,y1)
   lineEJW(pixels,x0,y1,x0,y0)

def DrawRectColor(pixels,x0,y0,x1,y1,color):
   lineEJWColor(pixels,x0,y0,x1,y0,color)
   lineEJWColor(pixels,x1,y0,x1,y1,color)
   lineEJWColor(pixels,x1,y1,x0,y1,color)
   lineEJWColor(pixels,x0,y1,x0,y0,color)

def DrawPolygon(pixels, arrPoints):
   size = arrPoints
   for lineIndex in range(size):
      arrPoint1 = arrPoints.remove(lineIndex)
      arrPoint2 = arrPoints.remove(lineIndex + 1)
      lineEJW(arrPoint1[0],arrPoint1[1],arrPoint2[0],arrPoint2[1])

def DrawFFTSingle(dataArray):
   # make the window

   cv2.namedWindow('image',cv2.WINDOW_NORMAL)
   cv2.setWindowTitle('image','Signal Picture')
   cv2.moveWindow('image', 100, 100)
   cv2.resizeWindow('image', 640, 350)
   img = cv2.imread('c:\pc-bck\Images\dummyA.bmp',cv2.IMREAD_UNCHANGED)
   cv2.imshow('image',img)
   cv2.waitKey(20)

   DrawFFTContinuous(img, dataArray)

   cv2.imshow('image',img)
   cv2.waitKey(0)
   cv2.destroyAllWindows()
   pass


def DrawFFTContinuous(img,dataArray):
   arrComplex = np.empty(44100, dtype=np.complex128)

   arrDouble = np.empty(44100, dtype=np.double)
   arrComplex = fft(dataArray)
   arrDouble = np.abs(arrComplex)

   arrDoubleMax = max(arrDouble)

   arrDisplayConstant = 256.0 / arrDoubleMax
   arrDisplay = np.empty(22050,np.uint16)

   for cc in range(0, 22050):
      xIndexToDisplay = 0
      toDisplay = 0
      arrDisplay[cc] = arrDisplayConstant * arrDouble[cc]

   deltax = 22050.0 / 640.0
   intDeltax = int(deltax)

   for dx in range(0,640):
      arrValue = 0
      for ix in range(dx * intDeltax, (dx+1) * intDeltax):
         arrValue += int(arrDisplay[ix])
      arrValue += 0.5
      arrValue /= intDeltax
      intValue = int(arrValue)
      if (intValue > 0):
         a=10
      img[300 - intValue * 2,dx,0] = 0
      img[300 - intValue * 2,dx,1] = 0
      img[300 - intValue * 2,dx,2] = 0
      lineEJWColor(img, 300 - intValue * intDeltax, dx,0,dx,(255,230,238))



class Point:
    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Point.")
        return super().__new__(cls)

    def __init__(self, x, y):
        print("2. Initialize the new instance of Point.")
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x}, y={self.y})"


