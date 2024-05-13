import pyaudio
import wave
import numpy as np
from numpy.fft import fft, ifft
#import utility
import cv2


CHUNK = 882
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 44100
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "output.wav"

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.setWindowTitle('image','Signal Picture')
cv2.moveWindow('image', 0, 0)
cv2.resizeWindow('image', 1024, 256)
img = cv2.imread('c:\pc2324\Images\Audio.bmp',cv2.IMREAD_UNCHANGED)
cv2.imshow('image',img)
height, width, channels = img.shape


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
h = 128
print('Starting Audio')
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
   fftData = [0] * 882
   data = stream.read(CHUNK)
   img = cv2.imread('c:\pc2324\Images\Audio.bmp',cv2.IMREAD_UNCHANGED)
   for j in range (0, 881,2):
       bData = ((data[j+1] + 128)) & 0xFF
       
       
       img[bData,j,0] = 255
       img[bData,j,1] = 255
       img[bData,j,2] = 255
       fftData[int(j/2)]=bData

   fftX = fft(fftData) 

   print(len(fftX))

   cv2.imshow('image',img)
   cv2.waitKey(20)

print('Audio Stopped')
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
cv2.destroyAllWindows()

arr = np.empty(1024, dtype=np.int16) 
bytestream = arr.tobytes()

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

stream.write(bytestream)
stream.stop_stream()
stream.close()
p.terminate()

#wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#wf.setnchannels(CHANNELS)
#wf.setsampwidth(p.get_sample_size(FORMAT))
#wf.setframerate(RATE)
#wf.writeframes(b''.join(frames))
#wf.close()