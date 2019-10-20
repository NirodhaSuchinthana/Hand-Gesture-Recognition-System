import numpy as np
import cv2

cap = cv2.VideoCapture(0)
hand_cascade = cv2.CascadeClassifier('cascade.xml') 

while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray, 1.1, 4) 

    for(x,y,w,h) in hands:
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

    cv2.imshow('frame',frame)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()