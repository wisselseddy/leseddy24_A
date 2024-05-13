import win32gui
import numpy as np
import threading
import ctypes
import time
import subprocess
import win32console
import os
from ctypes import windll, c_int, byref
import curses
import ctypes.wintypes
import cv2



#M = np.array([[np.cos(angle), -np.sin(angle), x0*(1-np.cos(angle))+ y0*np.sin(angle)],
#              [np.sin(angle), np.cos(angle), y0*(1-np.cos(angle))- x0*np.sin(angle)]])

class CParameters(object):
   def __init__(self):
      self.UID = 1
      self.cParams = self
      self.bSystemAlive = True
      self.numOfMotors = 2
      self.motorMaxSpeed = 128.0
      self.motorAcceleration = 0.05        # 1 unit per time unit
      self.motorDeacceleration = -0.1      # 0.5 units per time unit
      self.motorTimeUnit = 100            # timeunit in ms
      self.strFramesPath = 'c:\\ejw\\eindproefSyntra\\Wheels\\'
      # self.bWriteWheels = False
      # self.wheelImages = []
      # print('Storing...')
      # self.roi0 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot0.bmp')
      # self.roi1 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot1.bmp')
      # self.roi2 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot2.bmp')
      # self.roi3 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot3.bmp')
      # self.roi4 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot4.bmp')
      # self.roi5 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot5.bmp')
      # self.roi6 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot6.bmp')
      # self.roi7 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot7.bmp')
      # self.roi8 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot8.bmp')
      # self.roi9 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot9.bmp')
      # self.roi10 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot10.bmp')
      # self.roi11 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot11.bmp')
      # self.roi12 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot12.bmp')
      # self.roi13 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot13.bmp')
      # self.roi14 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot14.bmp')
      # self.roi15 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot15.bmp')
      # self.roi16 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot16.bmp')
      # self.roi17 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot17.bmp')
      # self.roi18 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot18.bmp')
      # self.roi19 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot19.bmp')
      # self.roi20 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot20.bmp')
      # self.roi21 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot21.bmp')
      # self.roi22 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot22.bmp')
      # self.roi23 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot23.bmp')
      # self.roi24 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot24.bmp')
      # self.roi25 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot25.bmp')
      # self.roi26 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot26.bmp')
      # self.roi27 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot27.bmp')
      # self.roi28 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot28.bmp')
      # self.roi29 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot29.bmp')
      # self.roi30 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot30.bmp')
      # self.roi31 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot31.bmp')
      # self.roi32 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot32.bmp')
      # self.roi33 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot33.bmp')
      # self.roi34 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot34.bmp')
      # self.roi35 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot35.bmp')
      # self.roi36 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot36.bmp')
      # self.roi37 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot37.bmp')
      # self.roi38 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot38.bmp')
      # self.roi39 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot39.bmp')
      # self.roi40 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot40.bmp')
      # self.roi41 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot41.bmp')
      # self.roi42 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot42.bmp')
      # self.roi43 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot43.bmp')
      # self.roi44 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot44.bmp')
      # self.roi45 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot45.bmp')
      # self.roi46 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot46.bmp')
      # self.roi47 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot47.bmp')
      # self.roi48 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot48.bmp')
      # self.roi49 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot49.bmp')
      # self.roi50 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot50.bmp')
      # self.roi51 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot51.bmp')
      # self.roi52 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot52.bmp')
      # self.roi53 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot53.bmp')
      # self.roi54 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot54.bmp')
      # self.roi55 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot55.bmp')
      # self.roi56 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot56.bmp')
      # self.roi57 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot57.bmp')
      # self.roi58 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot58.bmp')
      # self.roi59 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot59.bmp')
      # self.roi60 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot60.bmp')
      # self.roi61 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot61.bmp')
      # self.roi62 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot62.bmp')
      # self.roi63 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot63.bmp')
      # self.roi64 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot64.bmp')
      # self.roi65 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot65.bmp')
      # self.roi66 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot66.bmp')
      # self.roi67 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot67.bmp')
      # self.roi68 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot68.bmp')
      # self.roi69 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot69.bmp')
      # self.roi70 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot70.bmp')
      # self.roi71 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot71.bmp')
      # self.roi72 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot72.bmp')
      # self.roi73 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot73.bmp')
      # self.roi74 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot74.bmp')
      # self.roi75 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot75.bmp')
      # self.roi76 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot76.bmp')
      # self.roi77 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot77.bmp')
      # self.roi78 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot78.bmp')
      # self.roi79 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot79.bmp')
      # self.roi80 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot80.bmp')
      # self.roi81 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot81.bmp')
      # self.roi82 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot82.bmp')
      # self.roi83 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot83.bmp')
      # self.roi84 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot84.bmp')
      # self.roi85 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot85.bmp')
      # self.roi86 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot86.bmp')
      # self.roi87 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot87.bmp')
      # self.roi88 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot88.bmp')
      # self.roi89 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot89.bmp')
      # self.roi90 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot90.bmp')
      # self.roi91 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot91.bmp')
      # self.roi92 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot92.bmp')
      # self.roi93 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot93.bmp')
      # self.roi94 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot94.bmp')
      # self.roi95 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot95.bmp')
      # self.roi96 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot96.bmp')
      # self.roi97 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot97.bmp')
      # self.roi98 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot98.bmp')
      # self.roi99 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot99.bmp')
      # self.roi100 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot100.bmp')
      # self.roi101 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot101.bmp')
      # self.roi102 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot102.bmp')
      # self.roi103 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot103.bmp')
      # self.roi104 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot104.bmp')
      # self.roi105 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot105.bmp')
      # self.roi106 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot106.bmp')
      # self.roi107 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot107.bmp')
      # self.roi108 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot108.bmp')
      # self.roi109 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot109.bmp')
      # self.roi110 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot110.bmp')
      # self.roi111 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot111.bmp')
      # self.roi112 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot112.bmp')
      # self.roi113 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot113.bmp')
      # self.roi114 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot114.bmp')
      # self.roi115 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot115.bmp')
      # self.roi116 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot116.bmp')
      # self.roi117 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot117.bmp')
      # self.roi118 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot118.bmp')
      # self.roi119 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot119.bmp')
      # self.roi110 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot110.bmp')
      # self.roi111 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot111.bmp')
      # self.roi112 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot112.bmp')
      # self.roi113 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot113.bmp')
      # self.roi114 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot114.bmp')
      # self.roi115 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot115.bmp')
      # self.roi116 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot116.bmp')
      # self.roi117 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot117.bmp')
      # self.roi118 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot118.bmp')
      # self.roi119 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot119.bmp')
      # self.roi120 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot120.bmp')
      # self.roi121 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot121.bmp')
      # self.roi122 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot122.bmp')
      # self.roi123 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot123.bmp')
      # self.roi124 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot124.bmp')
      # self.roi125 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot125.bmp')
      # self.roi126 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot126.bmp')
      # self.roi127 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot127.bmp')
      # self.roi128 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot128.bmp')
      # self.roi129 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot129.bmp')
      # self.roi130 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot130.bmp')
      # self.roi131 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot131.bmp')
      # self.roi132 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot132.bmp')
      # self.roi133 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot133.bmp')
      # self.roi134 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot134.bmp')
      # self.roi135 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot135.bmp')
      # self.roi136 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot136.bmp')
      # self.roi137 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot137.bmp')
      # self.roi138 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot138.bmp')
      # self.roi139 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot139.bmp')
      # self.roi140 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot140.bmp')
      # self.roi141 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot141.bmp')
      # self.roi142 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot142.bmp')
      # self.roi143 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot143.bmp')
      # self.roi144 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot144.bmp')
      # self.roi145 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot145.bmp')
      # self.roi146 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot146.bmp')
      # self.roi147 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot147.bmp')
      # self.roi148 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot148.bmp')
      # self.roi149 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot149.bmp')
      # self.roi150 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot150.bmp')
      # self.roi151 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot151.bmp')
      # self.roi152 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot152.bmp')
      # self.roi153 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot153.bmp')
      # self.roi154 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot154.bmp')
      # self.roi155 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot155.bmp')
      # self.roi156 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot156.bmp')
      # self.roi157 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot157.bmp')
      # self.roi158 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot158.bmp')
      # self.roi159 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot159.bmp')
      # self.roi160 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot160.bmp')
      # self.roi161 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot161.bmp')
      # self.roi162 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot162.bmp')
      # self.roi163 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot163.bmp')
      # self.roi164 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot164.bmp')
      # self.roi165 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot165.bmp')
      # self.roi166 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot166.bmp')
      # self.roi167 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot167.bmp')
      # self.roi168 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot168.bmp')
      # self.roi169 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot169.bmp')
      # self.roi170 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot170.bmp')
      # self.roi171 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot171.bmp')
      # self.roi172 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot172.bmp')
      # self.roi173 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot173.bmp')
      # self.roi174 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot174.bmp')
      # self.roi175 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot175.bmp')
      # self.roi176 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot176.bmp')
      # self.roi177 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot177.bmp')
      # self.roi178 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot178.bmp')
      # self.roi179 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot179.bmp')
      # self.roi180 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot180.bmp')
      # self.roi181 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot181.bmp')
      # self.roi182 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot182.bmp')
      # self.roi183 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot183.bmp')
      # self.roi184 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot184.bmp')
      # self.roi185 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot185.bmp')
      # self.roi186 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot186.bmp')
      # self.roi187 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot187.bmp')
      # self.roi188 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot188.bmp')
      # self.roi189 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot189.bmp')
      # self.roi190 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot190.bmp')
      # self.roi191 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot191.bmp')
      # self.roi192 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot192.bmp')
      # self.roi193 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot193.bmp')
      # self.roi194 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot194.bmp')
      # self.roi195 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot195.bmp')
      # self.roi196 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot196.bmp')
      # self.roi197 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot197.bmp')
      # self.roi198 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot198.bmp')
      # self.roi199 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot199.bmp')
      # self.roi200 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot200.bmp')
      # self.roi201 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot201.bmp')
      # self.roi202 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot202.bmp')
      # self.roi203 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot203.bmp')
      # self.roi204 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot204.bmp')
      # self.roi205 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot205.bmp')
      # self.roi206 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot206.bmp')
      # self.roi207 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot207.bmp')
      # self.roi208 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot208.bmp')
      # self.roi209 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot209.bmp')
      # self.roi210 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot210.bmp')
      # self.roi211 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot211.bmp')
      # self.roi212 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot212.bmp')
      # self.roi213 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot213.bmp')
      # self.roi214 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot214.bmp')
      # self.roi215 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot215.bmp')
      # self.roi216 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot216.bmp')
      # self.roi217 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot217.bmp')
      # self.roi218 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot218.bmp')
      # self.roi219 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot219.bmp')
      # self.roi210 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot210.bmp')
      # self.roi211 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot211.bmp')
      # self.roi212 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot212.bmp')
      # self.roi213 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot213.bmp')
      # self.roi214 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot214.bmp')
      # self.roi215 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot215.bmp')
      # self.roi216 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot216.bmp')
      # self.roi217 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot217.bmp')
      # self.roi218 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot218.bmp')
      # self.roi219 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot219.bmp')
      # self.roi220 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot220.bmp')
      # self.roi221 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot221.bmp')
      # self.roi222 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot222.bmp')
      # self.roi223 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot223.bmp')
      # self.roi224 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot224.bmp')
      # self.roi225 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot225.bmp')
      # self.roi226 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot226.bmp')
      # self.roi227 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot227.bmp')
      # self.roi228 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot228.bmp')
      # self.roi229 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot229.bmp')
      # self.roi230 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot230.bmp')
      # self.roi231 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot231.bmp')
      # self.roi232 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot232.bmp')
      # self.roi233 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot233.bmp')
      # self.roi234 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot234.bmp')
      # self.roi235 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot235.bmp')
      # self.roi236 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot236.bmp')
      # self.roi237 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot237.bmp')
      # self.roi238 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot238.bmp')
      # self.roi239 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot239.bmp')
      # self.roi240 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot240.bmp')
      # self.roi241 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot241.bmp')
      # self.roi242 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot242.bmp')
      # self.roi243 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot243.bmp')
      # self.roi244 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot244.bmp')
      # self.roi245 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot245.bmp')
      # self.roi246 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot246.bmp')
      # self.roi247 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot247.bmp')
      # self.roi248 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot248.bmp')
      # self.roi249 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot249.bmp')
      # self.roi250 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot250.bmp')
      # self.roi251 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot251.bmp')
      # self.roi252 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot252.bmp')
      # self.roi253 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot253.bmp')
      # self.roi254 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot254.bmp')
      # self.roi255 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot255.bmp')
      # self.roi256 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot256.bmp')
      # self.roi257 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot257.bmp')
      # self.roi258 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot258.bmp')
      # self.roi259 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot259.bmp')
      # self.roi260 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot260.bmp')
      # self.roi261 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot261.bmp')
      # self.roi262 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot262.bmp')
      # self.roi263 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot263.bmp')
      # self.roi264 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot264.bmp')
      # self.roi265 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot265.bmp')
      # self.roi266 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot266.bmp')
      # self.roi267 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot267.bmp')
      # self.roi268 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot268.bmp')
      # self.roi269 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot269.bmp')
      # self.roi270 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot270.bmp')
      # self.roi271 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot271.bmp')
      # self.roi272 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot272.bmp')
      # self.roi273 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot273.bmp')
      # self.roi274 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot274.bmp')
      # self.roi275 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot275.bmp')
      # self.roi276 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot276.bmp')
      # self.roi277 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot277.bmp')
      # self.roi278 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot278.bmp')
      # self.roi279 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot279.bmp')
      # self.roi280 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot280.bmp')
      # self.roi281 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot281.bmp')
      # self.roi282 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot282.bmp')
      # self.roi283 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot283.bmp')
      # self.roi284 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot284.bmp')
      # self.roi285 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot285.bmp')
      # self.roi286 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot286.bmp')
      # self.roi287 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot287.bmp')
      # self.roi288 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot288.bmp')
      # self.roi289 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot289.bmp')
      # self.roi290 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot290.bmp')
      # self.roi291 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot291.bmp')
      # self.roi292 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot292.bmp')
      # self.roi293 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot293.bmp')
      # self.roi294 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot294.bmp')
      # self.roi295 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot295.bmp')
      # self.roi296 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot296.bmp')
      # self.roi297 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot297.bmp')
      # self.roi298 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot298.bmp')
      # self.roi299 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot299.bmp')
      # self.roi300 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot300.bmp')
      # self.roi301 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot301.bmp')
      # self.roi302 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot302.bmp')
      # self.roi303 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot303.bmp')
      # self.roi304 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot304.bmp')
      # self.roi305 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot305.bmp')
      # self.roi306 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot306.bmp')
      # self.roi307 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot307.bmp')
      # self.roi308 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot308.bmp')
      # self.roi309 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot309.bmp')
      # self.roi310 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot310.bmp')
      # self.roi311 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot311.bmp')
      # self.roi312 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot312.bmp')
      # self.roi313 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot313.bmp')
      # self.roi314 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot314.bmp')
      # self.roi315 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot315.bmp')
      # self.roi316 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot316.bmp')
      # self.roi317 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot317.bmp')
      # self.roi318 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot318.bmp')
      # self.roi319 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot319.bmp')
      # self.roi310 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot310.bmp')
      # self.roi311 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot311.bmp')
      # self.roi312 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot312.bmp')
      # self.roi313 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot313.bmp')
      # self.roi314 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot314.bmp')
      # self.roi315 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot315.bmp')
      # self.roi316 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot316.bmp')
      # self.roi317 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot317.bmp')
      # self.roi318 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot318.bmp')
      # self.roi319 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot319.bmp')
      # self.roi320 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot320.bmp')
      # self.roi321 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot321.bmp')
      # self.roi322 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot322.bmp')
      # self.roi323 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot323.bmp')
      # self.roi324 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot324.bmp')
      # self.roi325 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot325.bmp')
      # self.roi326 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot326.bmp')
      # self.roi327 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot327.bmp')
      # self.roi328 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot328.bmp')
      # self.roi329 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot329.bmp')
      # self.roi330 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot330.bmp')
      # self.roi331 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot331.bmp')
      # self.roi332 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot332.bmp')
      # self.roi333 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot333.bmp')
      # self.roi334 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot334.bmp')
      # self.roi335 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot335.bmp')
      # self.roi336 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot336.bmp')
      # self.roi337 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot337.bmp')
      # self.roi338 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot338.bmp')
      # self.roi339 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot339.bmp')
      # self.roi340 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot340.bmp')
      # self.roi341 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot341.bmp')
      # self.roi342 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot342.bmp')
      # self.roi343 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot343.bmp')
      # self.roi344 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot344.bmp')
      # self.roi345 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot345.bmp')
      # self.roi346 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot346.bmp')
      # self.roi347 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot347.bmp')
      # self.roi348 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot348.bmp')
      # self.roi349 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot349.bmp')
      # self.roi350 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot350.bmp')
      # self.roi351 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot351.bmp')
      # self.roi352 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot352.bmp')
      # self.roi353 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot353.bmp')
      # self.roi354 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot354.bmp')
      # self.roi355 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot355.bmp')
      # self.roi356 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot356.bmp')
      # self.roi357 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot357.bmp')
      # self.roi358 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot358.bmp')
      # self.roi359 = cv2.imread(f'C:\\ejw\\EindproefSyntra\\Wheels\\Wheel_rot359.bmp')
      # print('Stored')
      # self.wheelImages=[self.roi0,self.roi1,self.roi2,self.roi3,self.roi4,
      #                   self.roi5,self.roi6,self.roi7,self.roi8,self.roi9,
      #                   self.roi10,self.roi11,self.roi12,self.roi13,self.roi14,
      #                   self.roi15,self.roi16,self.roi17,self.roi18,self.roi19,
      #                   self.roi20,self.roi21,self.roi22,self.roi23,self.roi24,
      #                   self.roi25,self.roi26,self.roi27,self.roi28,self.roi29,
      #                   self.roi30,self.roi31,self.roi32,self.roi33,self.roi34,
      #                   self.roi35,self.roi36,self.roi37,self.roi38,self.roi39,
      #                   self.roi40,self.roi41,self.roi42,self.roi43,self.roi44,
      #                   self.roi45,self.roi46,self.roi47,self.roi48,self.roi49,
      #                   self.roi50,self.roi51,self.roi52,self.roi53,self.roi54,
      #                   self.roi55,self.roi56,self.roi57,self.roi58,self.roi59,
      #                   self.roi60,self.roi61,self.roi62,self.roi63,self.roi64,
      #                   self.roi65,self.roi66,self.roi67,self.roi68,self.roi69,
      #                   self.roi70,self.roi71,self.roi72,self.roi73,self.roi74,
      #                   self.roi75,self.roi76,self.roi77,self.roi78,self.roi79,
      #                   self.roi80,self.roi81,self.roi82,self.roi83,self.roi84,
      #                   self.roi85,self.roi86,self.roi87,self.roi88,self.roi89,
      #                   self.roi90,self.roi91,self.roi92,self.roi93,self.roi94,
      #                   self.roi95,self.roi96,self.roi97,self.roi98,self.roi99,
      #                   self.roi100,self.roi101,self.roi102,self.roi103,self.roi104,
      #                   self.roi105,self.roi106,self.roi107,self.roi108,self.roi109,
      #                   self.roi110,self.roi111,self.roi112,self.roi113,self.roi114,
      #                   self.roi115,self.roi116,self.roi117,self.roi118,self.roi119,
      #                   self.roi120,self.roi121,self.roi122,self.roi123,self.roi124,
      #                   self.roi125,self.roi126,self.roi127,self.roi128,self.roi129,
      #                   self.roi130,self.roi131,self.roi132,self.roi133,self.roi134,
      #                   self.roi135,self.roi136,self.roi137,self.roi138,self.roi139,
      #                   self.roi140,self.roi141,self.roi142,self.roi143,self.roi144,
      #                   self.roi145,self.roi146,self.roi147,self.roi148,self.roi149,
      #                   self.roi150,self.roi151,self.roi152,self.roi153,self.roi154,
      #                   self.roi155,self.roi156,self.roi157,self.roi158,self.roi159,
      #                   self.roi160,self.roi161,self.roi162,self.roi163,self.roi164,
      #                   self.roi165,self.roi166,self.roi167,self.roi168,self.roi169,
      #                   self.roi170,self.roi171,self.roi172,self.roi173,self.roi174,
      #                   self.roi175,self.roi176,self.roi177,self.roi178,self.roi179,
      #                   self.roi180,self.roi181,self.roi182,self.roi183,self.roi184,
      #                   self.roi185,self.roi186,self.roi187,self.roi188,self.roi189,
      #                   self.roi190,self.roi191,self.roi192,self.roi193,self.roi194,
      #                   self.roi195,self.roi196,self.roi197,self.roi198,self.roi199,
      #                   self.roi200,self.roi201,self.roi202,self.roi203,self.roi204,
      #                   self.roi205,self.roi206,self.roi207,self.roi208,self.roi209,
      #                   self.roi210,self.roi211,self.roi212,self.roi213,self.roi214,
      #                   self.roi215,self.roi216,self.roi217,self.roi218,self.roi219,
      #                   self.roi220,self.roi221,self.roi222,self.roi223,self.roi224,
      #                   self.roi225,self.roi226,self.roi227,self.roi228,self.roi229,
      #                   self.roi230,self.roi231,self.roi232,self.roi233,self.roi234,
      #                   self.roi235,self.roi236,self.roi237,self.roi238,self.roi239,
      #                   self.roi240,self.roi241,self.roi242,self.roi243,self.roi244,
      #                   self.roi245,self.roi246,self.roi247,self.roi248,self.roi249,
      #                   self.roi250,self.roi251,self.roi252,self.roi253,self.roi254,
      #                   self.roi255,self.roi256,self.roi257,self.roi258,self.roi259,
      #                   self.roi260,self.roi261,self.roi262,self.roi263,self.roi264,
      #                   self.roi265,self.roi266,self.roi267,self.roi268,self.roi269,
      #                   self.roi270,self.roi271,self.roi272,self.roi273,self.roi274,
      #                   self.roi275,self.roi276,self.roi277,self.roi278,self.roi279,
      #                   self.roi280,self.roi281,self.roi282,self.roi283,self.roi284,
      #                   self.roi285,self.roi286,self.roi287,self.roi288,self.roi289,
      #                   self.roi290,self.roi291,self.roi292,self.roi293,self.roi294,
      #                   self.roi295,self.roi296,self.roi297,self.roi298,self.roi299,
      #                   self.roi300,self.roi301,self.roi302,self.roi303,self.roi304,
      #                   self.roi305,self.roi306,self.roi307,self.roi308,self.roi309,
      #                   self.roi310,self.roi311,self.roi312,self.roi313,self.roi314,
      #                   self.roi315,self.roi316,self.roi317,self.roi318,self.roi319,
      #                   self.roi320,self.roi321,self.roi322,self.roi323,self.roi324,
      #                   self.roi325,self.roi326,self.roi327,self.roi328,self.roi329,
      #                   self.roi330,self.roi331,self.roi332,self.roi333,self.roi334,
      #                   self.roi335,self.roi336,self.roi337,self.roi338,self.roi339,
      #                   self.roi340,self.roi341,self.roi342,self.roi343,self.roi344,
      #                   self.roi345,self.roi346,self.roi347,self.roi348,self.roi349,
      #                   self.roi350,self.roi351,self.roi352,self.roi353,self.roi354,
      #                   self.roi355,self.roi356,self.roi357,self.roi358,self.roi359]

      # pass

      # pass



