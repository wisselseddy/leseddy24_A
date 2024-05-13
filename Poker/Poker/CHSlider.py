import cv2
import numpy
import time
from MakeBmp import *
from CParameters import CParameters
import win32gui
import win32api
import win32con

class CHSlider(object):
   def __init__(self, Tl, CParams):
      self.cParams = CParams
      self.listSlidersNames = CParams.getSlidersNames()
      self.listSlidersColors = CParams.getSlidersColors()
      self.listSlidersMinMaxCur = CParams.getSlidersMinMaxCur()
      self.bAlive = False
      self.bDebug = False
      self.quantity = len(self.listSlidersNames)
      self.winID = 'CHSlider'
      self.strWindowTitle = 'Sliders'
      self.waitKeyValue = 1
      self.selected = -1
      self.color = [0, 0, 0]
      self.XPos = CParams.slider_posX
      self.YPos = CParams.slider_posY
      self.bMouseDown = False
      self.background = cv2.imread("C:\pc2324\Images\AutoSliderImg.bmp")
      self.orgBackground = cv2.imread("C:\pc2324\Images\AutoSliderImg.bmp")
      self.sliderWidth = self.quantity * 11 + 10
      CParams.setSliderWidth(self.sliderWidth)
      hBackground, wBackground, channel = self.background.shape
      self.bActivateTriggerWindows = False
      CParams.sliderHandler = self

      self.hwnd = -1                      # only declaration, does not exist currently
      self.bDebugIn0 = False
# Make blocks
      sizeHeight = hBackground - 20
      
      for q in range(0,self.quantity):
         sliderValues = self.listSlidersMinMaxCur[q]
         sizeValue = sliderValues[1] - sliderValues[0] + 1
         scaleValueUnit = float(sizeHeight) / float(sizeValue)
         cPointY = int (float(sliderValues[2]) * scaleValueUnit)
         cPointX = q * 11 + 10
      
         for y in range (cPointY - 5, cPointY + 5):
            for x in range(cPointX - 5, cPointX + 5):
               self.background[y][x][0] = 200 + q
               self.background[y][x][1] = 0
               self.background[y][x][2] = 0
      cv2.namedWindow(self.winID, cv2.WINDOW_AUTOSIZE)
      cv2.setWindowTitle(self.winID, self.strWindowTitle)
#      cv2.namedWindow('CSlider', cv2.WINDOW_NORMAL | cv2.CV_WINDOW_AUTOSIZE)
#      cv2.resizeWindow('CSlider',  30, self.height)

      cv2.moveWindow(self.winID, self.cParams.slider_posX, self.cParams.slider_posY)
      cv2.resizeWindow(self.winID,self.cParams.sliderHandler.sliderWidth,self.cParams.displayHandler.window_height)
      cv2.setMouseCallback(self.winID,self.mouseCB)
      self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strWindowTitle)
      cv2.imshow(self.winID, self.background)
         
#        self.onChange1(0)
      key = cv2.waitKey(1) & 0xff
      if key == 27:
         cv2.destroyWindow(self.winID)
   
   def ResizeSliders(self):
      self.background = cv2.imread("C:\\pc2324\\Images\\AutoSliderImg.bmp")
      self.orgBackground = cv2.imread("C:\\pc2324\\Images\\AutoSliderImg.bmp")
      hBackground, wBackground, channel = self.background.shape
      sizeHeight = hBackground - 20
      
      for q in range(0,self.quantity):
         sliderValues = self.listSlidersMinMaxCur[q]
         sizeValue = sliderValues[1] - sliderValues[0] + 1
         scaleValueUnit = float(sizeHeight) / float(sizeValue)
         cPointY = int (float(sliderValues[2]) * scaleValueUnit)
         cPointX = q * 11 + 10
      
         for y in range (cPointY - 5, cPointY + 5):
            for x in range(cPointX - 5, cPointX + 5):
               self.background[y][x][0] = 200 + q
               self.background[y][x][1] = 0
               self.background[y][x][2] = 0
      pass

   def killSliders(self):
      self.bAlive = False

# Make blocks
   def MakeBlock(self,):
      hBackground, wBackground, channel = self.background.shape
      sizeHeight = hBackground - 20
      lastx = 0
      for q in range(0,self.quantity):
         currentCenter = self.listSlidersMinMaxCur[q]
         sizeValue = currentCenter[1] - currentCenter[0] + 1
         scaleValueUnit = float(sizeHeight) / float(sizeValue)
         cPointY = int (float(currentCenter[2]) * scaleValueUnit)
         cPointX = q * 11 + 10
         colors = self.cParams.listSlidersColors[q]
         for y in range (cPointY - 5, cPointY + 5):
            for x in range(cPointX - 5, cPointX + 5):
               self.background[y][x][0] = 200 + q
               self.background[y][x][1] = 0
               self.background[y][x][2] = 0
               lastx = x + 10
      pass

   def mouseCB(self, action, x, y, flags, *userdata):
      hBackground, wBackground,channels = self.background.shape
      sizeHeight = hBackground - 20
      self.bGreen = False
      self.bRed = False
      if action == cv2.EVENT_LBUTTONDOWN:
         self.cParams.bSlidersActive = True
         self.cParams.displayHandler.SetExternalBuffer(True)
         self.bMouseDown = True
         self.mark1 = [x, y]
         self.selected = -1
         for u in range(0,self.quantity):
            if self.background[y][x][0] == 200 + u:
               if (self.bDebug):
                  print('Slider %d selected' % (u))
               self.selected = u
         if self.bDebug:
            print('MouseCallback-LButtonDown')
         self.waitKeyValue = 0
         pass
      if action == cv2.EVENT_LBUTTONUP:
         self.cParams.bSlidersActive = False
         self.bMouseDown = False
         self.selected = -1
         if self.bDebug:
            print('MouseCallback-LButtonUp')
#         self.cParams.displayHandler.SetExternalBuffer(False)
         if (self.bActivateTriggerWindows):
            self.cParams.displayHandler.ProcessOrgContentsVideoBuffer()
#            self.cParams.commandHandler.TriggerWindowsFrameCommand()
         self.waitKeyValue = 1         
         cv2.imshow(self.winID, self.background)
         if (self.hwnd == -1 or self.hwnd == 0):
            bDebugA = True
            self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strWindowTitle)
         win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
         pass
      
      if action == cv2.EVENT_MOUSEMOVE:
#         print('mouse-action')

         if self.bMouseDown:
            if (not self.selected == -1):
               if (y < (sizeHeight + 15) and (y > 10)):
                  self.currentValue = y 
#                  self.bChangeDetected = True

                  if (self.bDebug):
                     print('yValue: %d' % (y))

                  u = self.selected
                  currentCenter = self.listSlidersMinMaxCur[u]
                  sizeValue = currentCenter[1] - currentCenter[0] + 1
                  scaleValueUnit = float(sizeHeight) / float(sizeValue)
                  resultValue = int(float(y) / scaleValueUnit)
                  if (resultValue > 255):
                     resultValue = 255
                  (self.listSlidersMinMaxCur[u])[2] = resultValue
                  self.cParams.setBlueCurrentValue((self.listSlidersMinMaxCur[0])[2])
                  self.cParams.setGreenCurrentValue((self.listSlidersMinMaxCur[1])[2])
                  self.cParams.setRedCurrentValue((self.listSlidersMinMaxCur[2])[2])
                  self.background = self.orgBackground.copy()
                  self.MakeBlock()
#                  retValue = self.cParams.commandHandler.TriggerWindowsFrameCommand()
                  cv2.imshow(self.winID, self.background)
                  pass
               pass
            pass
         pass
      pass
   
   def Run(self,CParams):
      val1 = 20
      val2 = 30
      value = 10
  
#      self.currentValue = 200    # For blue color

      CParams.changePositionPythonTerminal()
      CParams.bSlidersActive = True
      self.bDebugIn0 = False
      while CParams.bAlive:
         if CParams.bSlidersActive:

            self.bDebug = CParams.bSliderDebug
            self.background = self.orgBackground.copy()
            self.MakeBlock()
            cv2.imshow(self.winID, self.background)
            self.bDebugIn0 = True
            key = cv2.waitKey(self.waitKeyValue) & 0xff
            self.bDebugIn0 = False
            if key == 27:
               break
         else:
            key = cv2.waitKey(10) & 0xff
            if key == 27:
               break
            
      if not CParams.bAlive:
         cv2.destroyWindow(self.winID)
         print('CHSlider stopped...')
         
   def SetRules(self,Rule):
      (self.listSlidersMinMaxCur[3])[0] = 0
      (self.listSlidersMinMaxCur[3])[1] = 255 
      (self.listSlidersMinMaxCur[3])[2] = Rule[0]
      (self.listSlidersMinMaxCur[4])[0] = 0
      (self.listSlidersMinMaxCur[4])[1] = 255
      (self.listSlidersMinMaxCur[4])[2] = Rule[1]
      (self.listSlidersMinMaxCur[5])[0] = 0
      (self.listSlidersMinMaxCur[5])[1] = 255
      (self.listSlidersMinMaxCur[5])[2] = Rule[2]
      (self.listSlidersMinMaxCur[6])[0] = 0
      (self.listSlidersMinMaxCur[6])[1] = 255
      (self.listSlidersMinMaxCur[6])[2] = Rule[3]
      (self.listSlidersMinMaxCur[7])[0] = 0
      (self.listSlidersMinMaxCur[7])[1] = 255
      (self.listSlidersMinMaxCur[7])[2] = Rule[4]
      (self.listSlidersMinMaxCur[8])[0] = 0
      (self.listSlidersMinMaxCur[8])[1] = 255
      (self.listSlidersMinMaxCur[8])[2] = Rule[5]
      self.MakeBlock()
 








