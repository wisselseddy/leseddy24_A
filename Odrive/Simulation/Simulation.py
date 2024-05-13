import cv2
import time
import random
import threading
import numpy as np
import ctypes

import win32gui
import win32console
from ctypes import windll, byref, wintypes
from CParameters import CParameters
from CMotor import *

global motorLeft, motorRight
motorLeft = None
motorRight = None

event1 = threading.Event()
event1.clear()
bDebugEncoder = False

# trackWinID = 'Track1'

# def TrackBar(Parameters):
#    cv2.namedWindow(trackWinID, cv2.WINDOW_NORMAL)
#    cv2.resizeWindow(trackWinID, 500, 100)
#    cv2.setWindowTitle(trackWinID,'Track Speed')
#    cv2.moveWindow(trackWinID, 20, 20)
   
#    img = np.zeros((100,500,3),dtype = 'uint8')
   
# #   cv2.createTrackbar('Speed', trackWinID,0, 100, OnTrack)
#    while (True):
#       cv2.imshow(trackWinID,img)
#       key = cv2.waitKey(16) 
#       if (key == 27 & 0xFF):
#          break
# #      trackValue = cv2.getTrackbarPos('Speed',trackWinID)
      
#    cv2.destroyWindow(trackWinID)
   
#    pass

# def OnTrack(x):
#    pass

listLeftTicks = []
listRightTicks = []

def SendEncoderInfo(Parameters):
   while (Parameters.bSystemAlive):
      event1.wait()
      event1.clear()
      leftTicks = len(listLeftTicks)
      rightTicks = len(listRightTicks)
      if (leftTicks != 0):
         if bDebugEncoder:
            print(f'Motor1: {leftTicks}')
         listLeftTicks.clear()
      if (rightTicks != 0):   
         if bDebugEncoder:
            print(f'Motor2: {rightTicks}')
         listRightTicks.clear()
      pass
   print('Sending Encoder stopped')

def EncoderLeft(Parameters):
   global listLeftTicks
   while Parameters.bSystemAlive:
      motorLeft.event1.wait()
      motorLeft.event1.clear()
      ticks = int(motorLeft.currentSpeed * 100 + 0.5)
      ticks /= 100
      listLeftTicks.append(ticks)
      event1.set()
   print('EncoderLeft stopped')
   pass

def EncoderRight(Parameters):
   global listRightClicks
   while Parameters.bSystemAlive:
      motorRight.event1.wait()
      motorRight.event1.clear()
      ticks = int(motorRight.currentSpeed * 100 + 0.5)
      ticks /= 100
      listRightTicks.append(ticks)
      event1.set()
   print('EncoderRight stopped')
   pass

def GetInput(Parameters):
   global motorLeft, motorRight
   while (Parameters.bSystemAlive):
      strInp = input('Speed [MotorIndex[0-2]] [0 - 10]: ')
      if (strInp.upper() == 'EXIT'):
         break
      indexSpace = strInp.find(' ')
      try:
         motorIndex = int(strInp[0:indexSpace])
         motorSpeed = float(strInp[indexSpace:])
         if (motorSpeed < -10.0 or motorSpeed > 10.0):
            raise ValueError('Invalid speed...')
         if (motorIndex != 0 and motorIndex != 1 and motorIndex != 2):
            raise ValueError('Invalid Motor Index...')
         if motorIndex == 0:
            motorLeft.DemandSpeed(motorSpeed)
         if motorIndex == 1:
            motorRight.DemandSpeed(motorSpeed)
         if motorIndex == 2:
            motorLeft.DemandSpeed(motorSpeed)
            motorRight.DemandSpeed(motorSpeed)
      except:
         print('Invalid input')
         continue
      
   Parameters.bSystemAlive = False
   event1.set()
   motorRight.event1.set()
   motorLeft.event1.set()
   motorRight.speedEventUp.set()
   motorRight.speedEventDown.set()
   motorLeft.speedEventUp.set()
   motorLeft.speedEventDown.set()
   print('Input Process Finished...')   

def MotorLeft(Parameters):
   global motorLeft
   motorLeft = CMotor(0,Parameters)
   while(Parameters.bSystemAlive):
      motorLeft.Run()
   print('Motor left stopped')
   pass

def MotorRight(Parameters):
   global motorRight
   motorRight = CMotor(1,Parameters)
   while(Parameters.bSystemAlive):
      motorRight.Run()
   print('Motor Right stopped')
   pass


if __name__ == "__main__":
   parameters = CParameters()
   threadMotor1 = threading.Thread(target=MotorLeft,args = (parameters, ))
   threadMotor1.start()
   threadMotor2 = threading.Thread(target=MotorRight,args = (parameters, ))
   threadMotor2.start()
   time.sleep(0.250)
   threadInput = threading.Thread(target=GetInput,args = (parameters, ))
   threadInput.start()
   threadEnc1 = threading.Thread(target=EncoderLeft,args = (parameters, ))
   threadEnc1.start()
   threadEnc2 = threading.Thread(target=EncoderRight,args = (parameters, ))
   threadEnc2.start()
   threadEncTx = threading.Thread(target=SendEncoderInfo,args = (parameters, ))
   threadEncTx.start()
#   time.sleep(1)
#   threadTrackBar = threading.Thread(target=TrackBar,args = (parameters, ))
#   threadTrackBar.start()




