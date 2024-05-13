import time
import cv2
import numpy as np
import win32gui
import sys

import win32gui
import win32api
import win32ui
import win32con
import threading
import socket
import ctypes

from CParameters import CParameters

class CVideoServer(object):
   def __init__(self,CParams,bDisplayBuffer):
      CParams.videoServerHandler = self
      self.cParams = CParams
      self.winID = 'ServerWindow'
      self.strTitle = 'Server Window'
      self.bVideoServerAlive = True
      self.connectionSocket = -1
      self.lockEvent = threading.Event()
      self.lockEvent.clear()
      self.globalDisplayBuffer = np.full((480,640,3),[0,0,0],dtype='uint8')
      self.hwnd = -1
      self.bNoSocket = True
      self.localSocket = None
      self.bNotConnected = True
      self.bFirstConnectionMessage = False
      self.bSendConnectionMessage = False
      self.bDisplayBuffer = False
      self.HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
      self.PORT = 15005  # Port to listen on (non-privileged ports are > 1023)
      self.bFilter1 = False
      self.bSocketOK = True
      
   def DisplayBuffer(self,Params):
      global displayBuffer, bALive
      cv2.namedWindow(self.winID,cv2.WINDOW_NORMAL)
      cv2.resizeWindow(self.winID,640,480)
      cv2.setWindowTitle(self.winID,self.strHeading)
      cv2.moveWindow(self.winID, 900, 600)
      while (True):
         cv2.imshow(self.winID,self.globalDisplayBuffer)
      k = cv2.waitKey(1) & 0xff
   pass

   def RxProcess(self, RefData):
      global globalDisplayBuffer
      print('RxProcess Started')
      locSocket = RefData[socket]
      locAddress = RefData[str]
      locBool = RefData[bool]
      frameCounter = 0
      bLocSocket = True
      while(RefData[bool] and self.bSocketOK):
#      time.sleep(1.0)
#      print('1',end='')
         try:
            receivedData = list(locSocket.recv(640 * 480 * 3))
            if not (receivedData == []):
               # if self.cParams.bRGBFilter:
               #    blueValueIndex = 0
               #    for blueValue in receivedData[0:640 *480 * 3:3]:
               #       if blueValue > 127:
               #          receivedData[blueValueIndex] = 127
               #       blueValueIndex += 3
               #    greenValueIndex = 1
               #    for greenValue in receivedData[1:640 *480 * 3:3]:
               #       if greenValue > 127:
               #          receivedData[greenValueIndex] = 127
               #       greenValueIndex += 3
               #    redValueIndex = 2
               #    for redValue in receivedData[2:640 * 480 * 3:3]:
               #       if redValue > 127:
               #          receivedData[redValueIndex] = 127
               #       redValueIndex += 3
            
               globalDisplayBuffer = np.array(receivedData,dtype='uint8').reshape(480,640,3)
               if self.cParams.bRGBFilter1 or self.cParams.bRGBFilter2:
                  blueCur = (self.cParams.getSlidersMinMaxCur())[0][2]
                  greenCur =  (self.cParams.getSlidersMinMaxCur())[1][2]
                  redCur =  (self.cParams.getSlidersMinMaxCur())[2][2]
                  (B,G,R) = cv2.split(globalDisplayBuffer)
                  if self.cParams.bRGBFilter1:
                     R[R > redCur] = redCur
                     G[G > greenCur] = greenCur
                     B[B > blueCur] = blueCur
                  if self.cParams.bRGBFilter2:
                     R[R < redCur] = 0
                     G[G < greenCur] = 0
                     B[B < blueCur] = 0
                  globalDisplayBuffer = cv2.merge([B,G,R])
               
               self.cParams.videoBuffer = globalDisplayBuffer.copy()
               if self.cParams.displayHandler.bRecordingActive:
                  self.cParams.displayHandler.SaveFrame()
                  print('&',end='')
#               if self.cParams.displayHandler.hwnd != -1:
#                  bRet = win32api.PostMessage(self.cParams.displayHandler.hwnd,
#                                              win32con.WM_KEYDOWN,
#                                              (2 << 30) | (3 << 16) | 13,0)

            else:
               print('Not Data1')      # Connection is interrupted
               RefData[bool] = False
               locSocket.close()
               self.lockEvent.set()    # to release TX thread ???
               continue
            time.sleep(0.005)
            if (bLocSocket):
               locSocket.send(b'\x01\xFE')
#            lockEvent.set()
            
            strTitle = f'   Frame: {frameCounter}'
            strNewMainWindowTitle = self.cParams.mainWindowTitle + strTitle
            win32gui.SetWindowText(self.cParams.hwndMainWindow,strNewMainWindowTitle)
#            print(f'Frame: {frameCounter} \r', end = '')
            frameCounter +=1
            
         except:
            RefData[bool] = False
            bLocSocket = False
            self.lockEvent.set()
            continue
      print('\nRxProcess Ended')
      pass
 
   def TxProcess(self,RefData):
      print('TxProcess Started')
      count = 10
      locSocket = RefData[socket]
      locAddress = RefData[str]
      locBool = RefData[bool]
      counter = 0
      while(RefData[bool]):
#      time.sleep(1.0)
         self.lockEvent.wait()
         counter +=1
         self.lockEvent.clear()
         try:
            locSocket.send(b'\x01\xFE')
            print(f'Freq: {counter} \nCommand: ',end='')
         except:
            RefData[bool] = False
#           RefData[socket].close()
      self.bSocketOK = False
      print('\nTxProcess Ended')
      pass
   
   def EndAcceptance(self):
      self.bVideoServerAlive = False
      endSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
      endSocket.connect((self.HOST,self.PORT))
      endSocket.close()
      pass      

   def Run(self,Params):
      strAliveMessage = 'Alive'

      self.bVideoServerAlive = True

      socketFamily = socket.AF_INET
      socketType = socket.AF_INET
      socketProtocol = socket.IPPROTO_TCP

      localSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
      localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      localSocket.bind((self.HOST, self.PORT))
      localSocket.listen()

      while (self.cParams.bAlive and self.bVideoServerAlive):
         print('VideoServer: Ready to Accept Client')
         conn, addr = localSocket.accept()                  # is waiting for next client
         print('VideoServer: Client Accepted')
         bConnectionAlive = True
#   refData = np.array((bytes(conn),bytes(addr),bytes(bConnectionAlive)))
         refData = dict()
         refData.update({socket:conn,str:addr,bool:bConnectionAlive},)
         rxThread = threading.Thread(target=self.RxProcess,args = (refData,))
         rxThread.start()
         txThread = threading.Thread(target=self.TxProcess,args = (refData,))
         txThread.start()
         if (self.bDisplayBuffer):
            displayThread = threading.Thread(target=self.DisplayBuffer,args = (None,))
            displayThread.start()
            pass
         time.sleep(2.5)
         self.lockEvent.set()
#   while(1):
#      strInput = input()
#      print('-')
#      lockEvent.set()
      print('VideoServer Process Ended!')





