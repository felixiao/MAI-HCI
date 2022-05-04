import imutils
import cv2
from random import randint
import numpy as np
trackerName = 'csrt'

# OPENCV_OBJECT_TRACKERS = {
#     "csrt": cv2.TrackerCSRT_create,
#     "kcf": cv2.TrackerKCF_create,
#     "boosting": cv2.TrackerBoosting_create,
#     "mil": cv2.TrackerMIL_create,
#     "tld": cv2.TrackerTLD_create,
#     "medianflow": cv2.TrackerMedianFlow_create,
#     "mosse": cv2.TrackerMOSSE_create
# }

# initialize OpenCV's special multi-object tracker
calibrationImg = cv2.imread('pygameproj/calibrationImage2.jpg')

trackers = cv2.legacy.MultiTracker_create()
cap = cv2.VideoCapture(0)
anchorSize = 50
SCREEN_WIDTH = 1280
SCREEN_HEIGHT= 720

while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break
    
    # whiteboard = calibrationImg
    whiteboard = np.ones((SCREEN_HEIGHT,SCREEN_WIDTH,3),dtype=np.uint8)*80
    frame = imutils.resize(frame, width=SCREEN_WIDTH,height=SCREEN_HEIGHT)
    # print(frame.shape)
    (success, boxes) = trackers.update(frame)
    
    cv2.rectangle(whiteboard,(0,0),(anchorSize,anchorSize),(255,0,0),-1) # top left corner
    cv2.rectangle(whiteboard,(SCREEN_WIDTH-anchorSize,0),(SCREEN_WIDTH,anchorSize),(0,255,0),-1) # top right corner
    cv2.rectangle(whiteboard,(0,SCREEN_HEIGHT-anchorSize),(anchorSize,SCREEN_HEIGHT),(0,0,255),-1) # bottom left corner
    cv2.rectangle(whiteboard,(SCREEN_WIDTH-anchorSize,SCREEN_HEIGHT-anchorSize),(SCREEN_WIDTH,SCREEN_HEIGHT),(0,0,0),-1)   # bottom right corner
    
    cv2.rectangle(whiteboard,(int((SCREEN_WIDTH-anchorSize)/2),int((SCREEN_HEIGHT-anchorSize)/2)),(int((SCREEN_WIDTH+anchorSize)/2),int((SCREEN_HEIGHT+anchorSize)/2)),(125,125,125),-1)   # Center
    cv2.rectangle(whiteboard,(int((SCREEN_WIDTH-anchorSize)/2),0),(int((SCREEN_WIDTH+anchorSize)/2),anchorSize),(125,125,0),-1)   # Top Center
    cv2.rectangle(whiteboard,(int((SCREEN_WIDTH-anchorSize)/2),SCREEN_HEIGHT-anchorSize),(int((SCREEN_WIDTH+anchorSize)/2),SCREEN_HEIGHT),(0,0,125),-1)   # Bottom Center
    cv2.rectangle(whiteboard,(0,int((SCREEN_HEIGHT-anchorSize)/2)),(anchorSize,int((SCREEN_HEIGHT+anchorSize)/2)),(125,0,125),-1)   # Left Center
    cv2.rectangle(whiteboard,(SCREEN_WIDTH-anchorSize,int((SCREEN_HEIGHT-anchorSize)/2)),(SCREEN_WIDTH,int((SCREEN_HEIGHT+anchorSize)/2)),(0,125,0),-1)   # Right Center

    for i, box in enumerate(boxes):
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(whiteboard, (x, y), (x+ w, y + h), (0, 255, 0), 2)
        cv2.putText(whiteboard,f'b{i} {x} {y}',(x,y + h),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    # if len(boxes)>2:
    #     (x_1, y_1, w_1, h_1) = [int(v) for v in boxes[0]]
    #     (x_2, y_2, w_2, h_2) = [int(v) for v in boxes[1]]
    #     sx = (x_2- x_1)/(x2-x1)
    #     sy = (y_2 - y_1)/(y2-y1)
    #     cv2.rectangle(whiteboard, (x1, y1), (x1+50, y1 + 50), (0, 255, 0), 2)
    #     cv2.putText(whiteboard,f'b0 {x1} {y1}',(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    #     cv2.rectangle(whiteboard, (x2, y2), (x2+50, y2 + 50), (0, 255, 0), 2)
    #     cv2.putText(whiteboard,f'b1 {x2} {y2}',(x2,y2),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

    # loop over the bounding boxes and draw them on the frame
    # for i, box in enumerate(boxes):
    #     if i>1:
    #         (x, y, w, h) = [int(v) for v in box]
    #         X = x1+sx*(x-x_1)
    #         Y = y1+sy*(y-y_1)
    #         cv2.rectangle(whiteboard, (X, Y), (X+ w/sx, Y + h/sy), (0, 255, 0), 2)
    #         cv2.putText(whiteboard,f'b{i} {X} {Y}',(X,Y + h/sy),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

    cv2.imshow("Frame", whiteboard)
    cv2.imshow("Cam", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if key == ord("s"):
        # colors = []
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        
        # cv2.rectangle(frame,(x1,y1+20),(x1+50,y1+30),(255,255,255),-1)
        # cv2.rectangle(frame,(x1+20,y1),(x1+30,y1+50),(255,255,255),-1)

        # cv2.rectangle(frame,(x2,y2),(x2+50,y2+10),(255,255,255),-1)
        # cv2.rectangle(frame,(x2+20,y2),(x2+30,y2+50),(255,255,255),-1)
        # cv2.rectangle(frame,(x2,y2+40),(x2+50,y2+50),(255,255,255),-1)
        cv2.imwrite('pygameproj/cap.jpg',frame)
        box = cv2.selectROIs("Frame", frame, fromCenter=False,showCrosshair=True)
        box = tuple(map(tuple, box)) 
        for bb in box:
            tracker = cv2.legacy.TrackerCSRT_create()
            trackers.add(tracker, frame, bb)

    # if you want to reset bounding box, select the 'r' key 
    elif key == ord("r"):
        trackers.clear()
        trackers = cv2.legacy.MultiTracker_create()
        # cv2.rectangle(frame,(x1,y1+20),(x1+50,y1+30),(255,255,255),-1)
        # cv2.rectangle(frame,(x1+20,y1),(x1+30,y1+50),(255,255,255),-1)
        # cv2.rectangle(frame,(x2,y2),(x2+50,y2+10),(255,255,255),-1)
        # cv2.rectangle(frame,(x2+20,y2),(x2+30,y2+50),(255,255,255),-1)
        # cv2.rectangle(frame,(x2,y2+40),(x2+50,y2+50),(255,255,255),-1)
        
        box = cv2.selectROIs("Frame", frame, fromCenter=False,showCrosshair=True)
        box = tuple(map(tuple, box))
        for bb in box:
            tracker = cv2.legacy.TrackerCSRT_create()
            trackers.add(tracker, frame, bb)

    elif key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()