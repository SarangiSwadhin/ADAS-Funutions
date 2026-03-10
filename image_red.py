import cv2
import matplotlib.pyplot as plt
##reading an image
image = cv2.imread("image.jpg")
if image is None:
    print("error. no image loaded")

##obataining the height, width and channels of an image and calculating the pixals
(h, w, c) = image.shape
print(f"height {h}, width {w}, channels {c}".format(h, w, c))
pixals = h*w
print(f"the number of pixals are" ,pixals)

##extracting the pixal values of the image
(b, g, r)= image[211, 199]
print(f"blue {b}, green {g}, red {r}",(b, g, r))

##extracting a region from the image
extracted_image= image[250:2000 ,223:2580]

##image resizing
image_resize= cv2.resize(image, (3000, 3000))

##plaotting of image along with the axix
##plt.imshow(image)
##plt.imshow(extracted_image)
plt.imshow(image_resize)
plt.axis("on")
plt.show()