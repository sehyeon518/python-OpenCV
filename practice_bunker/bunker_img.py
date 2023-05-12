import cv2
import numpy as np


# ROI
isDragging = False                      # 마우스 드래그 상태 저장 
x0, y0, w, h = -1,-1,-1,-1              # 영역 선택 좌표 저장
roi = None

def onMouse(event,x,y,flags,param):     # 마우스 이벤트 핸들 함수  ---①
    global isDragging, x0,y0,w,h, roi, src   # 전역변수 참조
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼 다운, 드래그 시작 ---②
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv2.EVENT_MOUSEMOVE:  # 마우스 움직임 ---③
        if isDragging:                  # 드래그 진행 중
            img_draw = src.copy()       # 사각형 그림 표현을 위한 이미지 복제
            cv2.rectangle(img_draw, (x0, y0), (x, y), (0,0,255), 2) # 드래그 진행 영역 표시
            cv2.imshow('src', img_draw) # 사각형 표시된 그림 화면 출력
    elif event == cv2.EVENT_LBUTTONUP:  # 왼쪽 마우스 버튼 업 ---④
        if isDragging:                  # 드래그 중지
            isDragging = False          
            w = x - x0                  # 드래그 영역 폭 계산
            h = y - y0                  # 드래그 영역 높이 계산
            print("x:%d, y:%d, w:%d, h:%d" % (x0, y0, w, h))
            if w > 0 and h > 0:         # 폭과 높이가 양수이면 드래그 방향이 옳음 ---⑤
                img_draw = src.copy()   # 선택 영역에 사각형 그림을 표시할 이미지 복제
                cv2.rectangle(img_draw, (x0, y0), (x, y), (0,255,255), 2) 
                cv2.imshow('src', img_draw) # 빨간 사각형 그려진 이미지 화면 출력
                roi = src[y0:y0+h, x0:x0+w] # 원본 이미지에서 선택 영영만 ROI로 지정 ---⑥


# img read
src = cv2.imread('/home/sehyeon/Documents/GitHub/python-OpenCV/practice_bunker/bunker_1.jpg')
src = cv2.GaussianBlur(src, ksize=(11,11), sigmaX = 10.0)
cv2.imshow('src', src)
# src_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)


# ROI 바깥 영역을 검정색(0,0,0)으로
cv2.setMouseCallback('src', onMouse) # 마우스 이벤트 등록 ---⑧
cv2.waitKey()

if roi is not None:
    mask = np.zeros_like(src)
    mask[:,:] = (255, 255, 255)  # 흰색으로 채움
    mask[y0:y0+h, x0:x0+w] = src[y0:y0+h, x0:x0+w]
    image_with_color = cv2.bitwise_and(src, mask)
    image_with_color[np.where((mask==255).all(axis=2))] = (0, 0, 0)  # 바깥부분을 빨간색으로 채움
    cv2.imshow('mask', image_with_color)


# 밝은 색 추출
# cvt color -> black(255) or white(0) -> grayscale로 자동 변환
dst1 = cv2.inRange(image_with_color, (200, 200, 200), (255, 255, 255)) # 1. BGR
# dst2 = cv2.inRange(src_hsv, (0, 0, 90), (200, 0, 100))    # 2. HSV


# contours
mode = cv2.RETR_LIST
method = cv2.CHAIN_APPROX_SIMPLE
_, contours, hierarchy = cv2.findContours(dst1, mode, method)
cv2.drawContours(dst1, contours, -1, (0,255,255), 3)

# 가장 왼쪽 점과 가장 오른쪽 점 찾기
# x = np.zeros((src.shape[0], 1), dtype=np.uint8) + 255 # (333,1)
leftmost_point = (0,0)
for i in range(src.shape[1]):
    tmp = np.reshape(dst1[:, i], (src.shape[0], -1)) # column (333,1)
    result = (tmp==255)
    indices = np.where(result)[0]
    if len(indices) > 0:
        leftmost_point = (i, int(np.mean(indices)))
        break
    else:
        continue
rightmost_point = (src.shape[1] - 1,0)
for i in range(src.shape[1]-1, 0, -1):
    tmp = np.reshape(dst1[:, i], (src.shape[0], -1)) # column (333,1)
    result = (tmp==255)
    indices = np.where(result)[0]
    if len(indices) > 0:
        rightmost_point = (i, int(np.mean(indices)))
        break
    else:
        continue


cv2.waitKey()
cv2.destroyAllWindows()