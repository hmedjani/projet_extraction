import cv2 as cv
#load images
image1 = cv.imread("1.jpg")
image2 = cv.imread("2.jpg")
#convert to grayscale image
gray_scale1 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
gray_scale2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)
#initialize SIFT object
sift = cv.SIFT_create()
keypoints1, des1 = sift.detectAndCompute(image1,gray_scale1, None)
print('kepypoints1', des1)
keypoints2, des2 = sift.detectAndCompute(image2,gray_scale2, None)
print('keypoints2', des1)

#initialize Brute force matching
bf = cv.BFMatcher(cv.NORM_L1, crossCheck=True)
#match the descriptors
matches = bf.match(des1,des2)
#sort the maches
matches = sorted(matches, key= lambda match : match.distance)
#draw all matches
#matched_imge = cv.drawMatches(image1, keypoints1, image2, keypoints2, matches[:30], None)
matched_imge = cv.drawMatches(gray_scale1, keypoints1, gray_scale2, keypoints2, matches[:30], None)
#show the matched image
cv.imshow("Matching Images", matched_imge)
cv.waitKey(0)