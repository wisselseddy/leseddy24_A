from re import X
import win32gui
import threading
import ctypes
import time
import subprocess
import win32console

from CThread import *

#lock = threading.Lock()
#UID = 1

class CParameters(object):
   def __init__(self):
      self.UID = 1
      self.cParams = self
      self.lock = threading.Lock()
      self.handlePythonTerminal = None
      self.listSlidersNames = []
      self.listSlidersColors = []
      self.listSlidersMinMaxCur = []
      self.bAlive = True
      self.bSystemAlive = True
      self.slider_quantity = 3     # default value 
      self.display_width = 640     # default value (VGA)
      self.display_height = 480    # default value
      self.display_posX = 20
      self.display_posY = 20
      self.slider_posX = self.display_posX + self.display_width
      self.slider_posY = self.display_posY
      self.slider_height = self.display_height
      self.slider_width = 500
      self.blueCurrentValue = 128
      self.greenCurrentValue = 128
      self.redCurrentValue = 128
      self.bSliderDebug = False
      self.posStartXPythonTerminal = self.display_posX + self.display_width + self.slider_width
      self.commandHandler = None
      self.displayHandler = None
      self.sliderHandler = None
      self.analysHandler = None
      self.processImageHandler = None
      self.videoServerHandler = None
      self.analysFrameHandler = None
      self.displayWinID = None
      self.bPictureAlive = False
      self.bCameraAlive = False
      self.bSlidersActive = False
      self.cameraIndex = 0
      self.bRGBFilter = False
      self.bRGBFilter1 = False
      self.bRGBFilter2 = False
      self.videoBuffer = None
      self.listCThreads = []
      self.pointID = 1
      self.rule = [-1,-1,-1,-1,-1,-1]
      self.videoArray = None
      self.videoArrayStatus = None
      self.listBorderPoints = []
      self.mainWindowTitle = None
      self.handleMainWindow = -1
      
      #
      # VLA 
      # 

      self.vlaID = 0 
      self.listVLA = []
      self.listVLAPositions = []

      self.bRecording = False      

      for ind in range(10):
         threadHandle = CThread(self)
         self.listCThreads.append(threadHandle)
     
      self.terminalColors = {
         'reset': '\x1b[0m',
         'bold': '\x1b[1m',
         'italic': '\x1b[3m',
         'underline': '\x1b[4m',
         'inverse': '\x1b[7m',
         'black': '\x1b[30m',
         'red': '\x1b[31m',
         'green': '\x1b[32m',
         'yellow': '\x1b[33m',
         'blue': '\x1b[34m',
         'magenta': '\x1b[35m',
         'cyan': '\x1b[36m',
         'white': '\x1b[37m',
         'gray': '\x1b[90m',
         'bright_red': '\x1b[91m',
         'bright_green': '\x1b[92m',
         'bright_yellow': '\x1b[93m',
         'bright_blue': '\x1b[94m',
         'bright_magenta': '\x1b[95m',
         'bright_cyan': '\x1b[96m',
         'bright_white': '\x1b[97m',
         'bg_black': '\x1b[40m',
         'bg_red': '\x1b[41m',
         'bg_green': '\x1b[42m',
         'bg_yellow': '\x1b[43m',
         'bg_blue': '\x1b[44m',
         'bg_magenta': '\x1b[45m',
         'bg_cyan': '\x1b[46m',
         'bg_white': '\x1b[47m',
         'bg_gray': '\x1b[100m',
         'bg_bright_red': '\x1b[101m',
         'bg_bright_green': '\x1b[102m',
         'bg_bright_yellow': '\x1b[103m',
         'bg_bright_blue': '\x1b[104m',
         'bg_bright_magenta': '\x1b[105m',
         'bg_bright_cyan': '\x1b[106m',
         'bg_bright_white': '\x1b[107m'
      }
   
      pass

   def SetTerminalToVT100(self):
      kernel32 = ctypes.WinDLL('kernel32',use_last_error=True)
      kernel32.SetConsoleTitleW('xxxx')
      han = win32console.GetConsoleWindow()
      windowText =  win32gui.GetWindowText(han)
#      time.sleep(2.0)

#      BUF_SIZE = 256
#      buffer = ctypes.create_unicode_buffer(BUF_SIZE)
#      kernel32.GetConsoleTitleW(buffer, BUF_SIZE)
#      strConsoleTitle = buffer.value
      
      hwnd = win32gui.FindWindowEx(0,0,0, 'xxxx')
      handleForOut = ctypes.c_ulong()
      handleForOut = subprocess.STD_OUTPUT_HANDLE
      hStdOut = kernel32.GetStdHandle(handleForOut)
      mode = ctypes.c_ulong()
      mode = win32console.GetConsoleDisplayMode()

      # ret = kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
      # mode.value |= 4
      # ret = kernel32.SetConsoleMode(hStdOut, mode)
      # print(f'\x1b[93mVT100 Mode Set\x1b[0m')

   def GetLock(Params):
      return (Params.lock)
   
   def GetUIDLock(self):
      return (self.cParams.lock)
   
   def IncUID(self):
      return (self.UID) 
   
   def GetUID(self):
      lock = self.cParams.GetLock(self.cParams)
      lock.acquire()
      self.cParams.UID += 1
      self.lock.release()
      return self.cParms.UID
   
   def ReSize(self,Width,Height):
      self.display_width = self.displayHandler.window_width = Width
      self.display_height = self.displayHandler.window_height = Height
      self.slider_posX = self.display_posX + self.display_width
      self.slider_posY = self.display_posY
      self.slider_height = self.display_height
      self.posStartXPythonTerminal = self.display_posX + self.display_width + self.slider_width
      pass

   def changePositionPythonTerminal(self):
      self.posStartXPythonTerminal = self.display_posX + self.display_width + self.slider_width
      self.posHeigthPythonTerminal = self.display_height + 15
      self.widthPytonTerminal = 400          # width of the terminal is a predefined constant
      win32gui.MoveWindow(self.hwndMainWindow, 
                          self.posStartXPythonTerminal, 
                          self.display_posY,
                          self.widthPytonTerminal,                 # TBS
                          self.posHeigthPythonTerminal+25,
                          True)
#      return self.posStartXPythonTerminal + self.widthPytonTerminal
      
   def setSliderWidth(self,width):
      self.sliderWidth = width
   
   def setHandlePythonTerminal(self,han):
      self.handlePythonTerminal = han
      
   def getHandlePythonTerminal(self):
      return self.handlePythonTerminal
   
   def getSlidersNames(self):
      return self.listSlidersNames
   def getSlidersColors(self):
      return self.listSlidersColors
   def getSlidersMinMaxCur(self):
      return self.listSlidersMinMaxCur
   
   def setSlidersnNames(self,List):
      self.listSlidersName = List
   def setSlidersColors(self,List):
      self.listSlidersColors = List
   def setSlidersMinMaxCur(self, List):
      self.listSlidersMinMaxCur = List

   def calcNewParams(self):
      self.slider_posX = self.display_posX + self.display_width
      self.slider_posY = self.display_posY
      self.slider_height = self.display_height

   def setSliderQuantity(self, arg):
      self.slider_quantity = arg

   def getSliderQuantity(self):
      return self.slider_quantity

   def setSliderWidth(self, arg):
      self.slider_width = arg

   def setSliderPosX(self, arg):
      self.slider_posX = arg
   
   def getSliderPosX(self):
      return self.slider_posX

   def setSliderPosY(self, arg):
      self.slider_posY = arg
   
   def getSliderPosY(self):
      return self.slider_posY

   def getSliderHeight(self):
      return self.slider_height
   
   def getSliderWidth(self):
      return self.slider_width

   def getSliderQuantity(self):
      return self.slider_quantity

   def setDisplayWidth(self,arg):
      self.display_width = arg

   def setDisplayHeight(self,arg):
      self.display_height = arg

   def setDisplayPosX(self,arg):
      self.display_posX = arg

   def setDisplayPosY(self,arg):
      self.display_posY = arg

   def getDisplayWidth(self):
      return self.display_width

   def getDisplayHeight(self):
      return self.display_height

   def getDisplayPosX(self):
      return self.display_posX 

   def getDisplayPosY(self):
      return self.display_posY

   def getBlueCurrentValue(self):
      return self.blueCurrentValue

   def setBlueCurrentValue(self, Value):
      self.blueCurrentValue = Value
   
   def getGreenCurrentValue(self):
      return self.greenCurrentValue

   def setGreenCurrentValue(self, Value):
      self.greenCurrentValue = Value

   def getRedCurrentValue(self):
      return self.redCurrentValue

   def setRedCurrentValue(self, Value):
      self.redCurrentValue = Value

   





