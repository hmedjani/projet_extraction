import os
import cv2 as cv
import matplotlib.pyplot as plt
#print(type(cv)) 
#load image
image = cv.imread("001R_1.png")
#convert to grayscale image
gray_scale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#initialize SIFT object
sift = cv.SIFT_create()
#detect keypoints
keypoints, _descriptors = sift.detectAndCompute(gray_scale, None)
#draw keypoints
sift_image = cv.drawKeypoints(gray_scale, keypoints, None)
# print(keypoints)
###
# Extract keypoint properties
keypoint_sizes = [kp.size for kp in keypoints]
keypoint_angles = [kp.angle for kp in keypoints]

# Create histograms
plt.figure(figsize=(12, 6))

# Histogram for keypoint sizes
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
plt.hist(keypoint_sizes, bins=20, color='blue', alpha=0.7)
plt.title("Histogram of Keypoint Sizes")
plt.xlabel("Size")
plt.ylabel("Frequency")

# Histogram for keypoint angles
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
plt.hist(keypoint_angles, bins=20, color='orange', alpha=0.7)
plt.title("Histogram of Keypoint Angles")
plt.xlabel("Angle (degrees)")
plt.ylabel("Frequency")

# Show the plots
plt.tight_layout()  # Adjusts subplot parameters for better spacing
plt.show()
###
# #show image
# cv.imshow("Features Imagage", sift_image)
# #hold the window
# cv.waitKey(0)
