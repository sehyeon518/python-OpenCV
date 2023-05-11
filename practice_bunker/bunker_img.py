import cv2
import numpy as np

src = cv2.imread('/home/sehyeon/Documents/GitHub/python-OpenCV/practice_bunker/bunker_1.jpg')
src = cv2.GaussianBlur(src, ksize=(11,11), sigmaX = 10.0)
src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

# cvt color -> black or white
dst1 = cv2.inRange(src, (200, 200, 200), (255, 255, 255)) # 1. BGR
# dst2 = cv2.inRange(src_hsv, (0, 0, 90), (200, 0, 100))    # 2. HSV

cv2.imshow('src', src)
cv2.imshow('dst1', dst1)

cv2.waitKey()
cv2.destroyAllWindows()