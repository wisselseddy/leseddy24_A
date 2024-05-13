import win32api
import win32gui
import win32con
import time
hwnd = win32gui.FindWindowEx(0, 0, 0, "Test Picture")
#win32gui.SetWindowText(hwnd,'AAAA')

bRet = win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN,0)
print(bRet)

# bRet = win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 0x32,0)
while(1):
   bRet = win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, (2 << 30) | (3 << 16) | 13,0)
   time.sleep(0.035)
print(bRet)

pass

import os
import win32gui
import win32console
import ctypes
from ctypes import wintypes

# https://learn.microsoft.com/en-us/windows/  \
# win32/api/winuser/nf-winuser-mouse_event

MOUSEEVENTF_LEFTDOWN = 0x02
MOUSEEVENTF_LEFTUP = 0x04

appname = 'Command Prompt'
a= os.system('mode 80,25')                            # not possible in windows 11

strText = []

def enumHandler(hwnd, lParam):
   han = win32console.GetConsoleWindow()
   if win32gui.IsWindowVisible(han):
      windowText =  win32gui.GetWindowText(han)
      strText.append(windowText)
#      win32gui.MoveWindow(han, 500, 10, 1000, 800, True)
   pass

win32gui.EnumWindows(enumHandler, None)

pass




# python -m pip install pywin32
# pip install pypiwin32

import ctypes
import win32api
import win32com.client

hDllUser32 = ctypes.WinDLL('user32.dll')

#ret = hDllUser32.SetCursorPos(40,35)
#ret = hDllUser32.mouse_event(0x02,100,100,0,0)
#ret = hDllUser32.mouse_event(0x04,100,100,0,0)

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.volume = 99

# speaker.Speak("How is it going with you. My age is 25.")

MB_ICONEXCLAMATION = ctypes.c_uint(int("0x30",0))
NULL = None

#ret = hDllUser32.MessageBoxA(NULL,
#                             b'This is a MessageBox wrapping MessageBoxA()',
#                             b'Message Box Test',
#                             MB_ICONEXCLAMATION)

del hDllUser32;

import win32gui
titles = []
countVis = 0
countTotal = 0

def EachWindow(hwnd,lParam):
   global titles, countTotal,countVis
   countTotal += 1
   class_name = win32gui.GetClassName(hwnd)
   print('class_name: ' + class_name)
   if (win32gui.IsWindowVisible(hwnd)):
      windowText =  win32gui.GetWindowText(hwnd)
      
      titles.append(windowText)
      countVis += 1
   else:
      windowText =  win32gui.GetWindowText(hwnd)
      bVisible = win32gui.IsWindowVisible(hwnd)
      bEnabled = win32gui.IsWindowEnabled(hwnd)
      if (not bEnabled):
         win32gui.EnableWindow(hwnd)
      if (not bVisible):
         win32gui.SetForegroundWindow(hwnd)
      bEnabled = win32gui.IsWindowEnabled(hwnd)
      x1,y1,x2,y2 = win32gui.GetWindowRect(hwnd)
      titles.append(windowText)
      countVis += 1
   pass

# C++ definition
#
#   typedef struct _DISPLAY_DEVICEA {
#            DWORD cb;                 # size in bytes of the structure
#            CHAR  DeviceName[32];     # Identify the device name adaptor/monitor
#            CHAR  DeviceString[128];  # The device context string with is a description
#            DWORD StateFlags;         # DISPLAY_DEVICE_ACTIVE, DISPLAY_DEVICE_MIRRORING_DRIVER
                                       # DISPLAY_DEVICE_MODESPRUNED, DISPLAY_DEVICE_PRIMARY_DEVICE
                                       # DISPLAY_DEVICE_REMOVABLE, DISPLAY_DEVICE_VGA_COMPATIBLE
#            CHAR  DeviceID[128];      # DeviceID  (Not used)
#            CHAR  DeviceKey[128];     # DeviceKey (Reserved)
#   } DISPLAY_DEVICEA, *PDISPLAY_DEVICEA, *LPDISPLAY_DEVICEA;

class DISPLAY_DEVICEW(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('DeviceName', wintypes.WCHAR * 32),
        ('DeviceString', wintypes.WCHAR * 128),
        ('StateFlags', wintypes.DWORD),
        ('DeviceID', wintypes.WCHAR * 128),
        ('DeviceKey', wintypes.WCHAR * 128)
    ]

   
if __name__ == '__main__':
   EnumDisplayDevices = ctypes.windll.user32.EnumDisplayDevicesW
   EnumDisplayDevices.restype = ctypes.c_bool
   displays = []           # to store display information
   iDevNum = 0             # iteration variable for 'iDevNum'
   jMonNum = 0
   
   while(True):
      INFO = DISPLAY_DEVICEW()     # struct object (initiation of structure)
      INFO.cb = ctypes.sizeof(INFO)
      MONITOR_INFO = DISPLAY_DEVICEW()     # struct object (initiation of structure)
      MONITOR_INFO.cb = ctypes.sizeof(MONITOR_INFO)
      if not EnumDisplayDevices(None, iDevNum, ctypes.byref(INFO), 0):
         break       # break as soon as False is returned by 'EnumDisplayDevices'

      while EnumDisplayDevices(INFO.DeviceName,jMonNum,ctypes.byref(MONITOR_INFO),0):
         print("monitor name:\t\t",MONITOR_INFO.DeviceName,'\n\n')
         jMonNum+=1

      displays.append(INFO)       # append information to the list
      iDevNum += 1
       # display information in a sequential form
   for x in displays:
      print('DeviceName:\t\t', x.DeviceName)
      print("DeviceString:\t", x.DeviceString)
      print("StateFlags:\t\t", x.StateFlags)
      print("DeviceID:\t\t", x.DeviceID)
      print("DeviceKey:\t\t", x.DeviceKey)
      print(), print()
      
   win32gui.EnumWindows(EachWindow, None)

   print('Visible: %d' % countVis)
   print('Total: %d' % countTotal)
   for i in range(countVis):
      print(titles[i])
      