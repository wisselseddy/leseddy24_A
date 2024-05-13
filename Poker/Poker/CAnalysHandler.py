from pickle import FALSE
from re import I
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

class CAnalysHandler(object):
   def __init__(self,CParams, Multiplier):
      CParams.analysHandler = self
      self.cParams = CParams
      self.bDebug = False
      self.bMouseDown = False
      self.bAlive = False
      self.winID = 'AnalysWindow'
      self.strWindowTitle = 'Analys Display'
      self.multiplier = Multiplier
      self.waitKeyValue = 1
      self.windowHeight = 300 * self.multiplier 
      self.windowWidth = CParams.displayHandler.window_width * self.multiplier
      self.windowPosX = 1920 - CParams.displayHandler.window_width * self.multiplier
      self.windowPosY = 1024 - 275 * self.multiplier
      self.videoArrayBlack = np.full((self.windowHeight,self.windowWidth,3),[0,0,0],dtype='uint8')
      self.videoArray = self.videoArrayBlack.copy()
      self.lockEvent = threading.Event()
      self.lockEvent.clear()
      self.vLineData = np.full((self.windowHeight,3),[255,255,255],dtype='uint8')
      self.bStatusVLA1 = False
      self.bStatusVLA2 = False
      self.oldLineY1ListIndex = -1   # this is a x index vla1
      self.oldLineY2ListIndex = -1   # this is a x index vla2
      self.oldLineY1List = [] 
      self.oldLineY2List = [] 
      self.bLockingActive = True
      self.oldText = ''
      self.bVLAActive = False
      self.currentVLA = -1          # Current VLA in use
      self.xPosVLA1 = -1
      self.xPosVLA2 = -1
      self.xOldPosVLA1 = -1
      self.xOldPosVLA2 = -1 
      self.currentY1LineIndex = -1
      self.currentY2LineIndex = -1
      self.bVLAAlive = False
      self.oldDataArray = []
      self.imageHeight = -1
      self.imageWidth = -1
      
      self.blueMax = 0
      self.blueMin = 255
      self.greenMax = 0
      self.greenMin = 255
      self.redMax = 0
      self.redMin = 255
      
      self.newVLA = None
      self.debugB = 0
      self.debugC = 0
      self.listDebugs = []
      self.yellowVLA = np.full((300 * self.multiplier,3),[230,230,0],dtype='uint8')
      self.whiteVLA = np.full((300 * self.multiplier,3),[230,230,230],dtype='uint8')
      self.presetVLAIndex = -1
      self.listActions = []
      self.cParams.listVLAPositions = []
      self.cParams.listVLA = []
      self.orgText = ''
      self.orgDataArray = None
      
   def MouseCB(self, action, x, y, flags, *userdata):
#      if (self.bMouseDown):
#         self.listDebugs.append(x)
#         self.listDebugs.append('Mouse Down')
      if action == cv2.EVENT_LBUTTONDOWN:
         hBackground, wBackground,channels = self.videoArray.shape
         self.listDebugs = []
         self.bGreen = False
         self.bRed = False
         self.bBlue = False
         sizeHeight = hBackground - 20

         if self.bDebug:
            print('MouseCB-LButtonDown')
         self.bMouseDown = True
      
         if (self.bVLAActive):
            self.newVLA = self.CreateVLA(self.cParams,x)
            self.DrawText(str(x // self.multiplier))
            
      if action == cv2.EVENT_MOUSEMOVE:
         # if (not self.bMouseDown):
         #    if (self.presetVLAIndex != -1):
         #       for hi in range(self.windowHeight):
         #          self.videoArray[hi][x] = [230,230,230]
         #          self.presetVLAIndex = -1
         #       cv2.imshow(self.winID, self.videoArray)
         #       pass
         
         #    if (x in self.cParams.listVLAPositions):
         #       for hi in range(self.windowHeight):
         #          self.videoArray[hi][x] = [230,230,0]
         #       self.presetVLAIndex = x
         #       cv2.imshow(self.winID, self.videoArray)
         #       pass   
         
         if self.bMouseDown:
            self.listDebugs.append(x)
            self.listDebugs.append('Move')
            if self.bDebug:
               print('LButtonDown-move')
            if (self.bVLAActive):
               if not self.newVLA == None:
                  self.newVLA.DrawVLA(x)
                  self.DrawText(str(x // self.multiplier))

      if action == cv2.EVENT_LBUTTONUP:
         if self.bMouseDown:
            self.listDebugs.append(x)
            self.listDebugs.append('Mouse UP')
            self.bMouseDown = False
            if (self.bVLAActive):
               self.cParams.listVLAPositions.append(x)
#            self.newVLA.DrawVLA(x)
            
      cv2.imshow(self.winID, self.videoArray)   
         
   def SetVLAbActive(self, Boolean):
      self.bVLAActive = Boolean
      if (Boolean == False):
         self.ClearVLA()
         
   def CreateVLA(self,CParameters,XPos):
      newVLA = CVLA(CParameters)
      CParameters.listVLA.append(newVLA)
      newVLA.DrawVLA(XPos)
      return newVLA
   
   def ClearVLA(self):
      self.cParams.listVLA.clear()
      self.cParams.listVLAPositions = []
      self.cParams.listVLA = []
      self.ClearPicture()
      self.oldText = ''
      self.DrawText(self.orgText)
      self.oldDataArray.clear()
      self.DrawLine(self.orgDataArray)
      
   def ChoiceVLA(self, MouseXPos):
      x = MouseXPos
      self.currentVLA = -1
      if (self.oldLineY1ListIndex != -1):
         if (x > self.xPosVLA1 -2 and x < self.xPosVLA1 + 2):
            self.currentVLA == 1
        
      if (self.oldLineY2ListIndex != -1):
         if (x > self.xPosVLA2 -2 and x < self.xPosVLA2 + 2):
            self.currentVLA == 2
      
      return self.currentVLA
   
   def DrawText(self, Text):
      strText = Text
      font = cv2.FONT_HERSHEY_SIMPLEX
      org = (50, 50)
      color = (255,255,255)
      thickness = 2
      fontScale = 1
#      strText = f'{x//3}'
      if (self.oldText != ''):
         self.videoArray = cv2.putText(self.videoArray, self.oldText, org, font,  
                              fontScale, (0,0,0), thickness, cv2.LINE_AA) 
         
      self.videoArray = cv2.putText(self.videoArray, strText, org, font,  
                              fontScale, color, thickness, cv2.LINE_AA) 
      self.oldText = strText

   def Run(self,Param):
      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
      cv2.setWindowTitle(self.winID,self.strWindowTitle)
      cv2.resizeWindow(self.winID, self.windowWidth, self.windowHeight)

      # Create the vertical slider window
      cv2.moveWindow(self.winID,self.windowPosX, self.windowPosY)

      # Set up the mouse handler
      cv2.setMouseCallback(self.winID,self.MouseCB)
         
      self.cParams.analysHandler.bAlive = True
      self.lockEvent.set()
      self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strWindowTitle)
      while (self.cParams.bAlive and self.cParams.analysHandler.bAlive):
#         if (self.bLockingActive):
#            self.lockEvent.wait()
#            self.lockEvent.clear()
         cv2.imshow(self.winID, self.videoArray) 
         key = cv2.waitKey(self.waitKeyValue)
        
         if key == 27 & 0xff:
            pass
      
      cv2.destroyWindow(self.winID)      
      pass

   def SetLockingOn(self):
      self.bLockingActive = True
      
   def SetLockingOff(self):
      self.bLockingActive = False
      
   def SetupMouseCB(self):
      cv2.setMouseCallback(self.winID,self.MouseCB)
      
   def Locking(self):
#      cv2.setMouseCallback(self.winID,self.MouseCB)

      while (self.cParams.bAlive and self.cParams.analysHandler.bAlive):
#         self.lockEvent.wait()
#         self.lockEvent.clear()
         cv2.imshow(self.winID, self.videoArray) 
         key = cv2.waitKey(30)
         if key == 27 & 0xff:
            pass
         
      cv2.destroyWindow(self.winID)
      

   def SetVLA(self, StatusVLA):
      self.bStatusVLA = StatusVLA
      if not StatusVLA:
         self.waitKeyValue = 30
         bRet = win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
         pass
      else:
         self.waitKeyValue = 0
      self.lockEvent.set()
      pass
   
   def ClearPicture(self):
      self.videoArray = self.videoArrayBlack.copy()
      self.oldDataArray = []
   
   def GetRules(self):
      borders = list((self.blueMin, self.blueMax,self.greenMin,self.greenMax, self.redMin, self.redMax))
      self.cParams.rule = borders
      return (borders)
   
   def DrawLine(self,DataArray):
      self.orgDataArray = DataArray.copy()
      
      def PaintPixels(self,wi,DataArray,blue,green,red):
         m = self.multiplier
         
         blueValue = self.windowHeight - (DataArray[wi][0] * m) - 20          # this is the blue component
         greenValue = self.windowHeight - (DataArray[wi][1] * m) - 20         # this is the green component
         redValue = self.windowHeight - (DataArray[wi][2] * m) - 20           # this is the red component
        
         self.videoArray[blueValue][wi*m] = blue
         self.videoArray[greenValue][wi*m] = green
         self.videoArray[redValue][wi*m] = red

         if (self.multiplier == 3):
            self.videoArray[blueValue][wi*3-1] = blue
            self.videoArray[blueValue][wi*3+1] = blue
            self.videoArray[blueValue-1][wi*3] = blue
            self.videoArray[blueValue+1][wi*3] = blue
         
            self.videoArray[greenValue][wi*3-1] = green
            self.videoArray[greenValue][wi*3+1] = green
            self.videoArray[greenValue-1][wi*3] = green
            self.videoArray[greenValue+1][wi*3] = green
         
            self.videoArray[redValue][wi*3-1] = red
            self.videoArray[redValue][wi*3+1] = red
            self.videoArray[redValue-1][wi*3] = red
            self.videoArray[redValue+1][wi*3] = red
         
            return
   
      if len(self.oldDataArray) != 0:                # Clean previous line, write oldData with black color
         numPoints, co = self.oldDataArray.shape
         if (self.multiplier == 1):
            for wi in range(0,numPoints):
               PaintPixels(self, wi, self.oldDataArray, [0,0,0], [0,0,0],[0,0,0] )   
         if (self.multiplier == 3):
            for wi in range(1,numPoints-1):
               PaintPixels(self, wi, self.oldDataArray, [0,0,0], [0,0,0],[0,0,0] )   
         pass   
      
      a = type(DataArray)
      self.blueMin = np.amin(DataArray[:,0])
      self.greenMin = np.amin(DataArray[:,1])
      self.redMin = np.amin(DataArray[:,2])
      self.blueMax = np.amax(DataArray[:,0])
      self.greenMax = np.amax(DataArray[:,1])
      self.redMax = np.amax(DataArray[:,2])
      
      numPoints, co = DataArray.shape           # save current places in  oldData
      self.oldDataArray = DataArray.copy()
#     self.videoArray = self.videoArrayBlack.copy()
      h,w,c = self.videoArray.shape
      m = self.multiplier
      
      if (self.multiplier == 1):
         for wi in range(0,numPoints):
            PaintPixels(self, wi, DataArray,[255,0,220], [0,255,0],[0,0,255])   
      else:
         for wi in range(1,numPoints-1):
            PaintPixels(self, wi, DataArray,[255,0,220], [0,255,0],[0,0,255]) 
      
      strTextToDraw = f'{numPoints} - B: {self.blueMin}-{self.blueMax} G: {self.greenMin}-{self.greenMax} R: {self.redMin}-{self.redMax}'
      self.DrawText(str(strTextToDraw))
      
      self.lockEvent.set()
      
   def TriggerShow(self):
      self.lockEvent.set()
      bRet = win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)

   def Backup(self):
         if (self.bStatusVLA1 or self.bStatusVLA2):
            if (self.oldLineY1ListIndex != -1 or self.oldLineY2ListIndex != -1):                # write old info back to screen.... line erasing
               for hi in range(0,self.windowHeight):
                  if (self.currentVLA == 1):
                     self.videoArray[hi][self.oldLineY1ListIndex] = self.oldLineY1List[hi].copy()
                  if (self.currentVLA == 2):
                     self.videoArray[hi][self.oldLineY2ListIndex] = self.oldLineY2List[hi].copy()
            
            xi = x
            if (self.currentVLA == 1):
               self.xPosVLA1 = xi
               self.oldLineY1List.clear()
            if (self.currentVLA == 2):
               self.xPosVLA2 = xi
               self.oldLineY2List.clear()
            
            for hi in range(0,self.windowHeight):
               if (self.currentVLA == 1):
                  self.oldLineY1List.append(self.videoArray[hi][xi].copy())      # background of the new line - store for erase
                  self.videoArray[hi][xi] = [230,230,230]                       # draw new line with the white color
               if (self.currentVLA == 2):
                  self.oldLineY2List.append(self.videoArray[hi][xi].copy())      # background of the new line - store for erase
                  self.videoArray[hi][xi] = [230,230,230]                       # draw new line with the white color

            if (self.bStatusVLA1 or self.bStatusVLA2):
               if (self.currentVLA == 1):
                  xi = self.oldLineY1ListIndex
                  if self.bDebug:
                     print(f'Restore oldLineIndex: {self.oldLineY1ListIndex}')
                  for hi in range(0,self.windowHeight):
                     self.videoArray[hi][self.oldLineY1ListIndex] = self.oldLineY1List[hi].copy()
                  self.oldLineY1List.clear()
                  self.oldLineY1ListIndex = x
                  xi = x

                  for hi in range(0,self.windowHeight):
                     self.oldLineY1List.append(self.videoArray[hi][xi].copy())
                     self.videoArray[hi][xi] = [230,230,230] 
               if (self.currentVLA == 2):
                  xi = self.oldLineY2ListIndex
                  if self.bDebug:
                     print(f'Restore oldLineIndex: {self.oldLineY2ListIndex}')
                  for hi in range(0,self.windowHeight):
                     self.videoArray[hi][self.oldLineY2ListIndex] = self.oldLineY2List[hi].copy()
                  self.oldLineY2List.clear()
                  self.oldLineY2ListIndex = x
                  xi = x

                  for hi in range(0,self.windowHeight):
                     self.oldLineY2List.append(self.videoArray[hi][xi].copy())
                     self.videoArray[hi][xi] = [230,230,230] 
               
   
