import cv2
import numpy as np

p=r'E:\AoBi\data\new.avi'

cap = cv2.VideoCapture(0) #开相机
#cap = cv2.VideoCapture(p) #开视频

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(20)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()