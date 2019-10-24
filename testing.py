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
# frame = cv2.flip(frame, 1)
trackerType = "MOSSE" 
hand_cascade = cv2.CascadeClassifier('abcd.xml') 

while (True):
    # using cascade classifire

    # _, newFrame = cap.read()
    # gray = cv2.cvtColor(newFrame, cv2.COLOR_BGR2GRAY)
    # hands = hand_cascade.detectMultiScale(gray, 1.1, 3) 
    # for bbox in hands:
    #     a = bbox[0]
    #     b = bbox[1]
    #     c = bbox[2]
    #     d = bbox[3]
    #     boxes.append((a,b,a+c, b+d))
    #     newFrame = cv2.rectangle(newFrame, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (225,0,0), 2)
    # cv2.imshow("captured frame", newFrame)

    # using ROI
    bbox = cv2.selectROI('MultiTracker', frame)
    boxes.append(bbox)
    # print(boxes)

    # k = cv2.waitKey(0) & 0xFF
    # if (k == 113):
    #     break
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break
    if boxes:
        break

# cv2.imshow("captured frame", newFrame)
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
        correction_length = 0#int((newbox[2]+newbox[3])/6)

        p1 = (int(newbox[0]-correction_length), int(newbox[1])-correction_length)
        # p2 = (int(newbox[2]), int(newbox[3]))
        p2 = (int(newbox[0]+newbox[2]), int(newbox[1]+newbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

    # show frame
    # frame = cv2.flip(frame, 1)
    cv2.imshow('frame', frame)
    

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break
    
cap.release()
cv2.destroyAllWindows()
