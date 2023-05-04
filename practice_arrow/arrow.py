import cv2
import numpy as np

cap = cv2.VideoCapture('/home/sehyeon/Documents/GitHub/python-OpenCV/practice_arrow/arrow.mp4')


while True:
    retval, src = cap.read()
    if not retval:
        break

    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9) ,0)

    edges = cv2.Canny(blur, 50, 100)

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180.0, threshold=30)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(src, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    cv2.imshow('blur', src)

    key = cv2.waitKey(25)
    if key == 27:
        break

cv2.destroyAllWindows()


