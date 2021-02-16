import cv2
import numpy as np

img = cv2.imread("resimler/avustralya-yol.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 75, 150


#lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)

video = cv2.VideoCapture("resimler/test.mp4")
while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture("road_car_view.mp4")
        continue
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)