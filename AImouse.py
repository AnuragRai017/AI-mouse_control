import cv2
import numpy as np
import Tracking as Ht
import time
import autopy

############################
wCam,hCam = 640,720
frameR = 100
smoothing = 7
###########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
decorator = Ht.handDetector(maxHands=1)
wscr, hscr = autopy.screen.size()
# print(wscr)

while True:
    success, img = cap.read()
    img = decorator.findHands(img)
    lmList, bbox = decorator.findPosition(img)

    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2 ,y2 = lmList[11][1:]
        print(x1, x2,y1,y2)

        fingers = decorator.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        if fingers[1]==1 and fingers[2]==0:


            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wscr))
            y3 = np.interp(y1, (0, hCam-frameR), (0, hscr))
            clocX = plocX + (x3- plocX) / smoothing
            clocY = plocY + (y3 - plocY) / smoothing

            autopy.mouse.move(wscr-x3,y3)
            cv2.circle(img,(x1,y1), 15 ,(255,255,0),cv2.FILLED)
            plocX , plocY = clocX ,clocY

        if fingers[1] == 1 and fingers[2] == 1:
            length, img , lineInfo = decorator.findDistance(8, 12 ,img)
            if length<39:
                cv2.circle(img,(lineInfo[4], lineInfo[5]),15,(0,255,255),cv2.FILLED)
                autopy.mouse.click()

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3)

    cv2.imshow("Image Of Hand", img)
    cv2.waitKeyEx(1)