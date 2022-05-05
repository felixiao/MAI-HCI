# OpenCV Object Tracking
# import the necessary packages

import cv2

class ObjectTracker():
    def __init__(self,type='MOSSE'):
        self.type = type
        self.trackers = cv2.legacy.MultiTracker_create()
        self.numTrackers = 0

    def Marking(self,image,reset=False):
        if reset:
            self.numTrackers = 0
            self.trackers.clear()
            self.trackers = cv2.legacy.MultiTracker_create()
        box = cv2.selectROIs("Cam", image, fromCenter=False,showCrosshair=True)
        box = tuple(map(tuple, box)) 
        for bb in box:
            if self.type == 'BOOSTING':
                tracker = cv2.legacy.TrackerBoosting_create()
            elif self.type == 'MIL':
                tracker = cv2.legacy.TrackerMIL_create()
            elif self.type == 'KCF':
                tracker = cv2.legacy.TrackerKCF_create()
            elif self.type == 'TLD':
                tracker = cv2.legacy.TrackerTLD_create()
            elif self.type == 'MEDIANFLOW':
                tracker = cv2.legacy.TrackerMedianFlow_create()
            elif self.type == 'MOSSE':
                tracker = cv2.legacy.TrackerMOSSE_create()
            elif self.type == "CSRT":
                tracker = cv2.legacy.TrackerCSRT_create()
            self.trackers.add(tracker, image, bb)
            self.numTrackers +=1

    def Detect(self,image,drawImg):
        if self.trackers and self.numTrackers>0:
            ratioY = drawImg.shape[0] / image.shape[0]
            ratioX = drawImg.shape[1] / image.shape[1]
            (success, boxes) = self.trackers.update(image)
            # print(f'success: {success}')
            for i, box in enumerate(boxes):
                (x, y, w, h) = [int(v) for v in box]
                X=int(x*ratioX)
                W=int(w*ratioX)
                Y=int(y*ratioY)
                H=int(h*ratioY)
                cv2.rectangle(drawImg, (X, Y), (X+ W, Y + H), (0, 255, 0), 2)
                cv2.putText(drawImg,f'b{i} {X} {Y}',(X,Y + H),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
