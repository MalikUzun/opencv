import cv2

cap = cv2.VideoCapture("resimler/test.mp4")

while True:
    ret, frame = cap.read()

    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()