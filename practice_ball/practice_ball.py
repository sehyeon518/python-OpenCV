import cv2
import numpy as np

def f(x):
    pass

def detect_using_hough(mask):
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 600, param1 = 250, param2 = 10, minRadius = 0, maxRadius = 50)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            return (i[0], i[1]), i[2]  # (x, y), radius
    return None, None


def detect_using_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # adjust this threshold as needed
            (x,y), radius = cv2.minEnclosingCircle(contour)
            return (x, y), radius
    return None, None

def calculate_distance(radius, known_width, focal_length):
    # distance = (known_width * focal_length) / width
    return (known_width * focal_length) / (2 * radius)  # diameter = 2 * radius

known_ball_diameter = 4.0  # change this to the actual diameter of the ball in centimeters
focal_length = 700  # change this to the focal length of your camera

cap = cv2.VideoCapture("practice_ball\practice_ball.mp4")
if not cap.isOpened():
    print('Error opening video')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1200,800))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([145, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((4, 4), np.uint8)
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)

    # center_hough, radius_hough = detect_using_hough(mask)
    center_contour, radius_contour = detect_using_contours(mask)

    if center_contour and radius_contour:
        cv2.circle(frame, (int(center_contour[0]), int(center_contour[1])), int(radius_contour), (0, 255, 0), 2)  # draw in green
        distance = calculate_distance(radius_contour, known_ball_diameter, focal_length)
        cv2.putText(frame, f"Distance: {distance:.2f}cm", (int(center_contour[0]), int(center_contour[1]-20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # if center_contour and radius_contour:
    #     cv2.circle(frame, (int(center_contour[0]), int(center_contour[1])), int(radius_contour), (255, 0, 0), 2)  # draw in blue
    #     distance = calculate_distance(radius_contour, known_ball_diameter, focal_length)
    #     cv2.putText(frame, f"Distance: {distance:.2f}cm", (int(center_contour[0]), int(center_contour[1]+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)


    cv2.imshow("Frame", frame)
    cv2.imshow("binary", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()