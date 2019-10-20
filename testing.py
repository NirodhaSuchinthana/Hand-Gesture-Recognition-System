import cv2
import numpy as np
from random import randint

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)
    
  return tracker


cap = cv2.VideoCapture(0)
boxes = []
i = 0
while(i<10):
    ret, frame = cap.read()
    i = i + 1

trackerType = "CSRT" 

while (True):
    bbox = cv2.selectROI('MultiTracker', frame)
    boxes.append(bbox)
    print(bbox)
    # (535, 208, 209, 236)
    # frame = cv2.rectangle(frame, (535,208), (535+209,208+236), (0,0,225), 2)
    # cv2.rectangle(frame, (boxes[0], boxes[1]), (boxes[0]+boxes[2], boxes[1]+boxes[3]),(255, 0, 0), 2, 2)
    # cv2.imshow("frame", frame)

    k = cv2.waitKey(0) & 0xFF
    if (k == 113):  # q is pressed
        break
    if boxes:
        break

multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker 
for bbox in boxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)


# Process video and track objects
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    
    # get updated location of objects in subsequent frames
    success, bboxes = multiTracker.update(frame)

    # draw tracked objects
    for i, newbox in enumerate(bboxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

    # show frame
    cv2.imshow('frame', frame)
    

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break
    
cap.release()
cv2.destroyAllWindows()
