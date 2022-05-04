import imutils
import cv2
from random import randint
import numpy as np


calibrateImage = ''
trackerName = 'csrt'
trackers = cv2.legacy.MultiTracker_create()
cap = cv2.VideoCapture(0)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT= 800

bboxs = []

while cap.isOpened():
    ret, frame = cap.read()
    if frame is None:
        break

    (success, boxes) = trackers.update(frame)



    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        box = cv2.selectROIs("Frame", frame, fromCenter=False,showCrosshair=True)
        box = tuple(map(tuple, box)) 
        for bb in box:
            tracker = cv2.legacy.TrackerCSRT_create()
            trackers.add(tracker, frame, bb)