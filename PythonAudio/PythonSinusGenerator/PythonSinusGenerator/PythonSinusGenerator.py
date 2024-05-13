import pyaudio
import wave
import numpy as np
from numpy.fft import fft, ifft
#import utility
import cv2
import math
#from Graph4 import * 
from Graph5 import *

# We are making a sinus generator 
# in a specific window

# make the window

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.setWindowTitle('image','Signal Picture')
cv2.moveWindow('image', 100, 100)
cv2.resizeWindow('image', 640, 350)
img = cv2.imread('c:\pc2324\Images\dummyA.bmp',cv2.IMREAD_UNCHANGED)
cv2.imshow('image',img)
cv2.waitKey(20)

height, width, channels = img.shape

DURATION = 5    # 5 seconds
FREQUENCY = 8000
SAMPLE_RATE = 44100
AMPLITUDE_MAX = 32767.0
AMPLITUDE_MAX_2 = 255
CURRENT_AMPLITUDE = 30000.0
CURRENT_AMPLITUDE_2 = 150
#CHUNK = 882
FORMAT = pyaudio.paInt16
CHANNELS = 1 

#RECORD_SECONDS = 30
#WAVE_OUTPUT_FILENAME = "output.wav"

CONST = 2 * math.pi / SAMPLE_RATE * FREQUENCY
CONST2 = 2 * math.pi / SAMPLE_RATE * 1.0

dataArray = np.empty(44100, dtype=np.int16) 
sinusArray = np.empty(44100, dtype=np.int16)

for r in range(0,44100):
   alpha = CONST * r
   value = math.sin(alpha) * CURRENT_AMPLITUDE
   dataArray[r] = value

for r in range(0,44100):
   alpha = CONST2 * r
   value = math.sin(alpha) * CURRENT_AMPLITUDE_2 + 150
   sinusArray[r] = value

a = max(sinusArray)

#print(dataArray)

#arr = np.empty(1024, dtype=np.int16) 
#bytestream = arr.tobytes()

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=1,
                rate=SAMPLE_RATE,
                output=True,
                frames_per_buffer=44100)

for a in range(0,DURATION):
   stream.write(dataArray)
   print(type(dataArray))
   print(len(dataArray))
   DrawFFTContinuous(img,dataArray)
   cv2.imshow('image',img)
   cv2.waitKey(20)
   
stream.stop_stream()
stream.close()
p.terminate()

wConst = 44100.0 / FREQUENCY

dataIndex = 0
for displayIndex in range (0,640):
   heightValue = int(sinusArray[dataIndex])
   img[heightValue,displayIndex,0] = 0
   img[heightValue,displayIndex,1] = 0
   img[heightValue,displayIndex,2] = 0
   dataIndex += int(44100/640* 2) * 1
   while (dataIndex >= 44100):
      dataIndex -= 44100

cv2.imshow('image',img)
cv2.waitKey(20)

arrComplex = np.empty(44010, dtype=np.complex128)
arrDouble = np.empty(44010, dtype=np.double)
arrComplex = fft(dataArray)
arrDouble = np.abs(arrComplex)

arrDoubleMax = max(arrDouble)

arrDisplayConstant = 256.0 / arrDoubleMax
arrDisplay = np.empty(22050,np.uint16)

for cc in range(0, 22050):
   xIndexToDisplay = 0
   toDisplay = 0
   arrDisplay[cc] = arrDisplayConstant * arrDouble[cc]

deltax = 22050.0 / 640.0
intDeltax = int(deltax)

for dx in range(0,640):
      arrValue = 0
      for ix in range(dx * intDeltax, (dx+1) * intDeltax):
         arrValue += int(arrDisplay[ix])
      arrValue += 0.5
      arrValue /= intDeltax
      intValue = int(arrValue)
      if (intValue > 0):
         a=10
      img[300 - intValue * 2,dx,0] = 0
      img[300 - intValue * 2,dx,1] = 0
      img[300 - intValue * 2,dx,2] = 0
      lineEJWColor(img, 300 - intValue * intDeltax, dx,0,dx,(255,128,128))

cv2.imshow('image',img)
cv2.waitKey(0)

cv2.destroyAllWindows()





