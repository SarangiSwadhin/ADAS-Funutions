import cv2
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO
##############################################    STEPS FOR LANE DETECTION IN A VIDEO   ############################################
##Frame by frame start reading the video and displaying it
model = YOLO('yolov8n.pt')

vid = cv2.VideoCapture("vid.mp4")
if vid.isOpened() == False:
    print("The video is not opening")

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
    
    for x1,y1,x2,y2 in left_lines:
        cv2.line(vid_det, (x1,y1),(x2,y2),(0,255,0),5)
    for x1,y1,x2,y2 in right_lines:
        cv2.line(vid_det, (x1,y1),(x2,y2),(255,0,0),5)

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