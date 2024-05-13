from ast import Try
from tokenize import StringPrefix
from types import NoneType
import cv2
import time
import random
import threading
import numpy as np

import win32gui
import win32api
import win32con

from MakeBmp import *
from CParameters import CParameters
from CZoom import CZoom

class CDHandler:
   def __init__(self, WinID, CParams):
      CParams.displayWinID = WinID 
      CParams.displayHandler = self    
      
      self.hwnd = -1
      self.winID = WinID
      self.cParams = CParams
      self.listSlidersMinMaxCur = CParams.getSlidersMinMaxCur()
      self.blueCurrentValue = (self.listSlidersMinMaxCur[0])[2]
      self.greenCurrentValue = (self.listSlidersMinMaxCur[1])[2]
      self.redCurrentValue = (self.listSlidersMinMaxCur[2])[2]
      self.color = [self.blueCurrentValue, self.greenCurrentValue, self.redCurrentValue]
      self.window_width = CParams.display_width
      self.window_height = CParams.display_height
      self.window_posX = CParams.getDisplayPosX()
      self.window_posY = CParams.getDisplayPosY()
      self.blue_background = np.full((self.window_height, self.window_width, 3), self.color, dtype='uint8')
#      self.slider_value = self.blue_color[0]
      self.bDebug = False
      self.bMouseDown = False
      self.bDrawCircle = False
      self.listXDrawCircle = []
      self.listYDrawCircle = []
      self.cParams.videoBuffer = np.full((self.window_height,self.window_width,3),self.color,dtype='uint8')
      self.orgVideoBuffer = self.cParams.videoBuffer.copy()
      self.orgSource3VideoBuffer = None
      self.orgSource4VideoBuffer = None
      self.orgSource3VideoWidth = -1
      self.orgSource3VideoHeight = -1
      self.orgSource4VideoWidth = -1
      self.orgSource4VideoHeight = -1
      self.bVideoBufferValid = False
      self.bExternBuf = False
      self.bDVLActive = False
      self.bDHLActive = False
      self.lineIndex = -1
      self.oldlineIndex = -1
      self.whiteLine = np.full((self.window_width,3),[255,255,255],dtype='uint8')
      self.blackLine = np.full((self.window_width,3),[0,0,0],dtype='uint8')
      self.hDashLineIndex = -1
      self.oldHDashLineIndex = -1
      self.vDashLineIndex = -1
      self.oldVDashLineIndex = -1

      self.hDashLine = np.full((self.window_width,3),[0,0,0],dtype='uint8')
      self.hDashLine[0:self.window_width - 5:4] = [255,255,255]
      self.hDashLine[1:self.window_width - 5:4] = [255,255,255]
      self.vDashLine = np.full((self.window_height,3),[0,0,0],dtype='uint8')
      self.vDashLine[0:self.window_height:4] = [255,255,255]
      self.vDashLine[1:self.window_height:4] = [255,255,255]

      self.oldLineHContents = np.full((self.window_width,3),[0,0,0],dtype='uint8')
      self.oldLineVContents = np.full((self.window_height,3),[0,0,0],dtype='uint8')
      self.bOldLineType = -1        # -1 no valid line
                                    # 0 valid H line
                                    # 1 valid V line
      self.strWindowTitle = 'Display Handler'
      # Handling Frame Grabbing
      self.bFrameGrabbing = False
      self.bSingleFrameGrabbing = False
      self.bRecording = False
      self.bRecordingActive = False
      self.strFramePath = "C:\\pc2324\\Images\\Frames\\"
      self.frameIndex = 0
      self.bLoadedFrameActive = False
      self.bFrameDiffs = False
      self.strLoadedFramePath = ''
      self.strPreviousLoadedFramePath = ''
      self.bFrameRepeat = False
      self.bSaveSingleImage = False
      self.bResetMouseCB = False
      self.bRecording = False
      self.bContinueActive = False
      self.strTitleInfo = ''
      self.rectStartDimension = ((-1,-1))
      self.rectEndDimension = ((-1,-1))
      self.bRectDone = False
      
      self.bRectActive = False 
      self.waitKeyTime = 10
      self.wantedWaitKeyTime = 10
      self.debugValue = 0
      self.roi = None
      self.bZoomActive = False
      self.oldKeyTime = -1
      self.oldKeyText = -1
      
      self.bDiffActive = False
      self.bDiffSActive = False
      self.firstFrameIndex = -1
      self.secondFrameIndex = -1
      self.diffFirstFrameIndex = -1
      self.diffSecondFrameIndex = -1
      self.diffFirstFramePath = ''
      self.diffSecondFramePath = ''
      self.diffCounter = 0
      self.bDiffS1Active = True
      self.bDiffS2Active = False
      self.bCopyFromMaster = False
      self.bShowFrame = True
      
#      self.strFrameName = f'Frame-{self.frameIndex}.bmp'
      
      # Create the main window
      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
      cv2.resizeWindow(self.winID, self.window_width, self.window_height)
      cv2.setWindowTitle(self.winID,self.strWindowTitle)
      cv2.moveWindow(self.winID,self.window_posX, self.window_posY)
      self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strWindowTitle)
                   
      # Adjust threads for cv2
      cv2.setNumThreads(15)

#      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)

#      cv2.resizeWindow(self.winID, self.window_width, self.window_height)
#      cv2.moveWindow(self.winID,self.window_posX, self.window_posY)

      # Set up the mouse handler
      cv2.setMouseCallback(self.winID,self.mouseCB)

      # Create a trackbar for the slider
      cv2.imshow(self.winID, self.blue_background) 
      self.waitKeyTime = self.wantedWaitKeyTime
      key = cv2.waitKey(self.waitKeyTime)
      if key == 27 & 0xff:
          pass
      #cv2.createTrackbar("Blue Channel", slider_window_name, self.slider_value, 255, self.update_blue_channel)
      self.zoomID = 0
      
   def ResizeDisplayHandler(self,Width,Height):    # adapt display window on other then 640 * 480
      self.cParams.ReSize(Width,Height)
      self.window_width = self.cParams.display_width = Width
      self.window_height = self.cParams.display_height = Height
      self.blue_background = np.full((self.window_height, self.window_width, 3), self.color, dtype='uint8')
      self.cParams.videoBuffer = np.full((self.window_height,self.window_width,3),self.color,dtype='uint8')
      self.orgVideoBuffer = self.cParams.videoBuffer.copy()
      self.whiteLine = np.full((self.window_width,3),[255,255,255],dtype='uint8')
      self.blackLine = np.full((self.window_width,3),[0,0,0],dtype='uint8')
      self.hDashLine = np.full((self.window_width,3),[0,0,0],dtype='uint8')
      self.hDashLine[0:self.window_width - 5:4] = [255,255,255]
      self.hDashLine[1:self.window_width - 5:4] = [255,255,255]
      self.vDashLine = np.full((self.window_height,3),[0,0,0],dtype='uint8')
      self.vDashLine[0:self.window_height:4] = [255,255,255]
      self.vDashLine[1:self.window_height:4] = [255,255,255]

      self.oldLineHContents = np.full((self.window_width,3),[0,0,0],dtype='uint8')
      self.oldLineVContents = np.full((self.window_height,3),[0,0,0],dtype='uint8')
      cv2.resizeWindow(self.winID, self.window_width, self.window_height)   #849*614
      self.cParams.sliderHandler.sliderWidth = MakeBmp(self.cParams.getSliderQuantity(),self.window_height)
#      self.cParams.ReSize()
      time.sleep(0.100)
      self.cParams.sliderHandler.ResizeSliders()
      time.sleep(0.100)
      self.cParams.changePositionPythonTerminal()
      cv2.moveWindow(self.cParams.sliderHandler.winID, 
                     Width + 20,
                     self.cParams.sliderHandler.YPos)
      
      pass
   
   def TriggerDisplayHandler(self):
      win32api.PostMessage(self.cParams.displayHandler.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
      return
   
   def mouseCB(self, action, x, y, flags, *userdata):
#      print(self.waitKeyTime)
      self.strTitleInfo = f' Width: {x}' + f' Height: {y} FrameID: {self.frameIndex}'
      if ( y > (self.window_height - 1) or y < 0):
         return
      if ( x > (self.window_width - 1) or x < 0):
         return
      
      if action == cv2.EVENT_RBUTTONDOWN:
         self.oldHDashLineIndex = -1
         self.hDashLineIndex = -1
         self.oldVDashLineIndex = -1
         self.vDashLineIndex = -1
         self.oldDashLineType = -1                    # undefine old dashline type 0: hor 1 = vert -1:not avail.
         self.bDHLActive = False
         self.bDVLActive = False
         self.frameIndex = 0
         self.bRectActive = False
         self.bContinueActive = False
         pass
      
      if action == cv2.EVENT_LBUTTONDOWN:
         self.bMouseDown = True
         self.wantedWaitKeyTime = 0
         self.debugValue |= 0x01
         if (True): 
            if self.bLoadedFrameActive and self.bContinueActive:
               if (self.bContinueActive):    # Prepare path to next frame
                  indexChar = self.strLoadedFramePath.rfind('_')
                  strIndex = self.strLoadedFramePath[indexChar+1:-4]
                  self.frameIndex = int(strIndex) + 1
                  self.strLoadedFramePath = self.strLoadedFramePath[0:indexChar+1] + f'{self.frameIndex}.bmp'
#                  self.bContinueActive = False
                  return
               
            if (self.cParams.commandHandler.bSaveSingleImage):
               self.bSaveSingleImage = True
               return
            
            if self.cParams.commandHandler.bRecording:
               self.bRecording = not self.bRecording
               
            if (self.bDiffActive):    
               if self.bDHLActive:
                  self.hDashLineIndex = y
                  self.vDashLineIndex = -1
               if self.bDVLActive:
                  self.hDashLineIndex = -1
                  self.vDashLineIndex = x
               pass
            if self.bRectActive:
               self.orgVideoBuffer = self.cParams.videoBuffer.copy()
               self.rectStartDimension = (x,y)
               cv2.imshow(self.winID, self.orgVideoBuffer) 

         if self.bDebug:
             print('MouseCallback-LButtonDown')
                  
         self.debugValue &= 0xFE
         return    
      if action == cv2.EVENT_LBUTTONUP:
         self.debugValue |= 0x02
         if self.bRectActive and self.bMouseDown:
            self.bMouseDown = False
            if self.bRectActive:
               self.rectEndDimension = ((x,y))
               x1 = self.rectStartDimension[0]
               y1 = self.rectStartDimension[1]
               x2 = self.rectEndDimension[0]
               y2 = self.rectEndDimension[1]
               self.roi = self.orgVideoBuffer[y1:y2,x1:x2]
               h,w,c = self.roi.shape
#               roi = np.array(contents)
#               hhh = contents[y1:y2,x1:x2]
#               roi = self.orgVideoBuffer[x1:y1,x2:y2]
#               h,w,c = roi.shape
               self.bZoomActive = True
               cv2.rectangle(self.orgVideoBuffer,self.rectStartDimension, self.rectEndDimension,[0,0,0],2,0)
               self.wantedWaitKeyTime = 9  
               print('zoom asked')
               cv2.imshow(self.winID, self.orgVideoBuffer)
               win32api.PostMessage(self.cParams.displayHandler.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
         if (self.bContinueActive):
            cv2.imshow(self.winID, self.orgVideoBuffer)
            if (self.waitKeyTime == 0):
               win32api.PostMessage(self.cParams.displayHandler.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
                
         if self.bDebug:
            print('MouseCallback-LButtonUp')

         self.debugValue |= 0xFD

      if action == cv2.EVENT_MOUSEMOVE:
         self.debugValue |= 0x04
         if self.bMouseDown:
            if self.bDHLActive:
               self.hDashLineIndex = y
               cv2.imshow(self.winID, self.orgVideoBuffer)
            if self.bDVLActive:
               self.vDashLineIndex = x
               cv2.imshow(self.winID, self.orgVideoBuffer)
            if self.bRectActive:
               self.rectEndDimension = ((x,y))
               self.orgVideoBuffer = self.cParams.videoBuffer.copy()
               cv2.rectangle(self.orgVideoBuffer,self.rectStartDimension, self.rectEndDimension,[230,230,230],2,0)
               cv2.imshow(self.winID, self.orgVideoBuffer)
            pass
         self.debugValue &= 0xFB 
#      print(f'DebugValue: {self.debugValue}')
      self.debugValue = 0x00
      
   def Zooming(self,CParams,ZoomID,Roi):
      cZoom = CZoom(CParams,ZoomID,Roi)
      cZoom.Run()
      
   def SetExternalBuffer(self, Boolean):
      self.bExternBuf = Boolean
      pass
           
   def drawCircle(self, ListX, ListY):
      self.bDrawCircle = True
      self.listXDrawCircle = ListX
      self.listYDrawCircle = ListY
      pass
   
   def RedefineVideoBuffer(self):
      self.blueCurrentValue = (self.cParams.listSlidersMinMaxCur[0])[2]
      self.greenCurrentValue = (self.listSlidersMinMaxCur[1])[2]
      self.redCurrentValue = (self.listSlidersMinMaxCur[2])[2]
      self.cParams.videoBuffer = np.full((self.window_height,self.window_width,3),[self.blueCurrentValue,self.greenCurrentValue,self.redCurrentValue],dtype='uint8')
   
   def SetBufImg(self,StrA,Width,Height):
      strLength = len(StrA)
      numBytes = Width * Height * 3
      countNulls = StrA.count(b'\x00')
      pass
   
   def DHL(self, LineIndex):
      if (self.cParams.analysHandler.bAlive):
         # Draw white line in videodisplay
         h,w,c = self.cParams.videoBuffer.shape
         analysHLine = self.cParams.videoBuffer[LineIndex].copy()
         for wi in range(w):
#            analysHLine[0][wi] = self.cParams.videoBuffer[LineIndex][wi]
            self.cParams.videoBuffer[LineIndex][wi] = [255,255,255]
         self.cParams.analysHandler.DrawLine(analysHLine)
         
   def DVL(self, LineIndex):
      # Draw white line in videodisplay
      if (self.cParams.analysHandler.bAlive):
         h,w,c = self.cParams.videoBuffer.shape
         analysVLine = np.full((h,3),[0,0,0],dtype='uint8')
         for hi in range(h):
            analysVLine[hi] = self.cParams.videoBuffer[hi][LineIndex]
            self.cParams.videoBuffer[hi][LineIndex] = [255,255,255]
         self.cParams.analysHandler.DrawLine(analysVLine)
      
   def SetGraphicsBuffer(self,StrA,Width,Height):
      self.orgSource4VideoBuffer = StrA
      self.orgSource4VideoWidth = Width
      self.orgSource4VideoHeight = Height
      self.orgSource3VideoWidth = -1
      self.orgSource3VideoHeight = -1
      self.orgSource3VideoBuffer = None
      lenData = len(StrA)
      blueStr = StrA[::4]
      greenStr = StrA[1::4]
      redStr = StrA[2::4]
      aStr = StrA[3::4]
      
      minBlue,maxBlue,blueCur = self.listSlidersMinMaxCur[0]
      minGreen,maxGreen,greenCur = self.listSlidersMinMaxCur[1]
      minRed,maxRed,redCur = self.listSlidersMinMaxCur[2]

      newArray = np.full((self.window_height,self.window_width,3),[0,0,0],dtype = 'uint8')
      indexNumber = 0
      for h in range(self.window_height):
         for w in range(self.window_width):
            
            if (blueStr[indexNumber]  >= blueCur): 
               newArray[h][w][0] = blueCur
            else:
               newArray[h][w][0] = blueStr[indexNumber]
            if (greenStr[indexNumber]  >= greenCur): 
               newArray[h][w][1] = greenCur
            else:
               newArray[h][w][1] = greenStr[indexNumber]
            if (redStr[indexNumber] >= redCur):
               newArray[h][w][2] = redCur
            else:
#               newArray[h][w][2] = greenStr[indexNumber]
               newArray[h][w][2] = redStr[indexNumber]
               
            indexNumber += 1
            if (indexNumber > (self.window_width - 1)):
               pass
         indexNumber += Width - self.window_width  
      self.cParams.videoBuffer = newArray
      self.bCopyFromMaster = True
#      self.cParams.bPictureAlive = True
      self.bShowFrame = True

   def ProcessOrgContentsVideoBuffer(self):
      h,w,c = self.cParams.videoBuffer.shape
      if (self.orgSource4VideoBuffer == None):
         self.SetGraphicsBuffer2(self.orgSource3VideoBuffer,
                                 self.orgSource3VideoWidth,
                                 self.orgSource3VideoHeight)
      else:
         self.SetGraphicsBuffer(self.orgSource4VideoBuffer,
                                 self.orgSource4VideoWidth,
                                 self.orgSource4VideoHeight)

   def SetGraphicsBuffer2(self,StrA,Width,Height):
      self.orgSource3VideoBuffer = StrA
      self.orgSource4VideoBuffer = None
      self.orgSource3VideoWidth = Width
      self.orgSource3VideoHeight = Height
      self.orgSource4VideoWidth = -1
      self.orgSource4VideoHeight = -1
      
      blueStr = StrA[::3]
      greenStr = StrA[1::3]
      redStr = StrA[2::3]
      
      minBlue,maxBlue,blueCur = self.listSlidersMinMaxCur[0]
      minGreen,maxGreen,greenCur = self.listSlidersMinMaxCur[1]
      minRed,maxRed,redCur = self.listSlidersMinMaxCur[2]

      newArray = np.full((self.window_height,self.window_width,3),[0,0,0],dtype = 'uint8')
      indexNumber = 0
      for h in range(self.window_height):
         for w in range(self.window_width):
            
            if (blueStr[indexNumber]  >= blueCur): 
               newArray[h][w][0] = blueCur
            else:
               newArray[h][w][0] = blueStr[indexNumber]
            if (greenStr[indexNumber]  >= greenCur): 
               newArray[h][w][1] = greenCur
            else:
               newArray[h][w][1] = greenStr[indexNumber]
            if (redStr[indexNumber] >= redCur):
               newArray[h][w][2] = redCur
            else:
               newArray[h][w][2] = redStr[indexNumber]
               
            indexNumber += 1
            if (indexNumber > (self.window_width - 1)):
               pass
         indexNumber += Width - self.window_width  
      self.cParams.videoBuffer = newArray
      self.cParams.bPictureAlive = True
   
   def setBuf1(self, Buf, Height,Width):
      minBlue,maxBlue,blueCur = self.listSlidersMinMaxCur[0]
      minGreen,maxGreen,greenCur = self.listSlidersMinMaxCur[1]
      minRed,maxRed,redCur = self.listSlidersMinMaxCur[2]
      pass
   
   def setBuf(self,Buf, Height, Width):
      if (self.cParams.bRGBFilter):
         minBlue,maxBlue,blueCur = self.listSlidersMinMaxCur[0]
         minGreen,maxGreen,greenCur = self.listSlidersMinMaxCur[1]
         minRed,maxRed,redCur = self.listSlidersMinMaxCur[2]
      
         for hi in range(Height):
            for wi in range(Width):
               if (Buf[hi][wi][0] > blueCur):
                  Buf[hi][wi][0] = blueCur
               if (Buf[hi][wi][1] > greenCur):
                  Buf[hi][wi][1] = greenCur
               if (Buf[hi][wi][2] > redCur):
                  Buf[hi][wi][2] = redCur
                  
      self.cParams.videoBuffer = Buf
         
   def ListFrames(self):
      pass
   
   def SaveFrame(self):
      self.frameIndex += 1
      strFileName = self.strFramePath + f'Frame_{self.frameIndex}.bmp'
      cv2.imwrite(strFileName,self.cParams.videoBuffer)
#      print(f'\nImage Saved as {strFileName}\nCommand: ')
      pass
   
   def PrintKey(self,KeyTime,Text):
      return
      if (self.oldKeyTime != KeyTime or self.oldKeyText != Text):
         print(f'{Text} KeyTime: {KeyTime}')
         self.oldKeyTime = KeyTime
         self.oldKeyText = Text  
         
   def run(self):
      oldStrLoadedPath = ''
      faultCounter = 0
      self.bCopyFromMaster = True
      while self.cParams.bAlive:
         self.debugValue |= 0x08
# reset up the mouse handler
         if (self.bResetMouseCB):
            cv2.setMouseCallback(self.winID,self.mouseCB)
            print('Mouse Callback resetted')
            self.bResetMouseCB = False
            self.debugValue |= 0x10
         if (self.cParams.bCameraAlive or \
             self.cParams.bPictureAlive or \
             self.bLoadedFrameActive or \
             self.bFrameGrabbing or \
             self.bShowFrame or \
             self.bDiffSActive or \
             self.bCopyFromMaster):
            
            if self.bCopyFromMaster:
               self.orgVideoBuffer = self.cParams.videoBuffer
               self.bCopyFromMaster = False
            if (self.cParams.commandHandler.bSaveSingleImage or self.cParams.bRecording):
               if (self.bSaveSingleImage):
                  self.SaveFrame()
                  self.bSaveSingleImage = False
                  cv2.imshow(self.winID, self.cParams.videoBuffer)
                  self.waitKeyTime = self.wantedWaitKeyTime
                  key = cv2.waitKey(self.waitKeyTime) & 0xff
                  continue

               elif self.bRecording:
                  self.orgVideoBuffer = self.cParams.videoBuffer.copy()
                  cv2.circle(self.orgVideoBuffer,(50,50),20,[0,0,255],-1)
                  
                  strFileName = self.strFramePath + f'Frame_{self.frameIndex+1}.bmp'
                  cv2.putText(self.orgVideoBuffer, strFileName, 
                     (20,50), 
                     cv2.FONT_HERSHEY_SIMPLEX,
                     0.8,
                     (220,220,220),
                     2,
                     1)

                  self.SaveFrame()
                  cv2.imshow(self.winID, self.orgVideoBuffer)
                  self.waitKeyTime = self.wantedWaitKeyTime
                  key = cv2.waitKey(self.waitKeyTime) & 0xff
                  continue
#               elif not self.bRecording:
#                  orgVideoBuffer = self.cParams.videoBuffer.copy()
#                  cv2.circle(self.orgVideoBuffer,(50,50),20,[0,255,0],3)
#                  cv2.imshow(self.winID, self.orgVideoBuffer)
#                  self.waitKeyTime = self.wantedWaitKeyTime
#                  key = cv2.waitKey(self.waitKeyTime) & 0xff
            elif (self.bLoadedFrameActive):   # filter works on loaded, has already been done on live
               oldStrLoadedPath = self.strLoadedFramePath     # ejw just changed          
               globalDisplayBuffer = cv2.imread(self.strLoadedFramePath)
               self.cParams.videoBuffer = globalDisplayBuffer
               if self.cParams.bRGBFilter1 or self.cParams.bRGBFilter2:
                  blueCur = (self.cParams.getSlidersMinMaxCur())[0][2]
                  greenCur =  (self.cParams.getSlidersMinMaxCur())[1][2]
                  redCur =  (self.cParams.getSlidersMinMaxCur())[2][2]
                  (B,G,R) = cv2.split(globalDisplayBuffer)
                  if self.cParams.bRGBFilter1:
                     R[R > redCur] = redCur
                     G[G > greenCur] = greenCur
                     B[B > blueCur] = blueCur
                  if self.cParams.bRGBFilter2:
                     R[R < redCur] = 0
                     G[G < greenCur] = 0
                     B[B < blueCur] = 0
                  self.orgVideoBuffer = cv2.merge([B,G,R])
               else:
                  self.orgVideoBuffer = globalDisplayBuffer
#               if self.bRectActive and self.bMouseDown and self.bRectDone: 
#                  cv2.rectangle(self.orgVideoBuffer,self.rectStartDimension, self.rectEndDimension,[0,0,0],2,0)
#                  return
              
# Analysis start here for any picture (live of frame loaded)
            self.debugValue |= 0x20
            if (not type(self.cParams.videoBuffer) == type(NoneType())):
               if (self.hDashLineIndex != -1):
                  self.orgHDashLine = self.cParams.videoBuffer[self.hDashLineIndex].copy()
                  self.orgVideoBuffer[self.hDashLineIndex] = self.hDashLine
                  if (self.cParams.analysHandler != None):
                     try:
                        self.cParams.analysHandler.DrawLine(self.orgHDashLine)
                     except:
                        print('error 1')
               if (self.vDashLineIndex != -1):
                  for wi in range(0,self.window_height):
                     self.oldLineVContents[wi] = self.cParams.videoBuffer[wi][self.vDashLineIndex]
                     self.orgVideoBuffer[wi][self.vDashLineIndex] = self.vDashLine[wi]
#                     self.orgVideoBuffer[wi][self.vDashLineIndex] = [127,127,127]
               if (self.cParams.analysHandler != None):
                  try:
                     self.cParams.analysHandler.DrawLine(self.oldLineVContents)   # only part of width
                  except:
                     print('error 1')
               if self.bZoomActive:
                  print('zoom given')
                  self.cParams.zoomHandler.CreateZoom(self.roi)
#                  zoomThread = threading.Thread(target=self.Zooming,args = (self.cParams,self.zoomID,self.roi))
#                  zoomThread.start()
                  self.bZoomActive = False
                  continue
               
               if self.bDiffActive:
                  indexChar = self.strLoadedFramePath.rfind('_')
                  self.frameIndex = int(self.strLoadedFramePath[indexChar+1:-4])
                  self.strPreviousLoadedFramePath = self.strLoadedFramePath[0:indexChar] + f'_{self.frameIndex}.bmp'
                  self.frameIndex += 1
                  self.strLoadedFramePath = self.strLoadedFramePath[0:indexChar] + f'_{self.frameIndex}.bmp'
                  self.strTitleInfo = f' diff: {self.frameIndex} and {self.frameIndex+1}' 
                  currentBuffer = cv2.imread(self.strLoadedFramePath)
                  previousBuffer = globalDisplayBuffer.copy()
                  (Bs,Gs,Rs) = cv2.split(currentBuffer)
                  (Bp,Gp,Rp) = cv2.split(previousBuffer)
                  if (Rs[:] >= Rp[:]):
                     Rs[:] -= Rp[:]
                  Gs[:] -= Gp[:]
                  Bs[:] -= Bp[:]
                  self.orgVideoBuffer = cv2.merge([Bs,Gs,Rs])
               if (self.bDiffSActive):
                  self.diffFirstFramePath = self.strLoadedFramePath + f'Frame_{self.diffFirstFrameIndex}.bmp'
                  self.diffSecondFramePath = self.strLoadedFramePath + f'Frame_{self.diffSecondFrameIndex}.bmp'
                  self.strTitleInfo = f' diff: {self.diffFirstFrameIndex} and {self.diffSecondFrameIndex}'
                  firstBuffer = cv2.imread(self.diffFirstFramePath)
                  secondBuffer = cv2.imread(self.diffSecondFramePath)
                  # check if files exists()
                  (Bs,Gs,Rs) = cv2.split(firstBuffer)                 
                  (BBs,GGs,RRs) = cv2.split(firstBuffer)                 
                  (Bp,Gp,Rp) = cv2.split(secondBuffer)
                  (BBp,GGp,RRp) = cv2.split(secondBuffer)
                  self.diffCounter = 0
                  Rs[:] -= Rp[:]
                  Gs[:] -= Gp[:]
                  Bs[:] -= Bp[:]
                  for i in Rs[Rs>0]:
                     self.diffCounter += 1
                  for i in Gs[Gs>0]:
                     self.diffCounter += 1
                  for i in Bs[Bs>0]:
                     self.diffCounter += 1
                  if self.bDiffS1Active:
                     Rs[Rs>0] = RRs[Rs>0]
                     Gs[Rs>0] = GGs[Rs>0]
                     Bs[Rs>0] = BBs[Rs>0] 
                     self.orgVideoBuffer = cv2.merge([Bs,Gs,Rs]) 
                     self.cParams.videoBuffer = self.orgVideoBuffer.copy()
                  if self.bDiffS2Active:
                     Rp[:] -= RRs[:]
                     Gp[:] -= GGs[:]
                     Bp[:] -= BBs[:]
                     Rp[Rs>0] = RRp[Rs>0]
                     Gp[Gs>0] = GGp[Gs>0]
                     Bp[Bs>0] = BBp[Bs>0] 
                     self.orgVideoBuffer = cv2.merge([Bp,Gp,Rp]) 
                     self.cParams.videoBuffer = self.orgVideoBuffer.copy()
                  self.bDiffSActive = False
                  self.bShowFrame = True
#                  u,v,w = self.orgVideoBuffer.shape
#                  for ui in range(u):
#                     for vi in range(v):
#                        if self.orgVideoBuffer[ui][vi].any != np.array([0,0,0]).any:
#                           self.diffCounter += 1
                  pass
               if self.bShowFrame:
                  cv2.imshow(self.winID, self.orgVideoBuffer)
                  self.strTitleInfo = f' diff: {self.firstFrameIndex} and {self.secondFrameIndex} DiffCounter: {self.diffCounter}'
                  cv2.setWindowTitle(self.winID,'Display Handler ' + self.strTitleInfo)
                  self.waitKeyTime = self.wantedWaitKeyTime
#               print(f'{self.waitKeyTime}: before')
                  key = cv2.waitKey(self.waitKeyTime) & 0xff      # wait key main1
                  self.strTitleInfo = f' diff: {self.firstFrameIndex} and {self.secondFrameIndex} DiffCounter: {self.diffCounter}'
#               self.PrintKey(self.waitKeyTime,'after')
                  if (self.waitKeyTime == 0 or self.waitKeyTime == 9 ):
#                  self.waitKeyTime = 10
                     self.debugValue = 0
                  if key == 27:
                     break
               else:
                  faultCounter += 1
               continue
         self.debugValue |= 0x40
         width = self.window_width
         height = self.window_height
         self.blueCurrentValue = self.cParams.getBlueCurrentValue()
         self.greenCurrentValue = self.cParams.getGreenCurrentValue()
         self.redCurrentValue = self.cParams.getRedCurrentValue()

         self.blue_background = np.full((height,width,3),
                                        [self.blueCurrentValue,
                                         self.greenCurrentValue,
                                         self.redCurrentValue],
                                        dtype='uint8')
         
         if (self.bDrawCircle):
            centerXCircle = width / 2
            centerYCircle = height / 2

            for i in range(len(self.listXDrawCircle)):      # X data must have the same length as the Y Data
               drawx = (self.listXDrawCircle[i]) + centerXCircle
               typ = type(self.listXDrawCircle)
               drawy = (self.listYDrawCircle[i]) + centerYCircle
               x = int(drawx)
               y = int(drawy)
               self.blue_background[y][x] = [0,0,0]
               
         cv2.imshow(self.winID, self.blue_background) 
         cv2.setWindowTitle(self.winID,'Display Handler ' + self.strTitleInfo)         
         key = cv2.waitKey(self.waitKeyTime) & 0xff
         if key == 27:
            break
      self.debugValue &= 0xFF
      cv2.destroyWindow(self.winID)
      print('CDHandler module stopped!!!')
