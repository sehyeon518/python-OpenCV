import cv2

cap = cv2.VideoCapture(cv2.CAP_DSHOW+0)

def click_event(event, x, y, flags, param):
    global src
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭 이벤트
        cv2.circle(src, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(src, f'({x}, {y})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        print(f'{y}')
        cv2.imshow('Video', src)

# 마우스 클릭 이벤트 콜백 함수 등록
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', click_event)

while True:
    retval, src = cap.read()
    if not retval:
        break

    cv2.imshow("Video", src)
    key = cv2.waitKey(25)
    if key == 27:
       break

cv2.destroyAllWindows()