import cv2

p=r'E:\AoBi\data\suibian.avi'

cap = cv2.VideoCapture(0)

codec=cv2.VideoWriter_fourcc(*'MJPG')
fps=30.0
frameSize=(640,480)
out = cv2.VideoWriter(p, codec, fps, frameSize)

while True:
    ret, frame = cap.read()

    out.write(frame)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

