# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 23:31:53 2018

@author: Abd Elrahman
"""
import numpy as np
import dep
import cv2
def draw(warped,frame,im,color,shift):

    h,w=warped.shape
    warp_zero = np.zeros_like(warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    cv2.fillPoly(color_warp, dep.x, color)
    newwarp = cv2.warpPerspective(color_warp, im, (w, h)) 
    result = cv2.addWeighted(frame ,1, newwarp, 0.3, 0)
   #distance_px=(float(np.max(np.where(newwarp[-1,:,1]==255))+np.min(np.where(newwarp[-1,:,1]==255)))/2)-(frame.shape[1]/2)
    if shift>0:
      direction='left'
    elif shift<0:
       direction='right'
    else:
       direction='center'
    font = cv2.FONT_HERSHEY_SIMPLEX
    result=cv2.putText(result,'Vehicle is {:.2f}pixels '.format(abs(shift))+direction+' of center',(10,150), font, 2,(255,255,255),2,cv2.LINE_AA)

    return result