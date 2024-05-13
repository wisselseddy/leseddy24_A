import cv2
import numpy as np

def start(quantity, height):
   MakeBmp(quantity, height)
   pass

def MakeBmp(quantity, height):
   width = (quantity - 1) * 11 + 10 + 10
   img = np.full((height, width, 3), [255,255,255], dtype='uint8')
   startLine = 10
   endLine = height - 10 
   for q in range( 0, quantity):
      w = q * 11 + 10
      for h in range(startLine, height - 10):
         img[h][w][0] = 0
         img[h][w][1] = 0
         img[h][w][2] = 0
         
         img[h][w-1][0] = 0
         img[h][w-1][1] = 0
         img[h][w-1][2] = 0
         
         img[h][w+1][0] = 0
         img[h][w+1][1] = 0
         img[h][w+1][2] = 0

   for q in range( 0, quantity):
      w = q * 11 + 10
      for x in range(w - 5, w + 5):
         img[startLine][x][0] = 0
         img[startLine][x][1] = 0
         img[startLine][x][2] = 0
      for x in range(w - 5, w + 5):
         img[endLine][x][0] = 0
         img[endLine][x][1] = 0
         img[endLine][x][2] = 0

   cv2.imwrite("C:\\pc2324\\Images\\AutoSliderImg.bmp", img)

   return width

# For testing only
# ****************

#if __name__ == "__main__":
#   quan = int(input('Quantity: '))
#   hei = int(input('Height: '))
#   start(quan, hei)
