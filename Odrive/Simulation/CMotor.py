from typing import Self
import cv2
import numpy as np
import time
import win32gui
import win32api
import win32con
import threading
import imutils

from CParameters import CParameters

class CMotor(object):
   def __init__(self, MotorID, CParams):
      a = np.radians(90)
      self.bSystemAlive = True
      self.cParams = CParams
      self.event1 = threading.Event()
      self.event2 = threading.Event()
      
      if (MotorID != 0 and MotorID != 1):
         print('Invalid MotorID')
         CParams.bSystemAlive = False
         return
      
      self.commandEventUp = threading.Event()
      self.commandEventDown = threading.Event()
      self.motorID = MotorID
      self.currentSpeed = 0
      self.demandedSpeed = 0
      self.maxSpeed = CParams.motorMaxSpeed    
      self.acceleration = CParams.motorAcceleration
      self.deacceleration = CParams.motorDeacceleration
      if (MotorID == 0):
         self.winID = 'Motor1'
         self.windowTitle = 'Motor Index 0'
         self.windowXPos = 20
      if (MotorID == 1):
         self.winID = 'Motor2'
         self.windowTitle = 'Motor Index 1'
         self.windowXPos = 350
         
      self.speedEventUp = threading.Event()
      self.speedEventUp.clear()
      self.speedEventDown = threading.Event()
      self.speedEventDown.clear()
      
      self.threadInc = threading.Thread(target=self.AdjustSpeedUp,args = (None, )) 
      self.threadInc.start()
      self.threadDec = threading.Thread(target=self.AdjustSpeedDown,args = (None, )) 
      self.threadDec.start()
      pass

   def AdjustSpeedUp(self,Arg):
      while (self.cParams.bSystemAlive):
         self.speedEventUp.wait()
         self.speedEventUp.clear()
         if (self.currentSpeed < 0):
            self.currentSpeed = int((self.currentSpeed * 100) - 0.5)
         if (self.currentSpeed > 0):
            self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
         self.currentSpeed /= 100

         print('Up')
         while (self.demandedSpeed > 0 and
                self.demandedSpeed > self.currentSpeed and
                self.cParams.bSystemAlive):
            self.currentSpeed += self.cParams.motorAcceleration
            if (self.currentSpeed < 0):
               self.currentSpeed = int((self.currentSpeed * 100) - 0.5)
            if (self.currentSpeed > 0):
               self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
            self.currentSpeed /= 100
            time.sleep(0.2)
            continue
         
         while (self.demandedSpeed > 0 and 
                self.demandedSpeed < self.currentSpeed and 
                self.cParams.bSystemAlive):
            self.currentSpeed += self.cParams.motorDeacceleration
            if (self.currentSpeed < 0):
               self.currentSpeed = int((self.currentSpeed * 100) - 0.5)
            if (self.currentSpeed > 0):
               self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
            self.currentSpeed /= 100
            time.sleep(0.2)
            continue
         
         while (self.demandedSpeed < 0 and 
                self.demandedSpeed < self.currentSpeed and 
                self.cParams.bSystemAlive):
            self.currentSpeed -= self.cParams.motorAcceleration
            if (self.currentSpeed > 0):
               self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
            if (self.currentSpeed < 0):
               self.currentSpeed = int((self.currentSpeed * 100) - 0.5)
            self.currentSpeed /= 100
            time.sleep(0.2)
            continue
         
         while (self.demandedSpeed < 0 and 
                self.demandedSpeed > self.currentSpeed and 
                self.cParams.bSystemAlive):
            self.currentSpeed -= self.cParams.motorDeacceleration
            if (self.currentSpeed > 0):
               self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
            if (self.currentSpeed < 0):
               self.currentSpeed = int((self.currentSpeed * 100) - 0.5)
            self.currentSpeed /= 100
            time.sleep(0.2)
            continue
         
         self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
         self.currentSpeed /= 100
         pass
      
   def AdjustSpeedDown(self,Arg):
      while (self.cParams.bSystemAlive):
         self.speedEventDown.wait()
         self.speedEventDown.clear()
         print('Down')
         if (self.demandedSpeed == 0):
            if (self.currentSpeed < 0.6 and self.currentSpeed > - 0.6):
               self.currentSpeed = 0
               continue
         
         while (self.demandedSpeed < self.currentSpeed and self.cParams.bSystemAlive):
            self.currentSpeed += self.cParams.motorDeacceleration
            time.sleep(0.1)
            
         while (self.demandedSpeed > self.currentSpeed and self.cParams.bSystemAlive):
            self.currentSpeed -= self.cParams.motorDeacceleration
            time.sleep(0.1)
         if (self.currentSpeed > 0):
            self.currentSpeed = int((self.currentSpeed * 100) + 0.5)
         if (self.currentSpeed < 0):
            self.currentSpeed = int((self.currentSpeed * 100) - 0.5)
         self.currentSpeed /= 100
         pass

   def SetCurrentSpeed(self, CurrentSpeed):
      self.currentSpeed = CurrentSpeed
      pass

   def DemandSpeed(self, DemandedSpeed):
      self.demandedSpeed = DemandedSpeed
      if (DemandedSpeed > 0 and DemandedSpeed > self.currentSpeed):
         self.speedEventUp.set()
      if (DemandedSpeed > 0 and DemandedSpeed < self.currentSpeed):
         self.speedEventDown.set()
      if (DemandedSpeed < 0 and DemandedSpeed > self.currentSpeed):
         self.speedEventDown.set()
      if (DemandedSpeed < 0 and DemandedSpeed < self.currentSpeed):
         self.speedEventUp.set()
      if (DemandedSpeed == 0):
         while self.currentSpeed != 0:
            self.speedEventDown.set()
            time.sleep(0.2)
      pass
   
   def Run(self):
      # Create the main window

#      contentsClear = np.zeros((480,640,3), dtype = 'uint8')      
      wheelImage = cv2.imread('C:\\pc2324\\Frames\\Frame_16.bmp')
#      src = cv2.cuda_GpuMat()
#      src.upload(wheelImage)
      
      x1, y1, x2, y2 = self.FindFramePicture(wheelImage)
      wPic = x2 - x1
      hPic = y2 - y1

      cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
      cv2.resizeWindow(self.winID, wPic*2, hPic*2)
      cv2.setWindowTitle(self.winID,self.windowTitle)
      cv2.moveWindow(self.winID,self.windowXPos, 20)

      roi = wheelImage[y1:y2,x1:x2] 
      # h,w,c = roi.shape
      # for hi in range(h):
      #    for wi in range(w):
      #       contentsClear[hi][wi] = roi[hi][wi]
      
#      contentsClear = wheelImage
      rotate = 0
      
#      M = cv2.getRotationMatrix2D((hPic//2,wPic//2),rotate,1) 
#      rot = 0
      oldRotate = 0
      while self.cParams.bSystemAlive:
         diffRotate = rotate - oldRotate
         oldRotate = rotate
         M = cv2.getRotationMatrix2D((hPic//2,wPic//2),rotate,1) 
         if (rotate < 359):
            rotate += self.currentSpeed
         else:
            rotate -= 359
            
         if (self.currentSpeed > 0):
            self.event1.set()
         if (self.currentSpeed < 0):
            self.event2.set()

         roi1 = cv2.warpAffine(roi,M,(hPic,wPic)) 
         cv2.imshow(self.winID, roi1) 
         key = cv2.waitKey(1)
         if key == 27 & 0xff:
            break
         # if (self.cParams.bWriteWheels and self.winID == 'Motor1' and self.currentSpeed == 1):
         #    if (rotate == 0):
         #       bRightStart = True
         #    if bRightStart:
         #       cv2.imwrite(self.cParams.strFramesPath + f'Wheel_rot{rot}.bmp',roi1)
         #       print(f'Wheel: {rot} is written')
         #       rot += 1
         #       if (rot == 360):
         #          self.cParams.bWriteWheels = False
      cv2.destroyWindow(self.winID)
      self.cParams.bSystemAlive = False  
   
   # def Run1(self):
   #    # Create the main window

   #    contentsClear = np.zeros((480,640,3), dtype = 'uint8')      
   #    wheelImage = cv2.imread('C:\\ejw\\EindproefSyntra\\Frames\\Frame_16.bmp')
   #    x1, y1, x2, y2 = self.FindFramePicture(wheelImage)
   #    wPic = x2 - x1
   #    hPic = y2 - y1

   #    cv2.namedWindow(self.winID, cv2.WINDOW_NORMAL)
   #    cv2.resizeWindow(self.winID, wPic*2, hPic*2)
   #    cv2.setWindowTitle(self.winID,self.windowTitle)
   #    cv2.moveWindow(self.winID,self.windowXPos, 20)

   #    roi = wheelImage[y1:y2,x1:x2] 
   #    h,w,c = roi.shape
   #    for hi in range(h):
   #       for wi in range(w):
   #          contentsClear[hi][wi] = roi[hi][wi]
      
   #    contentsClear = wheelImage
   #    rotate = 0
      
   #    while self.cParams.bSystemAlive:
   #       if (rotate < 9):
   #          rotate += self.currentSpeed
   #       else:
   #          rotate = 0
   #       if (rotate == 0):
   #          cv2.imshow(self.winID, self.cParams.roi0) 
   #       elif rotate == 1: 
   #          cv2.imshow(self.winID, self.cParams.roi1) 
   #       elif rotate == 2: 
   #          cv2.imshow(self.winID, self.cParams.roi2) 
   #       elif rotate == 3: 
   #          cv2.imshow(self.winID, self.cParams.roi3) 
   #       elif rotate == 4: 
   #          cv2.imshow(self.winID, self.cParams.roi4) 
   #       elif rotate == 5: 
   #          cv2.imshow(self.winID, self.cParams.roi5) 
   #       elif rotate == 6: 
   #          cv2.imshow(self.winID, self.cParams.roi6) 
   #       elif rotate == 7: 
   #          cv2.imshow(self.winID, self.cParams.roi7) 
   #       elif rotate == 8: 
   #          cv2.imshow(self.winID, self.cParams.roi8) 
   #       elif rotate == 9: 
   #          cv2.imshow(self.winID, self.cParams.roi9) 
   #       key = cv2.waitKey(1)
   #       if key == 27 & 0xff:
   #          break
   #    cv2.destroyWindow(self.winID)
   #    self.cParams.bSystemAlive = False  
      
   def Timing(self):
      while (self.cParams.systemAlive):
         time.sleep(self.cParams.motorTimeUnit)
         self.ProcessTiming()
      pass
   
   def FindFramePicture(self,BmpFile) -> list:
      h,w,c = BmpFile.shape
      listXY = [255,255,0,0]
      hi = 0
      while (hi < h):
         for wi in range(w):
            if (BmpFile[hi][wi].all() != [0,0,0]).all():
               if wi < listXY[0]:
                  listXY[0] = wi
                  break
         hi += 1
      
      wi = 0
      while (wi < w):
         for hi in range(h):
            if (BmpFile[hi][wi].all() != [0,0,0]).all():
               if hi < listXY[1]:
                  listXY[1] = hi
                  break
         wi += 1
         
      hi = 0
      while (hi < h):
         for wi in range(w-1,0,-1):
            if (BmpFile[hi][wi].all() != [0,0,0]).all():
               if wi > listXY[2]:
                  listXY[2] = wi
                  break
         hi += 1
      
      wi = 0
      while (wi < w):
         for hi in range(h-1,0,-1):
            if (BmpFile[hi][wi].all() != [0,0,0]).all():
               if hi > listXY[3]:
                  listXY[3] = hi
                  break
         wi += 1

      return listXY
   
   def ProcessTiming(self):
      if (self.currentSpeed > 0):
         if (self.demandedSpeed != self.currentSpeed):
            if (self.demandedSpeed > self.currentSpeed):
               self.currentSpeed += self.acceleration
            if (self.demandedSpeed < self.currentSpeed):
               self.currentSpeed -= self.deacceleration
      elif (self.currentSpeed < 0):
         if (self.demandedSpeed != self.currentSpeed):
            if (self.demandedSpeed < self.currentSpeed):
               self.currentSpeed -= self.acceleration
            if (self.demandedSpeed > self.currentSpeed):
               self.currentSpeed += self.deacceleration
      else:
         if (self.demandedSpeed > 0):
            self.currentSpeed += self.acceleration
         if (self.demandedSpeed < 0):
            self.currentSpeed -= self.acceleration
      pass

   def Encoder(self):
      pass
            
