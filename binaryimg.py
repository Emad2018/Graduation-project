# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 18:55:32 2018

@author: Abd Elrahman
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:59:37 2018

@author: Abd Elrahman
"""

import cv2
import numpy as np 

def yellow_thresh(frame,show=False):
    h,w,c=frame.shape
    mask=np.zeros((h,w),np.uint8)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    low_yellow=np.array([0,10,150])
    high_yellow=np.array([30,255,255])
    ymask=cv2.inRange(hsv,low_yellow,high_yellow)
    output=cv2.bitwise_or(mask,ymask,mask=ymask)
    if show:
     cv2.imshow('yellow',output)
     if cv2.waitKey(0)==ord('q'):
      cv2.destroyAllWindows()
    return output  
def gray_thresh(frame,show=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eq_global = cv2.equalizeHist(gray)   
    _, output = cv2.threshold(eq_global, thresh=253, maxval=255, type=cv2.THRESH_BINARY)
    if show:
     cv2.imshow('output',output)
     if cv2.waitKey(0)==ord('q'):
      cv2.destroyAllWindows()
    return output
def white_thresh(frame,show=False):
    h,w,c=frame.shape
    mask=np.zeros((h,w),np.uint8)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HLS)
    low_white=np.array([0,180,0])
    high_white=np.array([255,255,255])
    ymask=cv2.inRange(hsv,low_white,high_white)
    output=cv2.bitwise_or(mask,ymask,mask=ymask)
    if show:
     cv2.imshow('white',output)
     if cv2.waitKey(0)==ord('q'):
      cv2.destroyAllWindows()
    return output  





def binary(img,show=False):
  output1=white_thresh(img,False)
  output2=yellow_thresh(img,False)
  output=cv2.bitwise_or(output2,output1)
  if show:
     cv2.imshow('output',output)
     if cv2.waitKey(30)==ord('q'):
      cv2.destroyAllWindows() 
  return output
 #laplacian=cv2.Laplacian(output,cv2.CV_64F)
 #xgrad=cv2.Sobel(output,cv2.CV_64F,1,0,ksize=3)
 #ygrad=cv2.Sobel(output,cv2.CV_64F,0,1,ksize=3)
 

