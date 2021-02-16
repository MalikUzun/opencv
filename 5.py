import cv2
import numpy as np

path = 'resimler/shapes.png'

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def kenarbul(img):
    contours,hie = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        print("Area = " , area)

        if area > 5000:
            cv2.drawContours(imgCont, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            print("PERİ = " , peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print("Approx = " , len(approx))
            objKose = len(approx)
            x , y , w , h = cv2.boundingRect(approx)

            if objKose == 3:
                objType = "Ucgen"
            elif objKose == 4:
                oran = w/float(h)
                if oran > 0.95 and oran < 1.05:
                    objType = "Kare"
                else:
                    objType = "Dikdortgen"
            elif objKose > 4 :
                objType = "Daire"

            cv2.rectangle(imgCont,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgCont,objType,
                        (x+(w//2)-50,y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)

    return


img = cv2.imread(path)

imgCont = img.copy()

imgGS = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGS,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
imgblack = np.zeros_like(img)

kenarbul(imgCanny)

imgStack = stackImages(0.7,([img,imgGS,imgCanny],
                            [imgBlur,imgCont,imgblack]))

cv2.imshow("Stack",imgStack)




cv2.waitKey(0)