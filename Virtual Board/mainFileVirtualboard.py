from tkinter import *

root = Tk()
def myClick():
    # import the required libraries( cv2 and numpy)
    import cv2
    import numpy as np

    # Setting the video size and shape
    frameWidth = 950
    frameHeight = 1050
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 150)

    # the colors which we are going to detect
    myColorsList = [[40, 104, 86, 116, 255, 255],
                    [0, 133, 135, 23, 255, 255],
                    [66, 136, 17, 102, 255, 67]]

    myColorValues = [[255, 128, 0],
                     [51, 51, 255],
                     [0, 153, 0]]
    myPoints = []

    def findColor(img, myColorsList, myColorValues):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        count = 0
        newPoints = []
        for color in myColorsList:
            lower = np.array(color[0:3])
            upper = np.array(color[3:6])
            mask = cv2.inRange(imgHSV, lower, upper)

            x, y = getContours(mask)
            # cv2.circle(imgResult, (x, y), 5, myColorValues[count], cv2.FILLED)
            if x != 0 and y != 0:
                newPoints.append([x, y, count])
            count += 1
            # cv2.imshow(str(color[0]),mask)
        return newPoints

    def getContours(img):
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

    def drawOnCanvas(myPoints, myColorValues):
        for point in myPoints:
            cv2.circle(imgResult, (point[0], point[1]), 6, myColorValues[point[2]], cv2.FILLED)

    while True:
        success, img1 = cap.read()
        img = cv2.flip(img1, 1)
        imgResult = img.copy()
        newPoints = findColor(img, myColorsList, myColorValues)
        if len(newPoints) != 0:
            for newP in newPoints:
                myPoints.append(newP)
        if len(myPoints) != 0:
            drawOnCanvas(myPoints, myColorValues)

        cv2.imshow("Result", imgResult)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
myButton = Button(root, text="Click Me!", padx=50, pady=10, command=myClick, bg="blue", fg="white")
myButton.pack()




root.mainloop()