import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
hand_cascade = cv2.CascadeClassifier('cascade.xml') 
isHanddetect = False

boxes = []
trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
trackerType = "MOSSE"

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


while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray, 1.1, 4) 

    for a,b,c,d in hands:
        # a = box[0]
        # b = box[1]
        # c = box[2]
        # d = box[3]
        boxes.append((a,b,a+c, b+d))
        # if(abs(c)> 50 & abs(d)> 50):
        frame = cv2.rectangle(frame, (a,b), (a+c+20,b+d+20), (255,0,0), 2)
        
        isHanddetect = True

    cv2.imshow('frame',frame)

    if(isHanddetect == True):
        break

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


# _, newFrame = cap.read()
def fixRectangle():
    while(True):
        _, frame = cap.read()
        frame = cv2.rectangle(frame, (a-30,b-100), (a+c+60,b+d+20), (0,0,225), 2)
        cv2.imshow("newFrame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break

# def trackHand():
multiTracker = cv2.MultiTracker_create()

for bbox in boxes:
  print('found box:', bbox)
  multiTracker.add(createTrackerByName(trackerType), frame, bbox)
  abc = multiTracker.getObjects()
  print('get objects:', abc)
  success, boxes = multiTracker.update(frame)
  print('update:', boxes)
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)
    print(boxes)
    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2)
    cv2.imshow('MultiTracker', frame)


# quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break
# if cv2.waitKey(20) & 0xFF == ord('q'):
#     break

cap.release()
cv2.destroyAllWindows()


