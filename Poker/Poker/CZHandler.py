import time
import random
import threading
import numpy as np
import cv2

import win32gui
import win32api
import win32con

from MakeBmp import *
from CParameters import CParameters
from CZoom import CZoom

class CZHandler(object):
   def __init__(self,  CParams): 
      self.cParams = CParams
      self.localData = threading.local()
      self.zoomID = 0
      self.lockID = threading.Lock()
      self.lockID1 = threading.Lock()
      self.listZooms = []
      self.listThreads = []
      self.indexListZooms = -1
      cv2.setNumThreads(15)
      pass
   
   def CreateZoom(self,Roi):
      self.lockID1.acquire()
      localID = self.GetZoomID() 
      threadZ = threading.Thread(target=self.ZoomF,args = (self.cParams,localID,Roi))
      threadZ.start()
      self.lockID1.release()
      pass
   
   def ZoomF(self,CParams,ID,Roi):        # this is a separated thread....
#      win32api.PostMessage(self.cParams.displayHandler.hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
      localZoom = CZoom(CParams,ID,Roi)
      #localZoom.Run()
      print(f'Zoom {ID} stopped')
      pass
   
   def DisplayZoom(self):
      pass
   
   def DeleteZoom(self):
      pass
   
   def Run(self):
      while(self.cParams.bSystemAlive):
         time.sleep(1.0)
         pass
   
   def GetZoomID(self):
      self.lockID.acquire()
      self.zoomID += 1
      self.lockID.release()
      return self.zoomID
   



