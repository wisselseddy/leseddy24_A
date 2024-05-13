
import os
import numpy as np
import win32gui
import win32con
import win32ui
import win32console
from PIL import Image

from CAnalysHandler import *
from CDHandler import *
from CProcessImage import *
from CCamera import *
from CProcessImage import *
from CVideoServer import *
from CAnalysFrame import *

import threading

from CParameters import CParameters

#from symbol import try_stmt

class CCHandler(object):
   def __init__(self,CParams):
      self.cParams = CParams
      self.bSystemAlive = True   # not here
      self.height = 0
      self.width = 0
      self.quantity = 0
      self.position = [0, 0]
      self.rgb = [0, 0, 0]
      self.title = ""
      self.bSliderDebug = False
      self.bOldSliderDebug = False
      self.bDrawCircle = False
      self.listX = []
      self.listY = []
      self.analysFrameHandler = None
      
      CParams.bCameraAlive = False
      self.cParams.bPictureAlive = True
      CParams.cameraIndex = 0
      self.threadCamera = None
      self.camera = None
      self.listWindows = []
      self.listWindowsCounter = 0
      self.windowframeindex = -1
      self.bRestore = False
      self.bPredefinedSave = False
      self.strTestPictureName = 'c:\\ejw\\crimac\\crimac.jpg'
      self.frameTuple = None
      self.bTimerServerAlive = False
      self.bSaveSingleImage = False
      self.bRecording = False
      self.bAnalysFrameActive = False
      
   def SetHeight(self, arg1):
      self.height = int(arg1)
 
   def SetWidth(self, arg1):
      self.width = int(arg1)
 
   def SetQuantity(self, arg1):
      self.quantity = int(arg1)
 
   def SetPosition(self, arg1):
      self.position = [int(arg1[0]), int(arg1[1])]
 
   def SetRGB(self, arg1):
      self.rgb = [int(arg1[0]), int(arg1[1]), int(arg1[2])]
 
   def SetTitle(self, arg1):
      self.title = arg1
 
   def ShowHelp(self):
      print('**********************************************')
      print('              Valid Commands and Arguments')
      print('**********************************************')
      print('Width=value    - Set Window Width (e.g., Width=800)')
      print('Height=value   - Set Window Height (e.g., Height=600)')
      print('Quantity=value - Set Quantity (e.g., Quantity=10)')
      print('Position=x,y   - Set Window Position (e.g., Position=100,100)')
      print('Title=value    - Set Window Title (e.g., Title=My Window)')
      print('RGB SETTING = r,g,b - Set RGB values for routine 1 (e.g., RGB=255,0,0)')
      print('RGBFILTER ON   - Set RGB Filter on camera on')
      print('RGBFILTER OFF  - Set RGB Filter on camera off')
      print('Slider Debug ON     - Set Debug ON for slider-info')
      print('Slider Debug OFF    - Set Debug ON for slider-info')
      print('Circle              - Draw Circle')
      print('Camera On, Index    - Turn Camera On')
      print('Camera Off, Index   - Turn Camera Off')
      print('ListFrames          - List all Windows On Desktop')
      print('Delete Frames          - Delete all frames in the frames directory')
      print('SelectedWindow = Index - Select Windows On Desktop')
      print('WindowsFrame Index     - Select Windows On Desktop with index from List')
      print('GetSliderValue Index   - Select Min,Max,Cur value of the indexed slider from SliderList')
      print('MHLC                   - Select Horz. Line with mouse')
      print('MVLC                   - Select Vert. Line with mouse')
      print('GetSliderValue Index   - Select Min,Max,Cur value of the indexed slider from SliderList')
      print('DVL [width]            - Select Vert. line')
      print('DHL [height]           - Select Horiz. line')
      print('STOREIMAGE             - Store picture')
      print('RESTOREIMAGE           - Restore picture')
      print('LoadImage imgName      - Load image')
      print('SetBackColor [left mouse button] - Select background color')
      print('FilterImage On         - Filter image')
      print('DetectBorder           - Detect Border') 
      print('ProcessCursor [Type]   - Set Cursor for processing image')
      print('GetProcessCursor       - Get Cursor for processing image')
      print('ListSavedImages        - Give index of saved images')
      print('SAVESINGLEIMAGE ON     - Save image with next index on mouse click')
      print('SAVESINGLEIMAGE OFF    - Save image with next index on mouse click')
      print('SAVEPREDEFINEDIMAGE    - Save single image at predefined place')
      print('RESTOREPREDEFINEDIMAGE - Restore single image from predefined place')
      print('LOCATIONFRAMES         - Show the path of the frames storage')
      print('Exit                   - Exit the program')
      print('Help                   - Show extended help')
   
   def GetSliderValue(self,SliderIndex):
      llist = self.cParams.listSlidersMinMaxCur[SliderIndex]
      print('Slider %d Min %d Max %d Cur %d\n' % (SliderIndex,llist[0],llist[1],llist[2]))
      pass

   def makeCircle(self,Radius):
      alpha = np.linspace(0,np.pi * 2,1000)
      self.listX = []
      self.listY= []
      for a in alpha:
         self.listX.append(np.cos(a) * Radius)
         self.listY.append(np.sin(a) * Radius)
      a= self.listX[0]
      self.cParams.displayHandler.drawCircle(self.listX,self.listY)
      pass
      
   def windowInfo(self, Number):
      windowText = self.listWindows[Number - 1]
      self.GetFrame(windowText)
      pass
   
   def ListWindows(self):
      self.listWindows = []                  # empty list
      self.listWindowsCounter = 1
      
      def enumHandler(hwnd,lParam):
#        han = win32console.GetConsoleWindow()
         if win32gui.IsWindowVisible(hwnd):
            windowText =  win32gui.GetWindowText(hwnd)
            if (not windowText == ""):
               self.listWindows.append(windowText)
               print('%d: %s' % (self.listWindowsCounter,windowText))
               self.listWindowsCounter += 1
               pass

      win32gui.EnumWindows(enumHandler, None)
      pass
   
   def GetFrame(self,Hwnd,Params):
      hwnd = Hwnd
      left, top, right, bot = win32gui.GetWindowRect(hwnd)
      leftc, topc, rightc, botc = win32gui.GetClientRect(hwnd)
      w = right - left -1
      h = bot - top -1
      wDC = win32gui.GetWindowDC(hwnd)
      dcObj=win32ui.CreateDCFromHandle(wDC)
      cDC=dcObj.CreateCompatibleDC()
#      hbmC =dcObj.CreateCompatibleBitmap(wDC,right,bot)
      dataBitMap = win32ui.CreateBitmap()
      dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
      oldSelectedObject = cDC.SelectObject(dataBitMap)
#      strA = dcObj.GetBitmapBits(w * h)
#      self.cParams.displayHandler.SetBufImg(strA, w, h)
      cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
      strA = dataBitMap.GetBitmapBits(w * h)
      bitmapSize = dataBitMap.GetSize()
      cDC.SelectObject(oldSelectedObject)

      typeStrA = type(strA)
      lenStrA = len(strA)
      lenBitmaps = w * h * 4
#      self.cParams.displayHandler.SetBufImg(strA)
      npArray = (np.frombuffer(strA,dtype = 'uint8'))
#      print(npArray.shape)
      self.cParams.displayHandler.SetGraphicsBuffer(strA,w,h)
#     
#      npArrayBut = npArray.reshape(h,w,3)
      
      if (self.bPredefinedSave):
         dataBitMap.SaveBitmapFile(cDC, "c:\\testPython\\SelectedWindow.bmp")
         print("Image saved...")
         self.self.bPredefinedSave = False
# Free Resources
      dcObj.DeleteDC()
      cDC.DeleteDC()
      win32gui.ReleaseDC(hwnd, wDC)
      win32gui.DeleteObject(dataBitMap.GetHandle())
      pass
   
   def DrawDHL(self,WidthIndex):
      print('Line height: %d' %(WidthIndex))
      # inform display that this line must be white
      self.cParams.displayHandler.DHL(WidthIndex)
      pass
   def DrawDVL(self, HeightIndex):
      print('Line width: %d' %(HeightIndex))
      # inform display that this line must be white
      self.cParams.displayHandler.DVL(HeightIndex)
      pass

   def TriggerWindowsFrameCommand(self):
      if self.windowframeindex == -1:
         return -1
      frameIndex = self.windowframeindex
      strWindowsTitle = self.listWindows[frameIndex - 1]
      self.GetFrame(strWindowsTitle)
      bWindowsFrameActive = True
      return frameIndex
   
   def TimerServer(self, FrameTuple):
      while(self.bSystemAlive and self.bTimerServerAlive):
         self.cParams.videoBuffer = self.FastFrame(FrameTuple)
         divisor = 1 / self.cParams.listSlidersMinMaxCur[-1][2]
         time.sleep(divisor)
      print('\nTimer Server stopped')   
      
   def Convert(self,Bitmap) -> cv2.Mat:
      bmpinfo = Bitmap.GetInfo()
      bmpbits = Bitmap.GetBitmapBits(True)
      pil_im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpbits, 'raw', 'RGBA', 0, 1)
      pil_array = np.array(pil_im)    
      new_array = cv2.cvtColor(pil_array, cv2.COLOR_RGBA2RGB)
      return new_array
   
   def FastFrame(self, FrameTuple):
      windowsTitle, hwnd, w, h = FrameTuple
      wDC = win32gui.GetWindowDC(hwnd)
      dcObj=win32ui.CreateDCFromHandle(wDC)
      cDC=dcObj.CreateCompatibleDC()
      dataBitMap = win32ui.CreateBitmap()
      dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
      oldSelectedObject = cDC.SelectObject(dataBitMap)
      cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
      image = self.Convert(dataBitMap)
#      strA = dataBitMap.GetBitmapBits(w * h)
#      bitmapSize = dataBitMap.GetSize()
      cDC.SelectObject(oldSelectedObject)

#      typeStrA = type(strA)
#      lenStrA = len(strA)
#      lenBitmaps = w * h * 4
#      npArray = (np.frombuffer(strA,dtype = 'uint8'))
#      print(npArray.shape)
#      self.cParams.displayHandler.SetGraphicsBuffer(strA,w,h)
#      b = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
      if (self.bPredefinedSave):
         dataBitMap.SaveBitmapFile(cDC, "c:\\testPython\\SelectedWindow.bmp")
         print("Image saved...")
         self.bPredefinedSave = False

# Free Resources
      dcObj.DeleteDC()
      cDC.DeleteDC()
      win32gui.ReleaseDC(hwnd, wDC)
      win32gui.DeleteObject(dataBitMap.GetHandle())
      return image
   
   #*****************************************
   # Difference between two frames
   #
   # Parameters:
   #     Cs    : First Frame
   #     Cp    : Second Frame
   #
   # Frames must have the same shape
   #
   # returns:
   #     diffcounter, diffFrame
   #
   #*****************************************

   def Diff(self, Cs, Cp):
      (Rs,Gs,Bs) = cv2.split(Cs)
      (RRs,GGs,BBs) = cv2.split(Cp)
#     (RRsOrg,GGsOrg,BBsOrg) = cv2.split(Cp)
      Rs[Rs>0] -= RRs[Rs>0]
      Gs[Gs>0] -= GGs[Gs>0]
      Bs[Bs>0] -= BBs[Bs>0]
      Rs[Rs!=0] = RRs[Rs!=0]
      Gs[Gs!=0] = GGs[Gs!=0]
      Bs[Bs!=0] = BBs[Bs!=0]
      
#  #   RRs[RRs>0] -= Rs[RRs>0]
#  #   GGs[GGs>0] -= Gs[GGs>0]
#  #   BBs[BBs>0] -= Bs[BBs>0]
      diffCounter = 0
      for i in Rs[Rs != 0]:
         diffCounter += 1
      for i in Gs[Gs != 0]:    
         diffCounter += 1
      for i in Bs[Bs != 0]:    
         diffCounter += 1
      if (diffCounter != 0):
         print(f'Differences: {diffCounter}')
      return diffCounter,cv2.merge([Rs,Gs,Bs])
         
   def CommandHandler(self):
      frameName = "" 
      bWindowsFrameActive = False
      frameIndex = -1
      while self.bSystemAlive:
         if (not self.bSliderDebug == self.bOldSliderDebug):
            self.bOldSliderDebug == self.bSliderDebug
            self.cParams.bSliderDebug = self.bSliderDebug
            self.cParams.bTrigger = True
         bNotOK = True
         
         strInput = input('Command: ')
         strInput = strInput.upper()
         lenInput = len(strInput)
         bWindowsFrameActive = False
         
         try:
            if ("L" == strInput):
               self.cParams.processImageHandler = CProcessImage(self.cParams,self.strTestPictureName)   # Initiate class
               self.cParams.processImageHandler.Run()
               bNotOK = False
            if ('VIDEOSERVER ON'in strInput):
               self.cParams.videoServer = CVideoServer(self.cParams, False)
               self.threadVideoServer = threading.Thread(target=self.cParams.videoServer.Run,args = (None,))
               self.threadVideoServer.start()
               bNotOK = False
            if ('VIDEOSERVER OFF'in strInput):
               self.cParams.videoServerHandler.bVideoServerAlive = False
               self.cParams.bPictureAlive = False
               self.cParams.videoServerHandler.EndAcceptance()
               bNotOK = False
            if ('DISPLAYPICTURE ON' in strInput):
               self.cParams.bPictureAlive = True
               bNotOK = False
            if ('DISPLAYPICTURE OFF' in strInput):
               self.cParams.bPictureAlive = False
               bNotOK = False
            if "TRIGGERANALYSWINDOW" in strInput:
               self.cParams.analysHandler.TriggerShow()
               bNotOK = False
            if "SAVEPREDEFINEDIMAGE" in strInput:
               self.bPredefinedSave = True
               bNotOK = False
            if "RESTOREPREDEFINEDIMAGE" in strInput:
               try:
                  dataBitMap = cv2.imread("c:\\testPython\\SelectedWindow.bmp")
                  ht,wt,ct = dataBitMap.shape
                  dataByte = bytes(dataBitMap)
                  self.cParams.displayHandler.SetGraphicsBuffer2(dataByte,wt,ht)
                  print("Image Restored")
                  bNotOK = False
               except:
                  print("Error in restore!!!")
            if "QUANTITY" in strInput:
               self.SetQuantity(strInput.split('=')[-1])
               bNotOK = False
            if "RGBFILTER ON" in strInput:
               self.cParams.bRGBFilter = True
               bNotOK = False
            if "RGBFILTER OFF" in strInput:
               self.cParams.bRGBFilter = False
               bNotOK = False
            if "RGBFILTER1 ON" in strInput:
               self.cParams.bRGBFilter1 = True
               bNotOK = False
            if "RGBFILTER1 OFF" in strInput:
               self.cParams.bRGBFilter1 = False
               bNotOK = False
            if "RGBFILTER2 ON" in strInput:
               self.cParams.bRGBFilter2 = True
               bNotOK = False
            if "RGBFILTER2 OFF" in strInput:
               self.cParams.bRGBFilter2 = False
               bNotOK = False
            if "CIRCLE" in strInput:
               self.bDrawCircle = True
               self.makeCircle(100)
               bNotOK = False
            if "EXIT" in strInput:
#               self.FinishSystem()
               self.bSystemAlive = False
               try:
                  self.bTimerServerAlive = False
                  self.cParams.bCameraAlive = False
                  self.cParams.bPictureAlive = False
                  self.cParams.bAlive = False
                  if (self.cParams.analysHandler != None):
                     self.cParams.analysHandler.bAlive = False
                     self.cParams.analysHandler.TriggerShow()
                     
               except:
                  pass                                    
               bNotOK = False
            if "WIDTH" in strInput:
               self.SetWidth(strInput.split('=')[-1])
               bNotOK = False
            if "HEIGHT" in strInput:
               self.SetHeight(strInput.split('=')[-1])
               bNotOK = False
            if "POSITION" in strInput:
               self.SetPosition(strInput.split('=')[-1].split(','))
               bNotOK = False
            if "RGB SETTING" in strInput:
               self.SetRGB(strInput.split('=')[-1].split(','))
               
               bNotOK = False
            if "TITLE" in strInput:
               self.SetTitle(strInput.split('=')[-1])
               bNotOK = False
            if "HELP" in strInput:
               self.ShowHelp()
               bNotOK = False
               
            if "MHLC ON" in strInput:
               self.cParams.displayHandler.bDHLActive = True
               self.cParams.displayHandler.bDVLActive = False
               if (self.cParams.analysHandler == None):
                  print('No ANALYSHANDLER is Created!')
               bNotOK = False
               pass
            
            if "RECT ON" in strInput:
               self.cParams.displayHandler.bRectActive = True
               if (self.cParams.analysHandler == None):
                  print('No ANALYSHANDLER is Created!')
               bNotOK = False
               pass
            
            if "RECT OFF" in strInput:
               self.cParams.displayHandler.bRectActive = False
               if (self.cParams.analysHandler == None):
                  print('No ANALYSHANDLER is Created!')
               bNotOK = False
               pass
            
            if "MHLC OFF" in strInput:
               self.cParams.displayHandler.bDHLActive = False
               if (self.cParams.analysHandler == None):
                  print('No ANALYSHANDLER is Created!')
               bNotOK = False
               pass
            
            if "MVLC ON" in strInput:
               self.cParams.displayHandler.bDVLActive = True
               self.cParams.displayHandler.bDHLActive = False
               if (self.cParams.analysHandler == None):
                  print('No ANALYSHANDLER is Created!')
               bNotOK = False
               pass
            
            if "MVLC OFF" in strInput:
               self.cParams.displayHandler.bDVLActive = False
               if (self.cParams.analysHandler == None):
                  print('No ANALYSHANDLER is Created!')
               bNotOK = False
               pass
            
            if "VLA OFF" in strInput:
               self.cParams.analysHandler.SetVLAbActive(False)
               self.cParams.analysHandler.TriggerShow()
               bNotOK = False
               
            if "VLA CLEAR" in strInput:
               self.cParams.analysHandler.ClearVLA()
               self.cParams.analysHandler.TriggerShow()
               bNotOK = False
               
            if "VLA ON" in strInput:
               self.cParams.analysHandler.SetVLAbActive(True)
               self.cParams.analysHandler.TriggerShow()
               bNotOK = False
            
            if "DHL" in strInput:
               if (len(strInput) > 3):
                  try:
                     hLineIndex = int(strInput[3:].lstrip())
                  except:
                     print('Invalid Command')
                     continue
               self.cParams.sliderHandler.bDHLActive = True   
               self.DrawDHL(hLineIndex)
               bNotOK = False

            if "DVL" in strInput:
               if (len(strInput) > 3):
                  try:
                     vLineIndex = int(strInput[3:].lstrip())
                  except:
                     print('Invalid Command')
                     continue
               self.cParams.sliderHandler.bDVLActive = True  
               self.DrawDVL(vLineIndex)
               bNotOK = False

            if "SLIDER DEBUG ON" in strInput:
               self.bSliderDebug = True
               bNotOK = False
            if "SLIDER DEBUG OFF" in strInput:
               self.bSliderDebug = False
               bNotOK = False
            if "CAMERA ON" in strInput:
               if "CAMERA ON," in strInput:
                  try:
                     self.camera = CCamera(self.cParams)                  
                     camera_index_str = strInput[10:]
#                     self.cParams.cameraIndex = int(camera_index_str) if camera_index_str else 0   # criptic programming
                     self.cParams.cameraIndex = int(camera_index_str)
                     
                     self.cParams.bCameraAlive = True
                     print(f'Turning camera {self.cParams.cameraIndex} ON')
                     self.threadCamera = threading.Thread(target=self.camera.cameraRunning,args = (None,))
                     self.threadCamera.start()
                     bNotOK = False
#                     self.cParams.bCameraAlive = True     # is already set
                  except ValueError:
                     print('Invalid camera index. Please provide a valid number.')
                     self.cParams.bCameraAlive = False
               else:
                  self.cParams.cameraIndex = 0
                  self.cParams.bCameraAlive = True
                  print('Turning default camera ON') 
                  self.camera.cameraRunning()
                  bNotOK = False
                  self.cParams.bCameraAlive = True
            
            if "CAMERA OFF" in strInput:
               self.cParams.bCameraAlive = False
               print('Turning camera OFF') 
               bNotOK = False
               
            if "WINDOWSFRAME" in strInput:
               if (len(strInput) > 12):
                  frameIndex = int(strInput[12:].lstrip())
                  self.windowframeindex = frameIndex
                  strWindowsTitle = self.listWindows[frameIndex - 1]
                  self.GetFrame(strWindowsTitle)
                  bNotOK = False
                  bWindowsFrameActive = True
                  self.cParams.sliderHandler.bActivateTriggerWindows = True
               elif (len(strInput) == 12):
                  frameIndex = self.selectedWindowNumber
                  strWindowsTitle = self.listWindows[frameIndex - 1]
                  self.GetFrame(strWindowsTitle)
                  bNotOK = False
               else:
                  pass
            else:
               pass
            if ("REITERATE" in strInput):
               self.cParams.processImageHandler.Reiterate()
               bNotOK = False
              
            if "SETBACKCOLOR" in strInput:
               print('Setup BACKCOLOR !!!')
               self.cParams.processImageHandler.SetBackColor()
               bNotOK = False
               
            if ("ANALYSWINDOW ON" in strInput):
               self.cParams.analysHandler = CAnalysHandler(self.cParams, 1)    # Multiplier
               self.cParams.analysHandler.bAlive = True
               print('Analys Window ON * 1')
               self.threadAnalysHandler = threading.Thread(target=self.cParams.analysHandler.Run,args = (None,))
               self.threadAnalysHandler.start()
               bNotOK = False
               pass
            
            if ("ANALYSWINDOW3 ON" in strInput):
               self.cParams.analysHandler = CAnalysHandler(self.cParams, 3)    # Multiplier
               self.cParams.analysHandler.bAlive = True
               print('Analys Window On * 3')
               self.threadAnalysHandler = threading.Thread(target=self.cParams.analysHandler.Run,args = (None,))
               self.threadAnalysHandler.start()
               bNotOK = False
               pass
            
            if ("ANALYSWINDOW OFF" in strInput):
               self.cParams.analysHandler.bAlive = False
               self.cParams.analysHandler.TriggerShow()
               time.sleep(1.0)
#               self.threadAnalysHandler.join(1.0)
               print('Analys Handler OFF in CCHandler')
               bNotOK = False
               pass
            
            if ("ANALYSWINDOW3l OFF" in strInput):
               self.cParams.analysHandler.bAlive = False
               self.cParams.analysHandler.TriggerShow()
               time.sleep(1.0)
#               self.threadAnalysHandler.join(1.0)
               print('Analys Handler OFF in CCHandler')
               bNotOK = False
               pass

            if "GETSLIDERVALUE" in strInput:
               if (lenInput > 14):
                  try:
                     sliderIndex = int(strInput[14:])         #index from the slider
                     self.GetSliderValue(sliderIndex)
                     bNotOK = False
                  except:
                     pass
               elif lenInput < 15:
                  sliderIndex = self.selectedWindowNumber
                  print('Index %d used.' % (sliderIndex))
                  self.GetSliderValue(sliderIndex)
                  bNotOK = False
               else:
                  print('No Index Given')
                  bNotOK = False
           
            if "LOADIMAGE " in strInput:
               strFilename = strInput[10:] 
               if (strFilename != '' and os.path.exists(strFilename)):
                  self.cParams.processImageHandler = CProcessImage(self.cParams,strFilename)   # Initiate class
                  self.cParams.processImageHandler.ProcessImage()
               else:
                  print('Invalid Image')   
               bNotOK = False
            
            if "RELOADIMAGE" in strInput:
               self.cParams.processImageHandler.ReloadImage()
               bNotOK = False
            
            if "CLEARIMAGE" in strInput:
               self.cParams.processImageHandler.ClearImage()
               bNotOK = False
            
            if "KILLIMAGE" in strInput:
               self.cParams.processImageHandler.KillImage()
               bNotOK = False
            
            if "FILTERIMAGE ON" in strInput:
               rule = self.cParams.analysHandler.GetRules()
               self.cParams.sliderHandler.SetRules(rule)               
               self.cParams.processImageHandler.SetRules(rule)               
               self.cParams.processImageHandler.FilterState(True)
               bNotOK = False
               
            if "FILTERIMAGE OFF" in strInput:
               self.cParams.processImageHandler.FilterState(False)
               bNotOK = False
               
            if "DETECTBORDER" in strInput:
               self.cParams.processImageHandler.DetectBorder()
               bNotOK = False
               
            if "LIST WINDOWS" in strInput:
               self.ListWindows()
               bNotOK = False
               
            if 'SELECTEDWINDOW' in strInput:
               self.selectedWindowNumber = int(strInput.split('=')[-1])
               print('Window %d is selected' % (self.selectedWindowNumber))
#               bNotOK = False
               self.windowframeindex = self.selectedWindowNumber
               
               strWindowsTitle = self.listWindows[self.windowframeindex - 1]
               hwnd = win32gui.FindWindowEx(0,0,0, strWindowsTitle)
               left, top, right, bot = win32gui.GetWindowRect(hwnd)
               leftc, topc, rightc, botc = win32gui.GetClientRect(hwnd)
               w = right - left -1
               h = bot - top -1
               self.frameTuple = tuple((strWindowsTitle,hwnd,w,h))
               self.cParams.displayHandler.ResizeDisplayHandler(w,h)
               self.GetFrame(hwnd,strWindowsTitle)
               bNotOK = False
               bWindowsFrameActive = True
               self.cParams.sliderHandler.bActivateTriggerWindows = True
               
            if 'WINDOWINFO' in strInput:
               self.selectedWindowNumber = int(strInput[10:])
               self.windowInfo(self.selectedWindowNumber)
               bNotOK = False
            if 'STOP CAMERA' in strInput:
               self.cParams.bCameraAlive = True
               bNotOK = False
            if 'RESTART CAMERA' in strInput:
               self.cParams.bCameraAlive = False
               bNotOK = False
            if 'SAVEPROCESSEDIMAGE' in strInput:
               self.savePath = strInput[19:]
               if (self.cParams.proccesImageHandler != None):
                  self.cParams.proccesImageHandler.save(self.savePath)
               else:
                  print('No ProcessImage to Save !!!')
               bNotOK = False
            if 'GETPROCESSCURSOR' in strInput:
               if (self.cParams.processImageHandler != None):
                  self.cParams.processImageHandler.GetCursorType()
               bNotOK = False
               
            if 'SETPROCESSCURSOR' in strInput:
               strCursorType = strInput[13:]
               if (self.cParams.proccesImageHandler != None):
                  self.cParams.proccesImageHandler.SetCursorType(strCursorType)
               else:
                  print('No Process Handler available')
               bNotOK = False
               
            if 'FRAMEGRABBING ON' in strInput:
               if (self.frameTuple == None):
                  print('No window is selected')
                  bNotOK = False
                  continue
               else:
                  self.bTimerServerAlive = True
                  self.timerThread = threading.Thread(target=self.TimerServer,args = (self.frameTuple,))
                  self.timerThread.start()
               if (self.cParams.displayHandler != None):
                  self.cParams.displayHandler.bFrameGrabbing = True
               else:
                  print('No Display Handler available')
               bNotOK = False
               
            if 'FRAMEGRABBING ALL' in strInput:
               self.bTimerServerAlive = True
               if (self.cParams.displayHandler != None):
                  self.cParams.displayHandler.bFrameGrabbingAll = True
               else:
                  print('No Display Handler available')
               bNotOK = False
               
            if 'FRAMEGRABBING OFF' in strInput:
               self.bTimerServerAlive = False
               if (self.cParams.displayHandler != None):
                  self.cParams.displayHandler.bFrameGrabbing = False
                  self.cParams.displayHandler.bFrameGrabbingAll = False
                  self.cParams.bPictureAlive = False
               else:
                  print('No Display Handler available')
               bNotOK = False
            if 'LOCATIONFRAMES' in strInput:
               path = self.cParams.displayHandler.strFramePath
               print(f'FramePath: {path}')
               bNotOK = False
            if 'LIST FRAMES' in strInput:
               path = self.cParams.displayHandler.strFramePath
               fileList = os.listdir(path)
               listIndexi = []
               if fileList != []:
                  for f in fileList:
                     listIndexi.append(int(f[6:-4]))
                  listIndexi.sort()
                  self.cParams.displayHandler.frameIndex = int(listIndexi[-1])
                  print(f'{len(listIndexi)} Frames from: {listIndexi[0]} till {listIndexi[-1]}')
               else:
                  print(f'Path {path} is empty')
               bNotOK = False
            
            if 'DELETEDUPFRAMES' in strInput:
               def TakeSecond(Param):
                  return(int(Param[6:-4]))
               
               listIndexi = []
               path = self.cParams.displayHandler.strFramePath
               fileList = os.listdir(path)
               fileList.sort(key=TakeSecond)
               
               if fileList != []:
                  for f in fileList:
                     listIndexi.append(int(f[6:-4]))
                  
               startIndex = 0
               while startIndex < len(listIndexi) - 2:
                  for indexi in range(startIndex, len(listIndexi) - 2):
                     index1 = listIndexi[indexi]
                     index2 = listIndexi[indexi+1]
                     fileContents1 = cv2.imread(path + f'Frame_{index1}.bmp')   
                     fileContents2 = cv2.imread(path + f'Frame_{index2}.bmp')
                     result, diffContents = self.Diff(fileContents1, fileContents2)
                     if (result == 0):
                        listIndexi.remove(index2)
                        fileToDelete = path + f'Frame_{index2}.bmp'
                        os.remove(fileToDelete)
                        print(f'Frame {index2} removed')
                        break
                     else:
                        startIndex += 1
                        break
            
               bNotOK = False
               pass
            
            if 'DELETE FRAMES' in strInput:
               def TakeSecond(Param):
                  return(int(Param[6:-4]))
               
               path = self.cParams.displayHandler.strFramePath
               fileList = os.listdir(path)
               fileList.sort(key=TakeSecond)
               filesToDelete = []
               print(f'Deleting Frames from: {fileList[0]} till {fileList[-1]}')

               for f in fileList:
                  filesToDelete.append(f)
                  print(f'Deleting frame {f}: Y/N')
                  strInput = input()
                  if (strInput.upper() == 'Y'):
                     fileToDelete = path+f
                     os.remove(fileToDelete)
                     print('Frame {f} removed',end='')
                  else:
                     continue
               bNotOK = False

            if 'DELETE ALL FRAMES' in strInput:
               path = self.cParams.displayHandler.strFramePath
               fileList = os.listdir(path)
               print(f'Deleting All Frames from: {fileList[0]} till {fileList[-1]}')
               for f in fileList:
                  fileToDelete = path+f
                  os.remove(fileToDelete)
                  print(f'Frame {f} removed')
                  pass
               pass
               bNotOK = False
               
            if ('LOADFRAME') in strInput:
               if (len(strInput) < 10):
                  print('Invalid index')
               else:   
                  frameIndex = int(strInput[10:])
                  strFramePath = self.cParams.displayHandler.strFramePath + f'Frame_{frameIndex}.bmp'
                  self.cParams.bPictureAlive = False
                  self.cParams.displayHandler.strLoadedFramePath = strFramePath
                  self.cParams.displayHandler.bLoadedFrameActive = True
                  frameContents = cv2.imread(strFramePath)
                  h,w,c = frameContents.shape
                  self.cParams.displayHandler.ResizeDisplayHandler(w,h)
               bNotOK = False
               pass
            
            if ('CONTINUATION ON') in strInput:
               self.cParams.displayHandler.bContinueActive = True
               self.cParams.displayHandler.bLoadedFrameActive = True
               bNotOK = False
               pass
            if ('CONTINUATION OFF') in strInput:
               self.cParams.displayHandler.bContinueActive = False
               self.cParams.displayHandler.bLoadedFrameActive = False
               bNotOK = False
               pass
            if ('DIFFFRAMES ON') in strInput:
               self.cParams.displayHandler.bDiffActive = True
               self.cParams.displayHandler.bLoadedFrameActive = True
               bNotOK = False
               pass
            if ('DIFFFRAMES OFF') in strInput:
               self.cParams.displayHandler.bDiffActive = False
               self.cParams.displayHandler.bLoadedFrameActive = False
               bNotOK = False
               pass
            
            if ('DIFFSFRAME ') in strInput:
               lastIndex = strInput.rfind(' ')
               self.cParams.displayHandler.strLoadedFramePath = self.cParams.displayHandler.strFramePath
               self.cParams.displayHandler.diffFirstFrameIndex = int(strInput[10:lastIndex])
               self.cParams.displayHandler.diffSecondFrameIndex = int(strInput[lastIndex:])
               self.cParams.displayHandler.firstFramePath = self.cParams.displayHandler.strFramePath + \
                                       f'Frame_{self.cParams.displayHandler.diffFirstFrameIndex}.bmp'
               self.cParams.displayHandler.secondFramePath = self.cParams.displayHandler.strFramePath + \
                                       f'Frame_{self.cParams.displayHandler.diffSecondFrameIndex}.bmp'
               self.cParams.displayHandler.bDiffS1Active = True
               self.cParams.displayHandler.bDiffS2Active = False
               self.cParams.displayHandler.bDiffSActive = True
               self.cParams.displayHandler.bLoadedFrameActive = False
               bNotOK = False
               pass
            if ('DIFFSFRAME1') in strInput:
               self.cParams.displayHandler.bDiffS1Active = True
               self.cParams.displayHandler.bDiffS2Active = False
               self.cParams.displayHandler.bDiffSActive = True
               bNotOK = False
               pass
            if ('DIFFSFRAME2') in strInput:
               self.cParams.displayHandler.bDiffS2Active = True
               self.cParams.displayHandler.bDiffS1Active = False
               self.cParams.displayHandler.bDiffSActive = True
               bNotOK = False
               pass
            if ('UNLOADFRAME') in strInput:
               self.cParams.bPictureAlive = False
               self.cParams.displayHandler.strLoadedFramePath = ''
               self.cParams.displayHandler.bLoadedFrameActive = False
               bNotOK = False
               pass
            if ('RECORDING ON') in strInput:
               self.cParams.bRecording = True
               self.bRecording = True
               self.cParams.displayHandler.bRecording = True
               bNotOK = False
               pass            
            if ('RECORDING OFF') in strInput:
               self.cParams.bRecording = False
               self.bRecording = False
               self.cParams.displayHandler.bRecording = False
               bNotOK = False
               pass            
            if ('SAVESINGLEIMAGE ON') in strInput:
               self.bSaveSingleImage = True
               bNotOK = False
               pass            
            if ('SAVESINGLEIMAGE OFF') in strInput:
               self.bSaveSingleImage = False
               bNotOK = False
               pass            
            if ('TRIGGERDISPLAYHANDLER') in strInput:
               self.cParams.displayHandler.TriggerKeyWait()
               bNotOK = False
               pass            
            if ('ANALYSFRAME') in strInput:
               if not self.bAnalysFrameActive:
                  self.cParams.analysFrameHandler = threading.Thread(target=CAnalysFrame,args = (self.cParams,))
                  self.cParams.analysFrameHandler.start()
                  self.bAnalysFrameActive = True
                  print(f'{self.cParams.terminalColors["green"]}')
                  print('AnalysFrameHandler Started')
               else:
                  print('Frame Handler is already Active')
               bNotOK = False
               pass            
            if bNotOK:
                print('Invalid Command')
                continue

         except ValueError as e:
            print(f'Error: {e}. Please enter a valid value.')
         except Exception as e:
            print(f'Error: {e}')
 
      print('Program Finished!')
 
#************** For testing ***************
#if __name__ == '__main__':
#    cc_handler = CCHandler()
#    cc_handler.ShowHelp()
#   cc_handler.CommandHandler()
 

