from pickle import FALSE
import cv2
import time
import random
import threading
import numpy as np

from CDHandler import *
from CCHandler import *
from CHSlider import *
from CZHandler import CZHandler

from MakeBmp import *
from CParameters import CParameters
import ctypes

import win32gui
import win32console
import numpy

#from obspy.core import read
#import win32api

from ctypes import windll, byref, wintypes
#from ctypes.wintypes import SMALL_RECT

#STDOUT = -11
#hdl = windll.kernel32.GetStdHandle(STDOUT)
#rect = wintypes.SMALL_RECT(600,20, 1200, 520) # (left, top, right, bottom)
#ret = windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))
#bufsize = wintypes._COORD(500,500) # rows, columns
#windll.kernel32.SetConsoleScreenBufferSize(hdl, bufsize)

appName = 'Command Prompt'
version = cv2.__version__
#pass

quan = 0    # quantity of sliders
hei = 0     # height of sliders
XPos = 20   # X startPosition of the slider window
YPos = 20   # Y startPosition of the slider window
 
def ZoomHandler(CParams):
   zm_handler = CZHandler(CParams)
   CParams.zoomHandler = zm_handler
   zm_handler.Run()
   
   pass

def DisplayHandler(WinID,arg2,CParams):
   d_handler = CDHandler(WinID,CParams)
   CParams.displayHandler=d_handler
   threadS = threading.Thread(target=Sliders,args = (threadingLock,CParams))
   threadS.start()
   d_handler.run()
   pass 

def CommandHandler(arg1, CParams):
   cc_handler = CCHandler(CParams)
   CParams.commandHandler = cc_handler
#   cc_handler.ShowHelp()
   cc_handler.CommandHandler()
   pass

def Sliders(Tl, CParams):
   hSlider = CHSlider(Tl,CParams)
   hSlider.Run(CParams)
   pass

if __name__ == "__main__":
   parameters = CParameters()                #instance of parameter class
#   displayHandler = CDHandler(parameters)
      
   parameters.hwndMainWindow = win32console.GetConsoleWindow()
   parameters.mainWindowTitle = 'EindProef'
   win32gui.SetWindowText(parameters.hwndMainWindow,parameters.mainWindowTitle)
   
#*******************************
# convert to utility to reuse
#    
   quantityInp = ''
   heightInp = ''
   hei = 0
   while (quantityInp == ''):
      parameters.SetTerminalToVT100()
      quantityInp = input('Quantity (12):')
      if (quantityInp == ''):
         quantityInp = 12
         quan = 12
         parameters.setSliderQuantity(quan)
      else:
         try:
            quan = int(quantityInp)
            parameters.setSliderQuantity(quan)
         except:
            print('Invalid Command')
            quantityInp == ''
      
   while (heightInp == ''):
      heightInp = input('Height (480): ')
      if (heightInp == ''):
         heightInp = '480'
         try:
            hei = 480
            parameters.setDisplayHeight(hei)
         except:
            print('Invalid Command')
            heightInp == ''
      else:
         try:
            hei = int(heightInp)
            parameters.setDisplayHeigth(hei)
         except:
            print('Invalid Command')
            quantityInp == ''
            
   # Calculate width of the slider  in function of number of sliders
   
   sliderWidth = MakeBmp(quan,hei)
   
   strPosX = input('Start X Position (20): ')
   if (strPosX == ''):
      posX = 20
      parameters.setDisplayPosX(posX)
   else:
      try:
         posX = int(strPosX)
         parameters.setDisplayPosX(posX)
      except:
         print('Invalid Command')
         heightInp == ''
      
   strPosY = input('Start Y Position (20): ')

   if (strPosY == ''):
      posY = 20
      parameters.setDisplayPosY(posY)
   else:
      try:
         posY = int(strPosX)
         parameters.setDisplayPosY(posY)
      except:
         print('Invalid Command')
         strPosY == ''
         
   for q in range(quan):
      parameters.listSlidersNames.append('Slider-%d' % (q))
      parameters.listSlidersMinMaxCur.append([0,255,127])
      parameters.listSlidersColors.append([220+q,0,0])
   parameters.listSlidersMinMaxCur[-1] = [1,100,1]
   
#   parameters.calcNewParams()
  
   widthDisplayHandler = parameters.getDisplayWidth()
#   win32gui.MoveWindow(han, posX, posY, quan * 11 + widthDisplayHandler, hei + 5, True)

   threadingLock = threading.Lock()
   threadCH = threading.Thread(target=CommandHandler,args = (threadingLock, parameters))
   threadDH = threading.Thread(target=DisplayHandler,args = ('Main Display', threadingLock, parameters ))
   threadCH.start()
   threadDH.start()
   threadZM = threading.Thread(target=ZoomHandler,args = (parameters, ))
   threadZM.start()



