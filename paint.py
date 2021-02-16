import cv2
import numpy as np
frameWidth = 720
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

low_gr = np.array([0,255,0])
high_gr = np.array([0,255,0])

low_pink = np.array([251,143,255])
high_pink = np.array([251,143,255])

myColors = [[38,16,51,82,177,81],
            [168,129,59,178,181,255]
            ]
myColorValues = [[0,255,0],          ## BGR
                 [251,143,255]]

myPoints =  []  ## [x , y , colorId ]

def renkbul(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),15,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1

        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        alan = cv2.contourArea(cnt)
        if alan > 800:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def ciz(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 12, myColorValues[point[2]], cv2.FILLED)



def kosebul(img):
    contours,hie = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        alan = cv2.contourArea(cnt)

        if alan > 1800:
            cv2.drawContours(new, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            print("PERİ = " , peri)
            approx = cv2.approxPolyDP(cnt,0.04*peri,True)
            print("Approx = " , len(approx))
            objKose = len(approx)
            print(objKose)
            x , y , w , h = cv2.boundingRect(approx)

            if objKose == 3:
                objType = "Ucgen"
            elif objKose == 4:
                oran = w/float(h)
                if oran > 0.95 and oran < 1.05:
                    objType = "Kare"
                else:
                    objType = "Dikdortgen"
            elif objKose ==5  :
                objType = "Besgen"
            elif objKose == 6 :
                objType = "Altigen"
            elif objKose == 7 :
                objType = "Yedigen"
            elif objKose == 8 :
                objType = "Sekizgen"
            elif objKose > 8 :
                objType = "Bilinmiyor"

            cv2.rectangle(new,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(new,objType,
                        (x+(w//2)-50,y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (255,255,255),2)
    return




while True:
    success, img = cap.read()

    imgResult = img.copy()

    newPoints = renkbul(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        ciz(myPoints,myColorValues)

    imgCont = img.copy()

    green_mask = cv2.inRange(imgResult,low_gr,high_gr)
    green = cv2.bitwise_and(imgResult,imgResult,mask=green_mask)

    pink_mask = cv2.inRange(imgResult,low_pink,high_pink)
    pink = cv2.bitwise_and(imgResult,imgResult,mask=pink_mask)

    new = cv2.addWeighted(pink, 0.8, green, 1.0, 0.)

    imgGS = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGS, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 100, 50)
    imgblack = np.zeros_like(img)

    kosebul(imgCanny)


    cv2.imshow("new",new)

    cv2.imshow("Canny", imgCanny)
    #cv2.imshow("cont",imgCont)
    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break