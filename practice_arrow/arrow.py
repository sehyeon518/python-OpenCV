import cv2
import numpy as np

cap = cv2.VideoCapture('/home/sehyeon/Documents/GitHub/python-OpenCV/practice_arrow/arrow.mp4')
# (720, 1080)

while True:
    retval, src = cap.read()
    cy, cx, _ = src.shape # 1080, 720
    if not retval:
        break

    # cvtColor, blur
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3) ,0)
    
    # 8.6 cv2.goodFeaturesToTrack()
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=10, qualityLevel=0.05, minDistance=30) # type(corners) = numpy.ndarray
    dst = src.copy()
    corners = corners.reshape(-1,2) # reshape -> (X rows) * (2 columns)
    for x, y in corners:
        cv2.circle(dst, (int(x), int(y)), 5, (0,0,255), -1)
    
    cv2.imshow('dst', dst)

    key = cv2.waitKey(25)
    if key == 27:
        break

cv2.destroyAllWindows()


