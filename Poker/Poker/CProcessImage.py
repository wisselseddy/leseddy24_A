import cv2
import win32api
import win32gui
import win32con
import os
from CErrorCode import *
import numpy as np
import threading
from time import time_ns

class CProcessImage(object):
   def __init__(self,CParams, ImagePath): 
      self.cParams = CParams
      CParams.processImageHandler = self
      self.errorCode = CErrorCode(CParams)
      self.imagePath = ImagePath
      self.winID = 'ProcessImage'
      self.strWindowTitle = 'Processing'

      self.imgBuf = None
      self.imageHeight = -1
      self.imageWidth = -1
      self.posX = 10
      self.posY = 1024 // 2
      self.bAlive = False
      self.displayThread = None
      self.bFilterState = False     # To switch filter activity on/off
      self.bMouseDown = False
      self.listColors = np.full((640,3),[0,0,0],dtype='uint8')
      self.listColorsQuantity = 0
      self.listIndex = 0
      self.messageTime = 0
      self.rule = None
      self.bReiterate = False
      self.backColor = np.full((3),[0,0,0],dtype='uint8')
      self.bBackColor = False
      self.bBackColorSet = False
      self.processArray = None
      self.cursorType = win32con.IDC_HAND

      self.cursorFile = 'c:\\ejw\\crimac\\crimacCursor.jpg'
      self.cursorImage = cv2.imread(self.cursorFile,cv2.IMREAD_COLOR)
      self.cursorWidth = -1
      self.cursorHeight = -1
      self.cursorChannels = -1
      self.cursorHeight, self.cursorWidth, self.cursorChannel = self.cursorImage.shape
      self.processWaitKey = 30
      self.hwnd = -1
#      self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strWindowTitle)   # This does not exist yet!!!!
      

      retB = os.path.exists(ImagePath)       # return True if file exists
      if (not retB):
         print( self.errorCode.HandleError( retB))                          # error File is not existing
      pass
   
   def MouseCB(self, action, x, y, flags, *userdata):
#      win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_HAND))
      if (x > self.imageWidth-1 or y > self.imageHeight-1 or x < 0 or y < 0):
         return
     
      if action == cv2.EVENT_LBUTTONDOWN:
         self.listColors = np.full((640,3),[0,0,0],dtype='uint8')
         self.backColor = np.full((3),[0,0,0],dtype='uint8')
         if (self.bBackColor):
            self.backColor[0] = self.videoArray[y][x]
            self.bBackColor = False
            self.bBackColorSet = True
            print(f'Backcolor is set to {self.backColor}\nCommand: ',end='')
            return
         
         self.bMouseDown = True
         self.listIndex = 0
         self.listColors[self.listIndex] = self.videoArray[y][x]
         self.processWaitKey = 0
#         self.listColors = []
#         self.listColors.append(self.videoArray[y][x])
#         self.listColorsQuantity = 1
         if (self.cParams.analysHandler != None):
            self.cParams.analysHandler.ClearPicture()
         self.messageTime = time_ns()
         pass
      
      if action == cv2.EVENT_LBUTTONUP:
#         hwnd = win32gui.FindWindowEx(0, 0, 0, self.winID)
         self.processWaitKey = 1
         bRet = win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
         self.bMouseDown = False
         pass
      
      if action == cv2.EVENT_MOUSEMOVE:
         a,b,c = self.videoArray.shape
         if (self.bMouseDown):
            print(f'C: {self.videoArray[y][x]}',end='')
            if (x > 0 and y > 0 and x < (self.imageWidth - self.cursorWidth ) and y < (self.imageHeight - self.cursorHeight)):
               win32api.SetCursor(0)
               newBG = self.videoArray.copy()
               newBG[y:y+self.cursorHeight,x:x+self.cursorWidth] = self.cursorImage 
               cv2.imshow(self.winID, newBG) 
            else:
               pass
         
         if self.videoArray[y][x].all == self.backColor.all:
            return
         
         if (self.bMouseDown):
            if (self.listIndex < 638):
               self.listIndex += 1
            else:
               self.listIndex = 0
            self.listColors[self.listIndex] = self.videoArray[y][x]
            self.messageTime = time_ns() - self.messageTime
            if (self.messageTime > 50000000):
               
               self.UpdateAnalysWindow(self.listColors)
            pass

   def UpdateAnalysWindow(self, Colors):
      if (self.cParams.analysHandler == None):
         return
      else:
         self.cParams.analysHandler.DrawLine(Colors)      # This must be self Triggering
      pass

   def GetCursorType(self):
      cursorType = win32api.GetCursor()
      print(f'CursorType: {cursorType}')
      
   def SetCursorType(self, StrType):
      if ('HAND') in StrType:
         self.cursorType = win32con.IDC_HAND
      if ('HELP') in StrType:
         self.cursorType = win32con.IDC_HELP
      if ('CROSS') in StrType:
         self.cursorType = win32con.IDC_CROSS
      if ('UPARROW') in StrType:
         self.cursorType = win32con.IDC_UPARROW
      if ('DEFAULT') in StrType:
         self.cursorType = 0
         
      win32api.SetCursor(win32api.LoadCursor(0, self.cursorType))
      
   def ApplyFilter(self, FilterType, FilterRule):
      if (FilterType == 0):
         
         pass
      pass
   
   def KillImage(self):
      self.bAlive = False
      
   def ProcessImage(self):
      self.displayThread = threading.Thread(target=self.DisplayThread,args = (None,))
      self.displayThread.start()
   
   def SetRules(self,Rules):
      self.rule = Rules.copy()
      pass
   
   def Reiterate(self):
      self.bReiterate = True
   
   def SetBackColor(self):
      self.bBackColor = True
   
   def DisplayThread(self,Params):
      
      # Create the main window
      if (not self.bReiterate):
         self.videoArray = cv2.imread(self.imagePath,cv2.IMREAD_COLOR)
#         self.videoArray[0][0][0] = 1                    # to indicate original load
         self.orgVideoArray = self.videoArray.copy()
         
      self.imageHeight, self.imageWidth, self.channels = self.videoArray.shape

      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
      cv2.setWindowTitle(self.winID,self.strWindowTitle)
      cv2.resizeWindow(self.winID, self.imageWidth, self.imageHeight)
      cv2.moveWindow(self.winID,self.posX, self.posY)
      self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strWindowTitle)

      # Set up the mouse handler
      cv2.setMouseCallback(self.winID,self.MouseCB)
      
      self.bAlive = True
      
      while self.bAlive:
         if self.bFilterState:
            self.Filter()
            self.bFilterState = False
            print('Filter implemented')
         cv2.imshow(self.winID, self.videoArray) 
         key = cv2.waitKey(self.processWaitKey)
         if key == 27 & 0xff:
            break
      
      cv2.destroyWindow(self.winID)  
      print('CProcessingImage Finished')
      
   
   def ClearPicture(self):
      self.videoArray = np.full((self.height,self.width, self.channel), [0,0,0], dtype='int8')
      return
   
   def ReloadImage(self):
      self.videoArray = cv2.imread(self.imagePath,cv2.IMREAD_COLOR)
#      self.videoArray[0][0][1] = 1                       # to indicate reload

   def DetectBorder(self):
      self.oldVideoArray = self.videoArray.copy()
      h,w,c = self.videoArray.shape
      self.processArray = np.full((h,w,c),[0,0,0],dtype='int8')
      
      for hi in range(1,h - 1):
         print(f'hi: {hi}')
         for wi in range(1,w - 1):
            retValue = 0
            shift = 0x01
            for hx in (-1,0,1):
               for wx in (-1,0,1):
                  tmpValue = 0
                  tmpValue += self.videoArray[hi+hx][wi+wx][0]
                  tmpValue += self.videoArray[hi+hx][wi+wx][1]
                  tmpValue += self.videoArray[hi+hx][wi+wx][2]
                  if (tmpValue < 750): 
                     retValue |= shift
                  shift = shift << 1
                  pass
               pass
            if retValue == 0xff: 
               retValue = 0
            self.processArray[hi][wi][0] = retValue
            self.processArray[hi][wi][1] = retValue
            self.processArray[hi][wi][2] = retValue
            pass
         pass
      self.videoArray = self.processArray.copy()
      pass

   def FilterState(self, BoolState):
      self.bFilterState = BoolState
   
   def Filter(self):
      if (self.bReiterate):
         self.bReiterate = False
         self.orgvideoArray = self.videoArray
         
      self.oldVideoArray = self.videoArray.copy()
      counter = 0    

      h,w,c = self.orgVideoArray.shape
      for hi in range(h):
         for wi in range(w):
            orgColor = self.orgVideoArray[hi][wi]
            if (orgColor[0] > self.rule[0] and
                orgColor[1] > self.rule[2] and
                orgColor[2] > self.rule[4] and
                orgColor[0] < self.rule[1] and
                orgColor[1] < self.rule[3] and
                orgColor[2] < self.rule[5]):
               self.videoArray[hi][wi] = self.backColor
               counter += 1
      print(f'{counter} points changed.')
      
   def Save(self, StrPathToSave):
      cv2.imwrite(StrPathToSave,self.videoArray)
      print('Image Saved.')
               
      