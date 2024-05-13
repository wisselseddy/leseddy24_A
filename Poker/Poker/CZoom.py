from ast import Pass, excepthandler
from asyncio.windows_events import NULL
from ctypes import windll, wintypes, byref

from cv2.cuda import setBufferPoolConfig
from CParameters import CParameters
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

class CZoom(object):
   SPI_GETWORKAREA = 0x0030
   desktopWorkingArea = wintypes.RECT()
   _ = windll.user32.SystemParametersInfoW(SPI_GETWORKAREA,0,byref(desktopWorkingArea),0)
   left = desktopWorkingArea.left
   top = desktopWorkingArea.top
   right = desktopWorkingArea.right
   bottom = desktopWorkingArea.bottom
   width = right - left
   height =  bottom - top
   global cpY
   cpY = height // 2 + 100
   global cpX
   cpX = width // 2

   def __init__(self,CParams,ZoomID, Roi):
      self.cParams = CParams
      u,v,w = Roi.shape
      if u == 0 and v == 0:
         return
         Roi = np.full((100,100,3),[128,220,250],dtype = 'uint8')
         
#         Roi[45:55,45:55]=[0,0,255]
      self.roi = Roi
      self.newRoi = Roi
      self.windowHeight, self.windowWidth,self.channels = Roi.shape
      self.newWindowHeight, self.newWindowWidth,self.newChannels = Roi.shape
      self.winID = f'ZoomID_{ZoomID}'      
      self.oldWinID = f'ZoomID_{ZoomID}'      
      self.strTitle = f'{ZoomID}-Zoom Window'
      self.lock = threading.Lock()
      self.windowPosX = cpX
      self.windowPosY = cpY
      self.newWindowPosX = cpX
      self.newWindowPosY = cpY
#      self.zoomThread = threading.Thread(target=self.Run,args = (None,))
      self.zoomFactor = 1
      self.hwnd = -1
      self.bSystemAlive = False
      
      self.bMouseDown = False
      self.bRMouseDown = False
     
#      self.zoomThread.run()
#      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
#      cv2.resizeWindow(self.winID, self.windowWidth, self.windowHeight)
#      cv2.setWindowTitle(self.winID,self.strTitle)
#      cv2.moveWindow(self.winID,self.windowPosX, self.windowPosY)       
#      cv2.setWindowTitle(self.winID,self.strTitle)

      self.Run()
      pass
   
   def MouseCB(self, Action, X, Y, Flags, *Userdata):
      self.strTitleInfo = f' Width: {X}' + f' Height: {Y}'
      if ( Y > (self.windowHeight - 1) or Y < 0):
         cv2.setWindowTitle(self.winID,self.strTitle + self.strTitleInfo)
         return
      if ( X > (self.windowWidth - 1) or X < 0):
         cv2.setWindowTitle(self.winID,self.strTitle + self.strTitleInfo)
         return
      if Action == cv2.EVENT_LBUTTONDOWN:
         self.bMouseDown = True
         return
      if Action == cv2.EVENT_LBUTTONUP:
         self.bMouseDown = False
         return
      if Action == cv2.EVENT_MOUSEMOVE:
         return
      if Action == cv2.EVENT_RBUTTONDOWN:
         self.bRMouseDown = True
         return
      if Action == cv2.EVENT_RBUTTONUP:
         self.bRMouseDown = False
         if (X < self.windowWidth // 2):
            if (self.zoomFactor > 1):
               self.zoomFactor -= 1
         if (X > self.windowWidth // 2):
            if (self.zoomFactor < 5):
               self.zoomFactor += 1
         print(f'Zoom: {self.zoomFactor}')      
         self.newWindowWidth =  self.windowWidth * self.zoomFactor
         self.newWindowHeight = self.windowHeight * self.zoomFactor
         self.newWindowPosX = self.windowPosX - (self.windowWidth * (self.zoomFactor - 1) // 2)
         self.newWindowPosY = self.windowPosY - (self.windowHeight * (self.zoomFactor - 1) // 2)
          
#         self.newRoi = cv2.resize(self.roi,
#                             (self.newWindowWidth,self.newWindowHeight),
#                             cv2.INTER_AREA)
#         cv2.resizeWindow(self.winID, self.newWindowWidth, self.newWindowHeight)
         cv2.moveWindow(self.winID, 
                        self.newWindowPosX,
                        self.newWindowPosY)
         cv2.imshow(self.winID, self.newRoi)
      pass

   def Run(self):
      self.bSystemAlive = True
      
      # Create the main window
      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
      cv2.resizeWindow(self.winID, self.windowWidth, self.windowHeight)
      cv2.setWindowTitle(self.winID,self.strTitle)
      cv2.moveWindow(self.winID,self.windowPosX, self.windowPosY)       
      cv2.setWindowTitle(self.winID,self.strTitle)
      cv2.setMouseCallback(self.winID,self.MouseCB)
      self.hwnd = win32gui.FindWindowEx(0, 0, 0, self.strTitle)

#      cv2.imshow(self.winID, self.roi)    # only for getting the handle of the zoomwindow
#      key = cv2.waitKey(40) & 0xff        # to test RT behaviour
      key = -1
      while self.bSystemAlive:
#         print('*',end = '')
#         cv2.moveWindow(self.winID,
#                        self.newWindowPosX, q
#                        self.newWindowPosY)
         if (self.winID != -1):
            try:
               cv2.resizeWindow(self.winID, self.newWindowWidth, self.newWindowHeight)
            except:
               print('Error in resize zoom')
               pass
            cv2.imshow(self.winID, self.newRoi) 
         key = cv2.waitKey(30) & 0xff        # to test RT behaviour
         if key == 27 or self.winID == -1:
            break
         continue
      if (key != 255):
         cv2.destroyWindow(self.winID)
         self.oldWinID = self.winID
         self.winID = -1
      print(f'CZoom {self.oldWinID} stopped!!!')

#************** For testing ***************
if __name__ == '__main__':
   parameters = CParameters
   roi = None
   zoom_handler = CZoom(parameters,roi)

