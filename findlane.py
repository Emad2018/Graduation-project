# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:42:57 2018

@author: Abd Elrahman
"""

import cv2
import numpy as np
import dep

def find_lane(warped):
 
 
 
 h,w=warped.shape 
 nonzero=warped.nonzero()
 nonzero_y = np.array(nonzero[0])
 nonzero_x = np.array(nonzero[1])
 margin=100

 if  dep.first_time==1:
  
  num_windows=9
  histogram=np.sum(warped[int(h/2):,:],axis=0)
  midpoint=int(h/2)
  win_height=int(h/num_windows)
  left_x_base=np.argmax(histogram[:midpoint])
  right_x_base=np.argmax(histogram[midpoint:])+midpoint
  current_left_x=left_x_base
  current_right_x=right_x_base
  minpix=10
  left_point_ind=[]
  right_point_ind=[]
  for window in range(num_windows):
    win_y_low=h-(window+1)*win_height
    win_y_high=win_y_low+win_height
    x_left_low=current_left_x-margin
    x_left_high=current_left_x+margin
    x_right_low=current_right_x-margin
    x_right_high=current_right_x+margin
    good_left_inds=((win_y_low<nonzero_y) &(win_y_high>nonzero_y)&(x_left_low<nonzero_x)&(x_left_high>nonzero_x)).nonzero()[0]
    good_right_inds = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= x_right_low) & (nonzero_x < x_right_high)).nonzero()[0]
    left_point_ind.append(good_left_inds)
    right_point_ind.append(good_right_inds)
    if len(good_left_inds) > minpix:
     current_left_x = np.int(np.mean(nonzero_x[good_left_inds]))
    if len(good_right_inds) > minpix:        
                current_right_x = np.int(np.mean(nonzero_x[good_right_inds]))
  left_point_ind = np.concatenate(left_point_ind)
  right_point_ind = np.concatenate(right_point_ind)
  leftx = nonzero_x[left_point_ind]
  lefty = nonzero_y[left_point_ind] 
  rightx = nonzero_x[right_point_ind]
  righty = nonzero_y[right_point_ind] 
  if (lefty.size!=0)&(leftx.size!=0):
    dep.left_fit = np.polyfit(lefty, leftx, 2)
  else:
            dep.left_fit=dep.prev_left
  if (righty.size!=0)&(rightx.size!=0):
            dep.right_fit = np.polyfit(righty, rightx, 2) 
  else:
            dep.right_fit=dep.prev_right
  if dep.first_time==1:
            
            dep.prev_left=dep.left_fit
            dep.prev_right=dep.right_fit
            dep.prev_prev_right=dep.right_fit
            dep.prev_prev_left=dep.left_fit
 else:
        # from the next frame of video (also called "binary_warped")
        # It's now much easier to find line pixels!
        
       
        good_left_inds = ((nonzero_x > (dep.left_fit[0]*(nonzero_y**2) + dep.left_fit[1]*nonzero_y + dep.left_fit[2] - margin)) & (nonzero_x < (dep.left_fit[0]*(nonzero_y**2) + dep.left_fit[1]*nonzero_y + dep.left_fit[2] + margin))) 
        good_right_inds = ((nonzero_x > (dep.right_fit[0]*(nonzero_y**2) + dep.right_fit[1]*nonzero_y + dep.right_fit[2] - margin)) & (nonzero_x < (dep.right_fit[0]*(nonzero_y**2) + dep.right_fit[1]*nonzero_y + dep.right_fit[2] + margin)))  

        leftx = nonzero_x[good_left_inds]
        lefty = nonzero_y[good_left_inds] 
        rightx = nonzero_x[good_right_inds]
        righty = nonzero_y[good_right_inds]
        # Fit a second order polynomial to each
        if (lefty.size!=0)&(leftx.size!=0):
            dep.left_fit = np.polyfit(lefty, leftx, 2)
        else:
            dep.left_fit=dep.prev_left
        if (righty.size!=0)&(rightx.size!=0):
            dep.right_fit = np.polyfit(righty, rightx, 2)
        else:
            dep.right_fit=dep.prev_right
 dep.left_fit= (dep.left_fit+dep.prev_left+dep.prev_prev_left)/3
 dep.right_fit=(dep.right_fit+dep.prev_right+dep.prev_prev_right)/3
 dep.prev_prev_right=dep.prev_right
 dep.prev_right=dep.right_fit
 dep.prev_prev_left=dep.prev_left
 dep.prev_left=dep.left_fit
 
 
 
   
