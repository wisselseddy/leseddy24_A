import threading

class CThread(object):
   def __init__(self,CParams):
      self.threadingLock = threading.Lock()
      self.videoBuffer = CParams.videoBuffer
      self.bActive = False
      pass
   
   def Run(self,Cur, H, W, Channel):
      self.bActive = True
      for w in range(W):
         if (self.videoBuffer[H][w][Channel] > Cur):
            self.videoBuffer[H][w][Channel] = Cur
      self.bActive = False
      




