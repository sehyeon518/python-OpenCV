import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('./contours_j.mp4')
previous_contours = []

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # 동영상 끝나면 종료
    if not ret:
        break

    # 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 블러 처리
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 캐니 에지 검출
    edges = cv2.Canny(blur, 20, 150, apertureSize=3)

    # 컨투어 검출
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 현재 프레임에 이전 윤곽선 그리기
    for cnt in previous_contours:
        area = cv2.contourArea(cnt)
        if area < 500:
            continue

        # 컨투어 근사화
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

        # 꼭지점 개수 확인
        if len(approx) != 7:
            continue

        # 컨투어 그리기
        cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 3)

        # 중심점 계산
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            cv2.putText(frame, f"Center: {cx}, {cy}", (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
        # 화살표의 각 점의 좌표 구하기
            for i in range(len(approx)):
                x, y = approx[i][0]
                #  각 점에 빨간색 원 그리기
                cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)
                # 원 옆에 각 점의 좌표 출력
                cv2.putText(frame, f"{x}, {y}", (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
 

    # 컨투어 전처리
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:
            continue

        # 컨투어 근사화
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

        # 꼭지점 개수 확인
        if len(approx) != 7:
            continue

        # 컨투어 그리기
        cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 3)

        # 중심점 계산
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            cv2.putText(frame, f"Center: {cx}, {cy}", (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
        # 화살표의 각 점의 좌표 구하기
            for i in range(len(approx)):
                x, y = approx[i][0]
                #  각 점에 빨간색 원 그리기
                cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)
                # 원 옆에 각 점의 좌표 출력
                cv2.putText(frame, f"{x}, {y}", (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
        previous_contours = contours
 
    # 출력 이미지 크기 조정
    scale_percent = 720 / frame.shape[0]
    width = int(frame.shape[1] * scale_percent)
    height = int(frame.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    # 결과 출력
    cv2.imshow('Arrow Detection', resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()