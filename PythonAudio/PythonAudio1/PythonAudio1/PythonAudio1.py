import pyaudio
import wave
import numpy as np
#import utility
import cv2


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.setWindowTitle('image','Signal Picture')
cv2.moveWindow('image', 0, 0)
cv2.resizeWindow('image', 1024, 256)
img = cv2.imread('c:\pc2324\Images\Audio.bmp',cv2.IMREAD_UNCHANGED)
cv2.imshow('image',img)
height, width, channels = img.shape

h = 128

for i in range(0,1023):     # we are thinking in bytes
   img[h,i,0] = 255
   img[h,i,1] = 255
   img[h,i,2] = 255

cv2.imshow('image',img)



p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

    data = stream.read(CHUNK)
    if (i == 1):
       print('len: ')
       print(len(data))
       print('\r\n')
       print('Data: ')
       print(data)
       print('\r\n')

    sig = np.frombuffer(data, dtype='<i2').reshape(-1, 2)
    print(sig)
    frames.append(data)
    if (i == 1):
       print(frames)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()