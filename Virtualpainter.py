import os

import cv2
import mediapipe as mp
import numpy as np

import handtrackingmodule as htm

detector=htm.handDetector()
foldername="Painter"
filepath=os.listdir(foldername)
list=[]
for path in filepath:
     image=cv2.imread(f"{foldername}/{path}")
     list.append(image)
#print(len(list))
header=list[0]
drawColor= (255,0,255)
brush=15
eraser=70

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
imgOld=np.zeros((720,1280,3),np.uint8)

while True:
    #Image selection
    success, img=cap.read()
    img=cv2.flip(img,1)
    # Hand landmarks
    img=detector.findHands(img)
    llist=detector.findPosition(img)
    if len(llist)!=0:
        #print(llist)
        x1,y1=llist[8][1:]
        x2,y2=llist[12][1:]

        # Checking no. of fingers up
        fingers=detector.FingersUp()
        #print(fingers)

        # Double fingers to select
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            print("Selection Mode")
            if y1<236:
                if 100<x1<350:
                    header=list[0]
                    drawColor=(0,0,255)
                elif 350<x1<700:
                    header=list[1]
                    drawColor=(255,0,0)
                elif 700<x1<950:
                    header=list[2]
                    drawColor=(0,255,0)
                elif 950<x1<1280:
                    header=list[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img, (x1,y1-25), (x2,y2+25), drawColor,cv2.FILLED)
        
        # Single index finger to draw
        if fingers[1] and fingers[2]==False: 
            cv2.circle(img, (x1,y1), 15, drawColor,cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp,yp =x1, y1
            if drawColor==(0,0,0):
                cv2.line(img, (xp,yp), (x1,y1), drawColor, eraser)
                cv2.line(imgOld, (xp,yp), (x1,y1), drawColor, eraser)
            else:
                cv2.line(img, (xp,yp), (x1,y1), drawColor, brush)
                cv2.line(imgOld, (xp,yp), (x1,y1), drawColor, brush)
            
            xp,yp=x1,y1
            
    img[0:236][0:1280]=header
    imgGray=cv2.cvtColor(imgOld,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgOld)
    #img=cv2.addWeighted(img,1,imgOld,1,0)
    cv2.imshow("Image", img)
    #cv2.imshow("ImgOld", imgOld)
    cv2.waitKey(1)  
