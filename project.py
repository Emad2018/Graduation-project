import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import binaryimg as b
import perspective as p
import findlane as fl
import dep
import draw
import drawb
import bluetooth
import serial 

ser = serial.Serial('COM3', 115200, timeout=0,parity=serial.PARITY_EVEN, rtscts=1)

"""port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect(("00:15:83:35:7A:9F", port))"""

dep.left_fit=None
dep.right_fit=None
dep.right_curverad=0
dep.left_curverad =0   
dep.first_time=1
tls=[]
brs=[]


option = {
    'model': 'cfg/tiny-yolo-voc.cfg',
    'load': 'bin/tiny-yolo-voc.weights',
    'threshold': 0.5,
    'gpu': 0
}
tfnet = TFNet(option)

cap=cv2.VideoCapture("vid.mp4")
colors = [tuple(255 * np.random.rand(3)) for i in range(5)]
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
inlane="no"
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('eman.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

while (cap.isOpened()):
    stime = time.time()
    ret, frame = cap.read()
    newframe=frame.copy()
    if ret ==False:
        break
    tls=[]
    brs=[]
    tock=time.time()
    if ret:
        detecteds = tfnet.return_predict(frame)
        for color, detected in zip(colors, detecteds):
            tl = (detected['topleft']['x'], detected['topleft']['y'])
            br = (detected['bottomright']['x'], detected['bottomright']['y'])
            label = detected['label']
            frame = cv2.rectangle(frame, tl, br, color, 7)
            frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            newframe[tl[1]:br[1],tl[0]:br[0],:]=0
            tls.append(tl)
            brs.append(br)
            
        binary=b.binary(newframe)
        warped,m,im=p.perspective_view(binary)
    
        fl.find_lane(warped)
        warpedbinary=drawb.drawbinary(warped,im)
        
        nonzero=warpedbinary.nonzero()
        nonzero_y = np.array(nonzero[0])
        nonzero_x = np.array(nonzero[1])
        y_high=max(nonzero_y)
        x_min=np.min(np.where(warpedbinary[y_high,:]==255))
        x_max=np.max(np.where(warpedbinary[y_high,:]==255))
        shift=((x_min+x_max)/2)-(frame.shape[1]/2)
        
        for i in range(len(tls)):
		   
            
          found=((tls[i][1]<nonzero_y) &(brs[i][1]>nonzero_y)&(tls[i][0]<nonzero_x)&(brs[i][0]>nonzero_x)).nonzero()[0]
          inlane="n"         
          if len(found) > 1:
              result=draw.draw(warped,frame,im,(0,0,255),shift)
              inlane="y"
          elif len(found)==0:
                  result=draw.draw(warped,frame,im,(0,255,0),shift)
                  inlane="n"    
				  
        if len(tls)==0:
           result=draw.draw(warped,frame,im,(0,255,0),shift)
           inlane="x"
        massage=inlane+'%'
        print(massage)
        """sock.send('"')
        sock.send(str(shift))
        sock.send('@')
        sock.send(str(len(tls)))
        sock.send('#')
        sock.send(inlane)
        sock.send('$')"""
        
        ser.write(massage.encode())
   
        cv2.imshow('frame', result)
        print(shift)
        print((len(tls)))
        print(inlane)
        tls=[]
        data3=""
        out.write(result)
        
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    else:
        cap.release()
        cv2.destroyAllWindows()
        break


