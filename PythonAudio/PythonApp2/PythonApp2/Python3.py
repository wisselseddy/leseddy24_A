
import pyaudio
import wave
import numpy as np
from numpy.fft import fft, ifft
#import utility
import cv2
import time


CHUNK = 882
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 44100
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "output.wav"

#cv2.namedWindow('image',cv2.WINDOW_NORMAL)
#cv2.setWindowTitle('image','Signal Picture')
#cv2.moveWindow('image', 0, 0)
#cv2.resizeWindow('image', 1024, 256)
#img = cv2.imread('c:\pc2324\Images\Audio.bmp',cv2.IMREAD_UNCHANGED)
#cv2.imshow('image',img)
#height, width, channels = img.shape

# specto init

spectoWidth = 256
spectoHeight = 882
spectoPosX = 20
spectoPosY = 20

WinID = 'Audio spectogram'
cv2.namedWindow(WinID, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WinID, spectoWidth, spectoHeight)
cv2.moveWindow(WinID,spectoPosX, spectoPosY)
background = np.full((spectoHeight,spectoWidth,3),[0,0,0],dtype='uint8')

cv2.imshow(WinID, background) 
#   print('t2: %f ' %(time2-time1))

key = cv2.waitKey(20) & 0xff
if key == 27:
   pass

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,   # microphone aanzetten
                frames_per_buffer=CHUNK)

print('Starting Audio')

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
   print(i)
   fftData = [0] * 882
   data = stream.read(CHUNK)
#   img = cv2.imread('c:\pc2324\Images\Audio.bmp',cv2.IMREAD_UNCHANGED)
   
   for j in range (0, 881,2):
      arr = np.full([256,3], [0,0,0], dtype=np.int16)  
      bData = ((data[j+1] + 128)) & 0xFF
      arr[bData] = [255,255,255];     # Set white point in array for specto
#      print((int)(bData))

      for h in range (1,spectoHeight):
         background[h-1] = background[h]

      background[spectoHeight - 1] = arr
      cv2.imshow('image',background)
      time.sleep(0.001)
      key = cv2.waitKey(1) & 0xff
#      if key == 27:
#         pass

#   cv2.imshow('image',img)
#   cv2.waitKey(20)

print('Audio Stopped')

# Clean termination of all software modules

stream.stop_stream()
stream.close()
p.terminate()
