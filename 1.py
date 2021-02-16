import cv2
from matplotlib import pyplot as plt
import numpy as np


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



filename = "resimler/avustralya-yol.jpg"
img = cv2.imread(filename) # dosyayi oku

cv2.imshow("Orjinal",img)

im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # grayscale kopya
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # rgb kopya

height = img.shape[0]
width = img.shape[1]

masked_white = cv2.inRange(im,200,255)
blurred = cv2.GaussianBlur(masked_white,(5,5),0.8)
edge_image = cv2.Canny(blurred,50,150)


mask = np.zeros_like(edge_image)
kenarlar = np.array([[(250,height),(250,height/3),(width,height/3),(width,height)]],np.int32)

cv2.fillPoly(mask, kenarlar, 255)


print (edge_image.shape, mask.shape)
masked = cv2.bitwise_and(edge_image, mask)


lines = cv2.HoughLinesP(masked,2,np.pi/180,20,np.array([]),minLineLength=50,maxLineGap=200)
zeros = np.zeros_like(img)


for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(zeros,(x1,y1),(x2,y2),(0,0,255),4)

img = cv2.addWeighted(img,0.8,zeros, 1.0,0.)


imgStack = stackImages(0.5,([masked,edge_image],[img,mask]))


cv2.imshow("ImageStack",imgStack)

plt.imshow(img)
plt.show()