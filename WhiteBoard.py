'''
Virtual WhiteBoard by Rishikesh

github : https://github.com/Rishikesh0005

linkedin: www.linkedin.com/in/rishikesh-n-27b927101 

Full Stack Developer rishikeshpandian
'''


import cv2
import numpy as np

Width = 1080                                              #Set Width of the frame
Height = 1080                                             #Set Heigth of the frame
cap = cv2.VideoCapture(1)                                 # Lapcam id = 0   ;;  Webcam id = 1
cap.set(3, Width)
cap.set(4, Height)
cap.set(10, 150)                                          # ID=10    === BRIGHTNESS ADJUST ACCORDING TO BACKGROUND

colors = [[0, 125, 0, 8, 255, 255],
            [110, 105, 117, 119, 255, 255]]               #HSV COLOR VALUES OF RED AND BLUE  1:3 = MINIMUM   ;; 3:6 = MAXIMUM
drawingcolors = [[0, 0, 255],
                 [255, 255, 255]]                         #Drawing colors;; Red and white from BGR[::]

myPoints = []

#Function to detect the hsv color by comparing with the above range
def colordetect(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = contour(mask)
        cv2.circle(imgResult, (x, y), 5, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]),mask)
    return newPoints

#Function to get the contour tracing
def contour(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


def draw(Points, Values):
    for point in Points:
        if Values[point[2]] == Values[0]:
            cv2.circle(imgResult, (point[0], point[1]), 13, Values[0], cv2.FILLED)  # Draw circleshape with fullyfilled if red is detected
        else:
            cv2.circle(imgResult, (point[0], point[1]), 100, Values[1], cv2.FILLED) #Thickness is 100 if blue and 13 if it is red



while True:
    success, img = cap.read()                     # Convert into frame
    img = cv2.flip(img, 1)                        # Avoid mirror effect
    imgResult = img.copy()
    newPoints = colordetect(img, colors, drawingcolors)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        draw(myPoints, drawingcolors)
    cv2.namedWindow('WhiteBoard', 0)
    cv2.resizeWindow('WhiteBoard', 1080, 1080)     #Set the size of the output window
    cv2.imshow("WhiteBoard", imgResult)
    if cv2.waitKey(1) and 0xFF == ord('q'):        # EXIT CONDITION....................................
        break
