import cv2
import matplotlib.pyplot as plt
import numpy as np
##############################################    STEPS FOR LANE DETECTION    ############################################
##Reading the image.
##Checking yhe pixla sof the image
##Resizeing the image 
##Adding gausian blur for smoothning the image
##grey scale conversion
##Canny edge detection to detect the edges
##ROI conversion
##Hough transformation
##Drawing lanes on original image. sperate marking of leat and right lanes using slope and averageing

image = cv2.imread("image.jpg")
image_resize = cv2.resize(image, (4096, 2160))
(h,w,r) = image.shape
 
image_blurred = cv2.GaussianBlur(image_resize, (5,5),0)
print(f"height {h}. width {w}, channels {r} dimensions of the normal image")

grey_scaleing = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)
(hg, wg) = grey_scaleing.shape
print(f"height {hg}. width {wg} dimension of grey scaled image" .format(hg,wg))

edge_detection = cv2.Canny(grey_scaleing, 70,200)
mask = np.zeros_like(edge_detection)

polygon = np.array([[(0,h), (0,1600), (2088,976),(4093,1400), (w,h)]], np.int32)
cv2.fillPoly(mask, polygon, 255)
roi_edges = cv2.bitwise_and(edge_detection, mask)

hough_lines = cv2.HoughLinesP(roi_edges, 1,np.pi/180, threshold =50, minLineLength = 100, maxLineGap = 50)
line_image= np.zeros_like(image_resize)
if hough_lines is not None:
    for line in hough_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 5)
lane_image =cv2.addWeighted(image_resize, 0.8, line_image,1,0)

left_lines =[]
right_lines=[]
if hough_lines is not None:
    for line in hough_lines:
        x1,y1,x2,y2 =line[0]
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
    cv2.line(image_resize, (x1,y1),(x2,y2),(0,255,0),5)
for x1,y1,x2,y2 in right_lines:
    cv2.line(image_resize, (x1,y1),(x2,y2),(0,255,0),5)

# plt.figure(figsize=(35,5))

# plt.subplot(1,7,1)
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# plt.title("orginal image")

# plt.subplot(1,7,2)
# plt.imshow(cv2.cvtColor(image_blurred, cv2.COLOR_BGR2RGB))
# plt.title("gaussian blur image")

# plt.subplot(1,7,3)
# plt.imshow(grey_scaleing, cmap ='gray')
# plt.title("grey scaled image")

# plt.subplot(1,7,4)
# plt.imshow(edge_detection)
# plt.title("Canny edge detection")

# plt.subplot(1, 7, 5)
# plt.imshow(roi_edges, cmap='gray')
# plt.title("ROI Edges")

# plt.subplot(1,7,6)
# plt.imshow(cv2.cvtColor(lane_image, cv2.COLOR_BGR2RGB))
# plt.title("Hough Lane Detection")

# plt.subplot(1,7,7)
plt.imshow(cv2.cvtColor(image_resize, cv2.COLOR_BGR2RGB))
plt.title("final image")

plt.tight_layout()
plt.show()