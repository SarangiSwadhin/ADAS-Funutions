import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
##Image testing

# image = cv2.imread("image_yolo.jpg")
# model = YOLO('yolov8n.pt')

# results =model(image)
# a_image = results[0].plot()

# a_image = cv2.cvtColor(a_image, cv2.COLOR_BGR2RGB)

# plt.imshow(a_image)
# plt.show()


## Video testing

model = YOLO("yolov5n.pt")

vid = cv2.VideoCapture("yolo.mp4")

if vid.isOpened() == False:
    print("Error opening the video")

while True:
    ret, frame= vid.read()

    if not ret:
        break

    results = model(frame)

    a_frame = results[0].plot()

       # show frame
    cv2.imshow("YOLO Video Detection", a_frame)

    # press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release video
vid.release()

# close all windows
cv2.destroyAllWindows()

