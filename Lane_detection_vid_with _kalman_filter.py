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

#Hough transformation
    vid_hough =cv2.HoughLinesP(vid_roi, 1, np.pi/180, threshold =50, minLineLength =50, maxLineGap =50)
    vid_frames = np.zeros_like(vid_blur)
    if vid_hough is not None:
        for line in vid_hough:
            x1, y1, x2, y2 = line[0]
            cv2.line(vid_frames, (x1,y1), (x2,y2), (255,0,0), 5)
    vid_hough_d =cv2.addWeighted(vid_blur, 0.8, vid_frames,1,0)
    vid_det=frame.copy()
##Ovelapping the lines on the oroginal image
    left_lines=[]
    right_lines=[]
    if vid_hough is not None:
        for lines in vid_hough:
            x1,y1,x2,y2=lines[0]
            if x1==x2:
                continue
            slope = (y2-y1)/(x2-x1)
            if abs(slope) < 0.1:
                continue

            if slope <-0.1:
                left_lines.append((x1,y1,x2,y2))

            elif slope >0.1:
                right_lines.append((x1,y1,x2,y2))
    
    for x1,y1,x2,y2 in left_lines:
        cv2.line(vid_det, (x1,y1),(x2,y2),(0,255,0),5)
    for x1,y1,x2,y2 in right_lines:
        cv2.line(vid_det, (x1,y1),(x2,y2),(255,0,0),5)
    

    cv2.imshow("original frame", frame)
    cv2.imshow("gaussian blur", vid_blur)
    cv2.imshow("Grey frame", vid_grey)
    cv2.imshow("Edge detected frames", vid_edge)
    cv2.imshow("ROI frames", vid_roi)
    cv2.imshow("Hough transformation video", vid_hough_d)
    cv2.imshow("final image", vid_det)
    results =model(frame)   
    a_frame = results[0].plot()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
vid.release()
cv2.destroyAllWindows