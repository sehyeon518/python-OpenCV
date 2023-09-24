import cv2
import numpy as np

img = cv2.imread('practice_bunker\\bunker_3.jpg')
img = cv2.resize(img, (200, 200))

cv2.namedWindow('HLS Image')

# 트랙바 콜백 함수
def update_hls(value):
    # 트랙바에서 H, L, S 범위 값을 가져오기
    hue_low = cv2.getTrackbarPos('Hue Low', 'HLS Image')
    hue_high = cv2.getTrackbarPos('Hue High', 'HLS Image')
    lightness_low = cv2.getTrackbarPos('Lightness Low', 'HLS Image')
    lightness_high = cv2.getTrackbarPos('Lightness High', 'HLS Image')
    saturation_low = cv2.getTrackbarPos('Saturation Low', 'HLS Image')
    saturation_high = cv2.getTrackbarPos('Saturation High', 'HLS Image')
    
    # 이미지를 HLS 색공간으로 변환
    img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    
    # 색상, 밝기, 채도 범위 설정
    lower_bound = np.array([hue_low, lightness_low, saturation_low])
    upper_bound = np.array([hue_high, lightness_high, saturation_high])
    
    # 범위 내의 픽셀을 마스크로 만들기
    mask = cv2.inRange(img_hls, lower_bound, upper_bound)
    
    # 마스크를 사용하여 이미지 업데이트
    img_result = cv2.bitwise_and(img, img, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 검은색이 아닌 영역을 사각형으로 표시
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 10 or h < 10:
            continue
        cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 초록색 사각형 그리기
        cv2.putText(img_result, f"{w*h}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('src', img_result)
    return w*h


# 트랙바 추가
cv2.createTrackbar('Hue Low', 'HLS Image', 0, 360, update_hls)
cv2.createTrackbar('Hue High', 'HLS Image', 180, 360, update_hls)
cv2.createTrackbar('Lightness Low', 'HLS Image', 135, 255, update_hls)
cv2.createTrackbar('Lightness High', 'HLS Image', 255, 255, update_hls)
cv2.createTrackbar('Saturation Low', 'HLS Image', 0, 255, update_hls)
cv2.createTrackbar('Saturation High', 'HLS Image', 31, 255, update_hls)

cv2.waitKey()
cv2.destroyAllWindows()
