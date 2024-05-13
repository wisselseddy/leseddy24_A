
#Exersize 1:

    # capture picture from a camera and display it in a window,
    # until you press the escape character in the windows
    
# Exersize 2:
    # put text on video

import time
import cv2
import numpy as np

startTime = time.time_ns()
#camera = cv2.VideoCapture(0)
#bRet, buf = camera.read()
#camera.release()
bRet = 0
buf = np.full((480,640,3),[0,0,0],dtype='b')

print(bRet)
height, width, channel = buf.shape
print(height)
print(width)
print(channel)

def startWindow(winID,strHeading):
    cv2.namedWindow(winID,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winID,width,height)
    cv2.setWindowTitle(winID,'Test Picture')
    cv2.moveWindow(winID, 100, 100)

def cameraRunning(cameraIndex,winID):
    global startTime
    camera = cv2.VideoCapture(cameraIndex)
    bRet = True
    while (bRet):
        bRet, buf = camera.read()
        now = time.time_ns()
    
#        cv2.putText(buf, str((now - startTime) / 1000000), 
#            (20,50), 
#            cv2.FONT_HERSHEY_SIMPLEX,
#            0.8,
#            (220,220,220),
#            2,
#            1)
        cv2.imshow(winID,buf)

        k = cv2.waitKey(0) & 0xff
        print(k)
        if k == 27: 
            cv2.destroyAllWindows()
            bRet = False
            break

if __name__ == '__main__':
    winID = 'Image1'
    startWindow(winID,'Test Picture')
    cameraRunning(1,winID)
