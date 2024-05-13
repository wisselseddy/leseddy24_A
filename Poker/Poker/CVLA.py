class CVLA(object):
   def __init__(self,CParams):
      self.cParams = CParams                          # default waarde
      self.vlaIndex = CParams.vlaID
      CParams.vlaID += 1
      self.currentXPos = -1                           # current position of the line
      self.oldXPos = -1                               # previous position of the line
      self.height = CParams.analysHandler.windowHeight
      self.color = [230,230,230]                      # List of BGR component
      self.listOldVLAData = []                           # Content of line on oldDataIndex
      self.oldVLAXPos = -1                          # 0 - 640 * multiplier
      self.bVisible = False
      self.bActive = False
      self.videoDataArray = CParams.analysHandler.videoArray
      pass

   def DrawVLA(self, XPos):
      if (self.oldVLAXPos != -1 and self.oldVLAXPos != XPos):             # An old vla is existing and not threaded yet,
         for hi in range(self.height): 
            self.videoDataArray[hi][self.oldVLAXPos] = self.listOldVLAData[hi]
            pass
         self.listOldVLAData.clear()
         pass
      
      for hi in range(self.height):
         self.listOldVLAData.append(self.videoDataArray[hi][XPos].copy())    # goede test!!!!
         self.videoDataArray[hi][XPos] = self.color
         pass
      self.oldVLAXPos = XPos
      
        
   def ReDraw(self,XPos):
      self.DrawVLA(self.XPos)


