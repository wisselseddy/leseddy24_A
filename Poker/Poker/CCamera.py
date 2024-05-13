import time
import cv2

class CCamera(object):
   def __init__(self,CParams):
      self.cameraIndex = CParams.cameraIndex                                       # default waarde
      CParams.bCameraAlive = False
      self.cParams = CParams
#      self.camIndex = 0
      self.startTime = time.time_ns()
      self.height = 0
      self.width = 0
      self.channels = 0
      self.camera = cv2.VideoCapture(CParams.cameraIndex)   # default camera
      self.fps = self.camera.get(cv2.CAP_PROP_FPS)
      self.brightness = self.camera.get(cv2.CAP_PROP_FPS)
      bRet, buf = self.camera.read()
      if bRet:
         self.height, self.width, self.channels = buf.shape
      else:
         print('camera %d is not available' % (CParams.cameraIndex))
      self.camera.release()
      self.displayHandler = CParams.displayHandler
      pass
   
   def cameraRunning(self, parms):              
      global startTime
      self.camera = cv2.VideoCapture(self.cParams.cameraIndex)         # 0 is default camera on the laptop, 1 means first USB camera
      bRet = True
     
      while (self.cParams.bCameraAlive):
         bRet, buf = self.camera.read()                 # is this a queuing mechanism ????
         bRet, self.cParams.videoBuffer = self.camera.read()                 # is this a queuing mechanism ????
         h,w,c =buf.shape
         now = time.time_ns()
         self.cParams.displayHandler.setBuf(buf,h,w)
         done = time.time_ns() - now
         pass

#         cv2.imshow('Main Display',buf)
#         k = cv2.waitKey(20) & 0xff 
#        cv2.putText(buf, str((now - startTime) / 1000000), 
#            (20,50), 
#            cv2.FONT_HERSHEY_SIMPLEX,
#            0.8,
#            (220,220,220),
#            2,
#            1)
#         cv2.imshow(self.WinID,buf)     # this is a task for the displayhandler


#         k = cv2.waitKey(20) & 0xff 
#         if k == 27: 
#            cv2.destroyAllWindows()
#            bRet = False
#            break

      self.camera.release()
      print('Camera %d released' % (self.cParams.cameraIndex))
      return 1




