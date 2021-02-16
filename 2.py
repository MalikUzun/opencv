import cv2
import numpy as np

img = cv2.imread("resimler/lambo.jpg")

print(img.shape)

imgResize = cv2.resize(img,(1600,1200))

print(imgResize.shape)

cv2.imshow("Resim",img)
cv2.imshow("Resized",imgResize)

imgResult = img.copy()

cv2.waitKey(0)