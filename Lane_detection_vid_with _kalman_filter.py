import cv2
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO

##we wont be resizeing the vidoe in this. resizeing the frame is optional. since w e are using the yolo model on the video. everythimnh will be inside the yolo loop
##Reading the frames form the video. 
model = YOLO('yolov8n.pt')
vid = cv2.VideoCapture("vid.mp4")
if vid.isOpened()==False:
    print("The video is not opening")

while True:
    ret, frame = vid.read()

    if not ret:
        break
    (h,w,c) = frame.shape
    print(f"height {h}, width {w}, channel {c}")


##Applying the gausian blur
    vid_blur = cv2.GaussianBlur(frame, (5,5),0)

##Applying the grey scaleing
    vid_grey = cv2.cvtColor(vid_blur, cv2.COLOR_BGR2GRAY)

##Applying the canny edge detection
    vid_edge = cv2.Canny(vid_grey, 50,100)

##Marking the region on intrets(ROI)
    mask = np.zeros_like(vid_edge) ##Creates a black frame of the same size as that of the vid_edge
    polygon = np.array([[(70,720),(750,400),(1280,720)]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    vid_roi = cv2.bitwise_and(mask, vid_edge)
    
    results =model(frame)   
    a_frame = results[0].plot()
    cv2.imshow("original frame", frame)
    cv2.imshow("gaussian blur", vid_blur)
    cv2.imshow("Grey frame", vid_grey)
    cv2.imshow("Edge detected frames", vid_edge)
    cv2.imshow("ROI frames", vid_roi)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
vid.release()
cv2.destroyAllWindows