import dep
import numpy as np
import cv2
def drawbinary(warped,im):
 
 h,w=warped.shape
 ploty = np.linspace(0, warped.shape[0]-1, warped.shape[0] )
 left_fitx = dep.left_fit[0]*ploty**2 + dep.left_fit[1]*ploty + dep.left_fit[2]
 right_fitx = dep.right_fit[0]*ploty**2 + dep.right_fit[1]*ploty + dep.right_fit[2]


 
 dep.pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
 dep.pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
 

 pts = np.hstack((dep.pts_left, dep.pts_right))
 dep.x=np.int_([pts])
 
 cv2.fillPoly(warped, np.int_([pts]), 255)
 
 
 warpedbinary=cv2.warpPerspective(warped, im, (w, h)) 


 return warpedbinary