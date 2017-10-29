import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)
i = 0
sec = 20
time_stamp = time.time()
while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    i+=1
    if ((time.time()-time_stamp) >=sec):
    	print i/sec
    	break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()