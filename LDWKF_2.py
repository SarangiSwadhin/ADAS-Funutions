#############################################################################################################################################
#This code is not very efficinent as we are considering only 2 state here that is the slope and the intercept. since the roads has curves and 
# this video is a complex example of lane detection. consider more state such as speed and distance to make it more efficient.
#############################################################################################################################################

import cv2
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO
##############################################    STEPS FOR LANE DETECTION IN A VIDEO   ############################################
##Frame by frame start reading the video and displaying it
model = YOLO('yolov8n.pt')

vid = cv2.VideoCapture("vid_2.mp4")
if vid.isOpened() == False:
    print("The video is not opening")

##Initialiisng the Kalman filter for left and right lanes seperately

kf_left =cv2.KalmanFilter(2,2)
kf_left.transitionMatrix = np.array([[1,0],[0,1]], np.float32)
kf_left.measurementMatrix = np.array([[1,0],[0,1]], np.float32)
kf_left.processNoiseCov =np.eye(2, dtype =np.float32)*5
kf_left.measurementNoiseCov =np.eye(2, dtype =np.float32)
kf_left.errorCovPost =np.eye(2, dtype =np.float32)

kf_right = cv2.KalmanFilter(2,2)
kf_right.transitionMatrix = np.array([[1,0],[0,1]],np.float32)
kf_right.measurementMatrix = np.array([[1,0],[0,1]],np.float32)
kf_right.processNoiseCov =np.eye(2, dtype= np.float32)*5
kf_right.measurementNoiseCov = np.eye(2, dtype =np.float32)
kf_right.processNoiseCov =np.eye(2, dtype = np.float32)

while True:
    ret, frame = vid.read()

    if not ret:
        break
    (h,w,c) = frame.shape
    print(f"width {w}, height {h}, channels {c} Original frames")

    ##Resizeing all the frames

    vid_resize = cv2.resize(frame, (1280, 720))
    (hr,wr,cr) = vid_resize.shape
    print(f"width {wr}, height {hr},channels {cr} Resized frames")

    ##Adding gaussian blue to smoothing the image

    vid_blur = cv2.GaussianBlur(vid_resize, (5,5),0)

    ##Grey sacleing of the image

    vid_grey = cv2.cvtColor(vid_blur, cv2.COLOR_RGB2GRAY)
    (hg,wg) = vid_grey.shape
    print(f"width {wg}, height {hg}, Grey frames")

    ##Apply the canny edge dtection to detect the edges of the object

    vid_edge =cv2.Canny(vid_grey, 50,100)
    
    ##Identifying the region of intrest (ROI)

    mask = np.zeros_like(vid_edge)
    polygon = np.array([[(0,720),(0,500),(750,400),(1280,720)]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    vid_roi = cv2.bitwise_and(mask, vid_edge)

    ##Hough transformation to obain the lines 

    vid_hough = cv2.HoughLinesP(vid_roi, 1, np.pi/180, threshold = 50, minLineLength=50, maxLineGap=50)
    vid_frames = np.zeros_like(vid_blur)
    if vid_hough is not None:
        for line in vid_hough:
            x1, y1, x2, y2 = line[0]
            cv2.line(vid_frames, (x1,y1), (x2,y2), (255,0,0), 5)
    vid_hough_d =cv2.addWeighted(vid_blur, 0.8, vid_frames,1,0)

    vid_det = vid_resize.copy()
    ##Overlapping the lines on the the original image
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
    
    ##Defining the laft and right lanes sperately and passing it into the kalman filter
    left_m=[]
    left_c=[]

    for x1,y1,x2,y2 in left_lines:
        m = (y2-y1)/(x2-x1)
        c = y1 - m*x1
        left_m.append(m)
        left_c.append(c)

    if len(left_m)> 0 and len(left_c) > 0:
        m_left =np.mean(left_m)
        c_left =np.mean(left_c)

        measurement_left = np.array([[np.float32(m_left)],[np.float32(c_left)]])
        prediction_left = kf_left.predict()
        estimated_left = kf_left.correct(measurement_left)
        m_left = float(estimated_left[0][0])
        c_left = float(estimated_left[1][0])

        y1=h
        y2= int(h*0.6)
        if abs(m_left) >0.001:
            x1= int((y1-c_left)/m_left)
            x2 = int((y2-c_left)/m_left)
            cv2.line(vid_det,(x1,y1),(x2,y2),(0,0,255),5)

    right_m=[]
    right_c=[]

    for x1,y1,x2,y2 in right_lines:
        m = (y2-y1)/(x2-x1)
        c = y1 - m*x1
        right_m.append(m)
        right_c.append(c)

    if len(right_m)> 0 and len(right_c) > 0:
        m_right = np.mean(right_m)
        c_right =np.mean(right_c)

        measurement_right = np.array([[np.float32(m_right)],[np.float32(c_right)]])
        preiction_right = kf_right.predict()
        estimated_right = kf_right.correct(measurement_right)
        m_right =float(estimated_right[0][0])
        c_right =float(estimated_right[1][0])

        y1=h
        y2= int(0.6*h)
        if abs(m_left)>0.001:
            x1= int((y1-c_right)/m_right)
            x2 = int((y2-c_right)/m_right)
            cv2.line(vid_det,(x1,y1),(x2,y2),(0,0,255),5) 

    # for x1,y1,x2,y2 in left_lines:
    #     cv2.line(vid_det, (x1,y1),(x2,y2),(0,255,0),5)
    # for x1,y1,x2,y2 in right_lines:
    #     cv2.line(vid_det, (x1,y1),(x2,y2),(255,0,0),5)

    # cv2.imshow("original video", frame)
    # # cv2.imshow("resized video", vid_resize)
    # # cv2.imshow("Blurred video", vid_blur)
    # cv2.imshow("edge detection video", vid_edge)
    # cv2.imshow("ROI video", vid_roi)
    # cv2.imshow("Hough transformation video", vid_hough_d)
    # cv2.imshow("Lane dtection video", vid_det)

    results = model(vid_det)
    a_frame = results[0].plot()
    cv2.imshow("YOLO Video Detection", a_frame)
    if cv2.waitKey(10) & 0xFF == ord("Q"):
        break

vid.release()
cv2.destroyAllWindows()