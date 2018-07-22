# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 08:27:58 2018

@author: Abd Elrahman
"""

import cv2
import numpy as np

def perspective_view(img,show=False):

   
    h, w = img.shape[:2]
    # tr
    src=np.float32(
    [[200,img.shape[0]-1],
    [565,470],
    [600,470],
    [1100,img.shape[0]-1]
        ])
    dst=np.float32(
    [[100,img.shape[0]-1],
    [100,0],
    [1000,0],
    [1000,img.shape[0]-1]
        ])
    src=np.float32([[100,img.shape[0]-1],[400,340],
    [600,340],
    [1000,img.shape[0]-1]])
    src=np.float32([[300,img.shape[0]-1],[600,480],
    [780,480],
    [1150,img.shape[0]-1]])
    
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)

    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)
    if show:
        cv2.imshow("perspective_view",warped)
        if cv2.waitKey(30)==ord('q'):
            cv2.destroyAllWindows()
    return warped,M,Minv
   
        



  