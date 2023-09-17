import cv2

cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)
while True:
    retval, src = cap.read()
    if not retval:
        break

    cv2.circle(src, (src.shape[1]//2, src.shape[0]//2), 5, (0,0,255), -1)
    cv2.imshow('src', src)
    key = cv2.waitKey(25)
    if key == 27:
       break
cv2.destroyAllWindows()