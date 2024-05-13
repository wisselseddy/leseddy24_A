import threading
import cv2
import numpy as np
from CVLA import CVLA
from Graph5 import *
from threading import *
import time
import win32con
import win32api
import win32gui
from CParameters import CParameters

class CAnalysFrame(object):
   def __init__(self,CParams):
      CParams.analysFrame = self
      self.cParams = CParams
      self.xPos = -1
      self.yPos = -1
      self.direction = 0
      self.lastDirection = 0
      self.listBodyPoints = [()]
      self.winID = 'AnalysTool'
      self.strTitle = 'Tool for testing frame analysis'
      self.bAlive = self.cParams.commandHandler.bAnalysFrameActive
      self.analysResultData = np.full((300,300,3),[230,230,230],dtype = 'uint8')
      self.listxy = [()]
      self.listXy = [()]
      self.listxY = [()]
      self.frameContents = self.cParams.displayHandler.orgVideoBuffer.copy()
      self.listxy.clear()
      self.listXy.clear()
      self.listxY.clear()
      h,w,c = self.frameContents.shape
      for hi in range(h):
         for wi in range(w):
            if (self.frameContents[hi][wi][0] != 0 or
                self.frameContents[hi][wi][1] != 0 or
                self.frameContents[hi][wi][2] != 0):
               self.listxy.append((wi,hi))
      
      self.listXy = self.listxy.copy()
      self.listxY = self.listxy.copy()
   
      self.listXy.sort(key=lambda t: t[0])
      self.listxY.sort(key=lambda t: t[1])

      self.Run()
      pass
   
   def U(self):
      self.yPos -= 1
      self.lastDirection = 7
      pass
   
   def UL(self):
      self.yPos -= 1
      self.xPos -= 1
      self.lastDirection = 6
      pass
   
   def UR(self):
      self.yPos -= 1
      self.xPos += 1
      self.lastDirection = 8
      pass
   
   def D(self):
      self.yPos += 1
      self.lastDirection = 3
      pass

   def DL(self):
      self.yPos += 1
      self.xPos -= 1
      self.lastDirection = 4
      pass
   
   def DR(self):
      self.yPos += 1
      self.xPos += 1
      self.lastDirection = 2
      pass
   
   def L(self):
      self.xPos -= 1
      self.lastDirection = 5
      pass
   
   def R(self):
      self.xPos += 1
      self.lastDirection = 1
      pass   

   def MarkLocations(self,Contents,ListXy, Direction):
      lastDirection = Direction
      listBodyPoints = [()]
      bScanning = True
      (C1B, C1G, C1R) = cv2.split(Contents)
      
      (x,y) = ListXy[0]    # this is the first most left point, follow clockwise
                           # so list is (+1,-1)
                           # crawl right of you
      cp = (x-1,y)         # first centerpoint must be black,right not
                           # scan around red
      
      while bScanning and self.cParams.bSystemAlive:
         if (self.xPos == -1):
            self.xPos = x
         if (self.yPos == -1):
            self.yPos = y
         y = self.yPos
         x = self.xPos
         self.listBodyPoints.append((x,y))
         surroundingsData = Contents[y-1:y+2,x-1:x+2]     # x1,y1     --- x2,y2 
         if self.lastDirection == 1:
            if (surroundingsData[0][0] == [0,0,0]).all():
               if (surroundingsData[0][1] == [0,0,0]).all():
                  if (surroundingsData[0][2] == [0,0,0]).all():
                     if (surroundingsData[1][2] == [0,0,0]).all():
                        if (surroundingsData[2][2] == [0,0,0]).all():
                           if (surroundingsData[2][1] == [0,0,0]).all():
                              if (surroundingsData[2][0] == [0,0,0]).all():
                                 if (surroundingsData[1][0] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return
                                 else:
                                    self.L()
                              else:
                                self.DL()
                           else:
                              self.D()
                        else:
                           self.DR()
                     else:   
                        self.R()
                  else:
                     self.UR()
               else:
                  self.U()
            else:
               self.UL()
   
         elif self.lastDirection == 2:
            if (surroundingsData[1][0] == [0,0,0]).all():
               if (surroundingsData[0][0] == [0,0,0]).all():
                  if (surroundingsData[0][1] == [0,0,0]).all():
                     if (surroundingsData[0][2] == [0,0,0]).all():
                        if (surroundingsData[1][2] == [0,0,0]).all():
                           if (surroundingsData[2][2] == [0,0,0]).all():
                              if (surroundingsData[2][1] == [0,0,0]).all():
                                 if (surroundingsData[2][0] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return
                                 else:
                                    self.DL()
                              else:
                                self.D()
                           else:
                              self.DR()
                        else:
                           self.R()
                     else:   
                        self.UR()
                  else:
                     self.U()
               else:
                  self.UL()
            else:
               self.L()
               
         elif self.lastDirection == 3:
            if (surroundingsData[1][2] == [0,0,0]).all():
               if (surroundingsData[2][2] == [0,0,0]).all():
                  if (surroundingsData[2][1] == [0,0,0]).all():
                     if (surroundingsData[2][0] == [0,0,0]).all():
                        if (surroundingsData[1][0] == [0,0,0]).all():
                           if (surroundingsData[0][0] == [0,0,0]).all():
                              if (surroundingsData[0][2] == [0,0,0]).all():
                                 if (surroundingsData[0][1] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return
                                 else:
                                    self.U()
                              else:
                                self.UR()
                           else:
                              self.UL()
                        else:
                           self.L()
                     else:   
                        self.DL()
                  else:
                     self.D()
               else:
                  self.DR()
            else:
               self.R()
      
         elif self.lastDirection == 4:
            if (surroundingsData[1][2] == [0,0,0]).all():
               if (surroundingsData[2][2] == [0,0,0]).all():
                  if (surroundingsData[2][1] == [0,0,0]).all():
                     if (surroundingsData[2][0] == [0,0,0]).all():
                        if (surroundingsData[1][0] == [0,0,0]).all():
                           if (surroundingsData[0][0] == [0,0,0]).all():
                              if (surroundingsData[0][1] == [0,0,0]).all():
                                 if (surroundingsData[0][2] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return
                                 else:
                                    self.UR()
                              else:
                                self.U()
                           else:
                              self.UL()
                        else:
                           self.L()
                     else:   
                        self.DL()
                  else:
                     self.D()
               else:
                  self.DR()
            else:
               self.R()
   
         elif self.lastDirection == 5:
            if (surroundingsData[2][2] == [0,0,0]).all():
               if (surroundingsData[2][1] == [0,0,0]).all():
                  if (surroundingsData[2][0] == [0,0,0]).all():
                     if (surroundingsData[1][0] == [0,0,0]).all():
                        if (surroundingsData[0][0] == [0,0,0]).all():
                           if (surroundingsData[0][1] == [0,0,0]).all():
                              if (surroundingsData[0][2] == [0,0,0]).all():
                                 if (surroundingsData[1][2] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return 
                                 else:
                                    self.R()
                              else:
                                self.UR()
                           else:
                              self.U()
                        else:
                           self.UL()
                     else:   
                        self.L()
                  else:
                     self.DL()
               else:
                  self.D()
            else:
               self.DR()
         elif self.lastDirection == 6:
            if (surroundingsData[2][1] == [0,0,0]).all():
               if (surroundingsData[2][0] == [0,0,0]).all():
                  if (surroundingsData[1][0] == [0,0,0]).all():
                     if (surroundingsData[0][0] == [0,0,0]).all():
                        if (surroundingsData[0][1] == [0,0,0]).all():
                           if (surroundingsData[0][2] == [0,0,0]).all():
                              if (surroundingsData[1][2] == [0,0,0]).all():
                                 if (surroundingsData[2][2] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return
                                 else:
                                    self.DR()
                              else:
                                self.R()
                           else:
                              self.UR()
                        else:
                           self.U()
                     else:   
                        self.UL()
                  else:
                     self.L()
               else:
                  self.DL()
            else:
               self.D()
         elif self.lastDirection == 7:
            if (surroundingsData[1][0] == [0,0,0]).all():
               if (surroundingsData[0][0] == [0,0,0]).all():
                  if (surroundingsData[0][1] == [0,0,0]).all():
                     if (surroundingsData[0][2] == [0,0,0]).all():
                        if (surroundingsData[1][2] == [0,0,0]).all():
                           if (surroundingsData[2][2] == [0,0,0]).all():
                              if (surroundingsData[2][0] == [0,0,0]).all():
                                 if (surroundingsData[2][1] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self. bScanning = False
                                    return
                                 else:
                                    self.D()
                              else:
                                self.DL()
                           else:
                              self.DR()
                        else:
                           self.R()
                     else:   
                        self.UR()
                  else:
                     self.U()
               else:
                  self.UL()
            else:
               self.L()
         elif self.lastDirection == 8:
            if (surroundingsData[1][0] == [0,0,0]).all():
               if (surroundingsData[0][0] == [0,0,0]).all():
                  if (surroundingsData[0][1] == [0,0,0]).all():
                     if (surroundingsData[0][2] == [0,0,0]).all():
                        if (surroundingsData[1][2] == [0,0,0]).all():
                           if (surroundingsData[2][2] == [0,0,0]).all():
                              if (surroundingsData[2][1] == [0,0,0]).all():
                                 if (surroundingsData[2][0] == [0,0,0]).all():
                                    # unique single point
                                    self.listBodyPoints.append((x,y))
                                    self.bScanning = False
                                    return
                                 else:
                                    self.DL()
                              else:
                                self.D()
                           else:
                              self.DR()
                        else:
                           self.R()
                     else:   
                        self.UR()
                  else:
                     self.U()
               else:
                  self.UL()
            else:
               self.L()
      pass
   
   def Run(self):
      xPos = self.cParams.posStartXPythonTerminal + self.cParams.widthPytonTerminal
      yPos = self.cParams.display_posY
      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
      cv2.setWindowTitle(self.winID,self.strTitle)
      cv2.resizeWindow(self.winID, 300, 300)
    
   # Create the vertical slider window
      cv2.moveWindow(self.winID,xPos,yPos)
      cv2.setMouseCallback(self.winID,self.MouseCB)
  
      self.bAlive = True
      while (self.bAlive): 
         cv2.imshow(self.winID, self.analysResultData) 
         key = cv2.waitKey(30)
         if key == 27 & 0xff:
            break    
      print('AnalysFrame Stopped')
      
   def MouseCB(self, action, x, y, flags, *userdata):
      pass
   
def MouseCB():
   pass

if __name__ == '__main__':
   winID = 'AnalysTool'
   title = 'Tool for testing frame analysis'
   
   testData = np.full((300,300,3),[230,230,230],dtype = 'uint8')
   cv2.namedWindow(winID, cv2.WINDOW_NORMAL)
   cv2.setWindowTitle(winID,title)
   cv2.resizeWindow(winID, 300, 300)
    
   # Create the vertical slider window
   cv2.moveWindow(winID,20, 20)

   # Set up the mouse handler
   cv2.setMouseCallback(winID,MouseCB)
   
   bAlive = True
   while (bAlive): 
      cv2.imshow(winID, testData) 
      key = cv2.waitKey(30)
      if key == 27 & 0xff:
         break    
    

