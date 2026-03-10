import cv2
import matplotlib.pyplot as Ply
from ultralytics import YOLO

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
    
    cv2.imshow("YOLO Video Detection", a_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()