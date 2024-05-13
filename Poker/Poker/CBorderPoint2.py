
from re import L
import numpy as np
import os
import sys
import time
import cv2
import inspect          # for checking 

from CParameters import CParameters

class CBorderPoint2(object):
   def __init__(self,CParams, NewPos, PrevPos):
      self.cParams = CParams
      self.pointID = -1
      self.currPosition = NewPos
      self.prevPosition = PrevPos
      self.counter = CParams.borderPointCounter
      self.rule = self.cParams.rule
      self.minBlue = self.rule[0]
      self.maxBlue =  self.rule[1]
      self.minGreen =  self.rule[2]
      self.maxGreen =  self.rule[3]
      self.minRed =  self.rule[4]
      self.maxred =  self.rule[5]
      self.videoArray = CParams.videoArray
      self.videoArrayStatus = CParams.videoArrayStatus
      pass
   
   def CheckPoint(self, X, Y):
      if not (X > 0 and X < 639 and Y > 0 and Y < 479):     # check x,y is inside the borders
         return -1
      retValue = 0
      if (self.videoArray[Y][X-1] != 0): retValue |= 0x01  
      if (self.videoArray[Y-1][X-1] != 0): retValue |= 0x02 
      if (self.videoArray[Y-1][X] != 0): retValue |= 0x04 
      if (self.videoArray[Y-1][X+1] != 0): retValue |= 0x08 
      if (self.videoArray[Y][X+1] != 0): retValue |= 0x10 
      if (self.videoArray[Y+1][X+1] != 0): retValue |= 0x20 
      if (self.videoArray[Y+1][X] != 0): retValue |= 0x40 
      if (self.videoArray[Y+1][X-1] != 0): retValue |= 0x80 
      return retValue 

   def Init(self):
      h,w,c = self.videoArray.shape
      for hi in range(h):
         for wi in range(w):
            self.videoArrayStatus = self.CheckPoint(wi,hi)

   def Run(self):
      self.cParams.pointID += 1
      self.pointID = self.cParams.pointID       # global pointer
      x = self.currentPos[0]
      y = self.currentPos[1]
      
      bRunning = True
      # Look around the point 1 - 8          no border found then done else 1 - 2 - 4 - 8 - 16 - 32 - 64 - 128
      
      while (bRunning):
         self.direction = 1
         self.videoArrayStatus[x][y] = self.CheckPoint(x,y)
         self.prevPosition = [x,y]
         if (self.direction == 1): self.newPosition = [x-1,y]
         if (self.direction == 2): self.newPosition = [x-1,y-1]
         if (self.direction == 3): self.newPosition = [x,y-1]
         if (self.direction == 4): self.newPosition = [x+1,y-1]
         if (self.direction == 5): self.newPosition = [x+1,y]
         if (self.direction == 6): self.newPosition = [x+1,y+1]
         if (self.direction == 7): self.newPosition = [x,y+1]
         if (self.direction == 8): self.newPosition = [x-1,y+1]
         
         if (self.videoArrayStatus[x][y]):
            continue
         else:
            self.listToDo[ind] = True
            
            if ind == 0:
               pos, bReturn = self.CheckPoint(x,y)                  # if False, do not start search further, you sit on the border
               self.prevPoint = [-1,-1]
               if (bReturn):
                  continue
               else:
                  break   
            elif ind == 1:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x - 1, y)
               if (bReturn):
                  newListToDo = [False,False,False,False,False,False,False,False,False]
               else:
                  continue   
            elif ind == 2:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x - 1, y - 1)       # if False, do not start search further, you sit on the border
               if (bReturn):
                  newListToDo = [False,True,False,False,False,False,False,False,True]   
               else:
                  continue                                        # you sit on the border
            elif ind == 3:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x, y - 1)
               if (bReturn):
                  newListToDo = [False,True,False,False,False,False,False,True,True]
               else:
                  continue
            elif ind == 4:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x + 1, y - 1)
               if (bReturn):
                  newListToDo = [False,True,False,False,False,False,False,False,True]
               else:
                  continue
            elif ind == 5:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x + 1, y)
               if (bReturn):                                   # when false, border discovered
                  newListToDo = [False,True,True,True,False,False,False,False,True]
               else:
                  continue
            elif ind == 6:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x + 1, y + 1)
               if (bReturn):
                  newListToDo = [False,False,True,True,False,False,False,False,False]
               else:
                  continue
            elif ind == 7:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x, y +  1)
               if (bReturn):
                  newListToDo = [False,False,True,True,True,False,False,False,False]
               else:
                  continue
            elif ind == 8:
               prevPoint = (x,y)
               pos, bReturn = self.CheckPoint(x - 1, y + 1)
               if (bReturn):
                  newListToDo = [False,False,False,True,True,True,False,False,False]
               else:
                  continue
            print(f'ID: {ind}')
            if (self.cParams.borderPointCounter == 18):
               bDebugA = 1

            newBP = CBorderPoint2(self.cParams, pos, prevPoint, newListToDo, ind)
            newBP.Run()
            pass
         pass
      print(f'ClassID: {self.cParams.borderPointCounter} Finished')
      pass
   
   def CheckPoint(self, X, Y):
      currentColor = self.cParams.videoArray[Y][X]
      blue = currentColor[0]
      green = currentColor[1]
      red = currentColor[2]
      
      if (blue > 250 and green > 250 and red > 250):
         return ((X,Y), True)       # continue search
      else:
         tup = tuple((X,Y))
         self.cParams.borderList.append(tup)
         print(f'Border at X:{X} - Y:{Y}')
         return ((X,Y), False)      # Halt search border found
         

if __name__ == "__main__":
   sys.setrecursionlimit(10000)  
   ll = len(inspect.stack())
   print(f'Current Stack: {ll}')
   
   parameters = CParameters()
   
   WinID = 'Main Display'
   parameters.videoArray = np.full((480,640,3), [0,0,0], dtype='uint8')
   parameters.videoArrayStatus = np.full((480,640,1), [0], dtype='uint8')

   cv2.namedWindow(WinID, cv2.WINDOW_NORMAL)
   cv2.resizeWindow(WinID, 640, 480)
#   buf = np.array()
   # Create the vertical slider window
   cv2.namedWindow(WinID, cv2.WINDOW_NORMAL)
   cv2.resizeWindow(WinID, 640, 480)
   cv2.moveWindow(WinID,20, 20)
   
   while(True):
      cv2.imshow(WinID, parameters.videoArray) 
      key = cv2.waitKey(10) & 0xff
      if (key == 27):
         break
      
   parameters.videoArray = cv2.rectangle(parameters.videoArray,[318,238],[322,242],[255,255,255], -1)
   
   while(True):
      cv2.imshow(WinID, parameters.videoArray) 
      key = cv2.waitKey(10) & 0xff
      if (key == 27):
         break
   
#   strInput = input('Rules: ')
#   rule = list(strInput[7:])
   parameters.rule = [10,250,10,250,10,250]   
   
   a = parameters.videoArray[240][320]
   
   startPoint = CBorderPoint2(parameters, [320,240],[-1,-1])
   b = startPoint.cParams.videoArray[240][320]
   startPoint.Run()

   while(True):
      cv2.imshow(WinID, parameters.videoArray) 
      key = cv2.waitKey(10) & 0xff
      if (key == 27):
         break







