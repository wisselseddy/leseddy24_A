import os
from datetime import datetime
from CParameters import CParameters

class CErrorCode(object):
   def __init__(self,CParams):
      self.errorCodes = dict ({
            0:'SUCCESS',
            1:'ERROR_INVALID_FUNCTION',
            2:'ERROR_FILE_NOT_FOUND',
            3:'ERROR_PATH_NOT_FOUND',
            4:'ERROR_TOO_MANY_OPEN_FILES',
            5:'ERROR_ACCESS_DENIED'})
      
      self.masterFilePath = 'C:\\ejw\\MasterCodes\\ERRORS.txt'
      self.strExtension = self.masterFilePath[-4:]
      
      self.masterFilePath = 'C:\\ejw\\MasterCodes\\ERRORS.txt'

      pass
   
   def BackupMaster(self):
      # Backup Master file before change
      strCopy = f'copy {self.masterFilePath} {self.masterFile[:-4]}' 
      strCopy += datetime.now().strftime("%m_%d_%Y_%H_%M_%S") 
      strCopy += self.strExtension
      os.system(strCopy)

   def SaveToMaster(self):
      # Backup Master file before change
      self.BackupMaster()
      strToWrite = str(self.errorCodes)
      file = open(self.masterFilePath, mode = 'w',closefd = True)
      bRet = file.write(strToWrite)
      bRet = file.close()
      pass
   
   def RestoreFromMaster(self):
      file = open(self.masterFilePath, mode = 'r',closefd = True)
      strFromRead = file.read()
      self.errorCodes = dict(strFromRead) 
      pass
   
   def AddErrorToLocalErrors(self,ErrorDict,BoolSave):
      self.errorCodes += ErrorDict
      if (BoolSave):
         self.SaveToMaster()
      pass
   
   def AddErrorToGlobalErrors(self,ErrorDict):
      self.errorCodes += ErrorDict
      self.SaveToMaster()
      pass
   
   def HandleError(self, ErrorCode):
      try:
         return self.errorCodes[ErrorCode]
      except:
         return('Undefined Error')
     
if __name__ == "__main__":
   errorTest = CErrorCode(CParameters)
   strResult = errorTest.HandleError(0)
   print(strResult)
   strResult = errorTest.HandleError(3)
   print(strResult)
   strResult = errorTest.HandleError(5)
   print(strResult)
   strResult = errorTest.HandleError(6)
   print(strResult)
   strResult = errorTest.HandleError(-1)
   print(strResult)
   
   print('Test Finished !!!')
   



