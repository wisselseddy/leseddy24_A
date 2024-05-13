import math
import cv2
import numpy as np
from numpy.fft import fft, ifft

def ShowHelp(arg1,arg2):
   print('****************************')
   print(' Valid Command and arguments')
   print('****************************')
   print('Width = nnn            -- Set Window Width')
   print('Height = nnn           -- Set Window Height')
   print('Position = nnn,nnn     -- Set Window Position')
   print('Title = \'xxx...\'       -- Set Window Title')    # shift to cover for \'
   print('Display                -- Display Image')
   print('Display = [Routine]    -- Display Image using [routine]')
   print('Kill                   -- Remove Display')
   print('RGB = bbb,ggg,rrr      -- Set RGB = r,g,b for routine 1')
   print('Routine = n            -- Select Routine n')
   print('Status                 -- Show Settings')
   print('Find Cameras           -- Find all cameras')
   print('Exit')

def StartWindow(WinID, Width, Height, StrTitle, PositionX, PositionY,DisplayBuffer):
    cv2.namedWindow(WinID,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WinID,Width,Height)
    cv2.setWindowTitle(WinID,StrTitle)
    cv2.moveWindow(WinID, PositionX, PositionY)

    cv2.imshow(WinID,DisplayBuffer)
    k = cv2.waitKey(20) & 0xff 



