#（基于透视的图像矫正）
import cv2
import math
from cv2 import ROTATE_90_CLOCKWISE
from cv2 import ROTATE_90_COUNTERCLOCKWISE
from cv2 import ROTATE_180
import numpy as np
import imutils
import mediapipe as mp
import time

def Perspective_transform(box,original_img,flip=None,rotation=0):
    # 获取画框宽高(x=orignal_W,y=orignal_H)
    orignal_W = math.ceil(np.sqrt((box[3][1] - box[2][1])**2 + (box[3][0] - box[2][0])**2))
    orignal_H= math.ceil(np.sqrt((box[3][1] - box[0][1])**2 + (box[3][0] - box[0][0])**2))

    # 原图中的四个顶点,与变换矩阵
    pts1 = np.float32([box[0], box[1], box[2], box[3]])
    pts2 = np.float32([[int(orignal_W+1),int(orignal_H+1)], [0, int(orignal_H+1)], [0, 0], [int(orignal_W+1), 0]])

    # 生成透视变换矩阵；进行透视变换
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result_img = cv2.warpPerspective(original_img, M, (int(orignal_W+3),int(orignal_H+1)))
    if rotation==90:
        result_img = cv2.rotate(result_img,ROTATE_90_CLOCKWISE)
    elif rotation==180:
        result_img = cv2.rotate(result_img,ROTATE_180)
    elif rotation==270:
        result_img = cv2.rotate(result_img,ROTATE_90_COUNTERCLOCKWISE)
    if flip:
        result_img = cv2.flip(result_img,flip)
    return result_img

def ShowBackground():
    SCREEN_WIDTH = 1080
    SCREEN_HEIGHT= 720
    cap = cv2.VideoCapture(0)
    calibrImg = cv2.imread('pygameproj/calibrationImage2.jpg')
    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            break
        cv2.imshow("Cam", frame)
        # whiteboard = np.ones((SCREEN_HEIGHT,SCREEN_WIDTH,3),dtype=np.uint8)*127
        cv2.imshow("original", calibrImg)
        key = cv2.waitKey(1) & 0xFF    
        if key == ord('c'):
            cv2.imwrite('pygameproj/cap.jpg',frame)
            break
    cap.release()
    cv2.destroyAllWindows()

def Calibre(img,show=False):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (9, 9), 0)                     # 高斯模糊去噪（设定卷积核大小影响效果）
    _, RedThresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)  # 设定阈值165（阈值影响开闭运算效果）
    cnts = cv2.findContours(RedThresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]              # 计算最大轮廓的旋转包围盒
    epsilon = 0.1*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)[:,0]
    # print(f'Len Approx: {len(approx)}')
    print(f'Approx: {approx}')
    print(f'[1-0] = {approx[1]-approx[0]}')
    print(f'[2-0] = {approx[2]-approx[0]}')
    print(f'[3-0] = {approx[3]-approx[0]}')

    if show:
        cv2.drawContours(img, [c], -1, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        flip = None
        rotation = 90
        while True:
            perTra = Perspective_transform(approx,img,flip=flip,rotation=rotation)
            cv2.imshow("PreTransform", perTra)
            key = cv2.waitKey(1) & 0xFF
            if key== ord('f'):
                flip=None
            if key == ord('h'):
                flip=0
            if key == ord('v'):
                flip=1
            if key == ord('b'):
                flip=-1
            if key == ord('r'):
                rotation= (rotation+90) % 360
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

    return approx

def Draw(approx):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT= 720

    pTime = time.time()
    flip = 1
    rotation = 90
    showInfo = True
    showCam =True
    brightness = 127
    while cap.isOpened():
        whiteboard = np.ones((SCREEN_HEIGHT,SCREEN_WIDTH,3),dtype=np.uint8)*brightness
        ret, frame = cap.read()
        if frame is None:
            break
        
        imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        corpImg = Perspective_transform(approx,imgRGB,flip=flip,rotation=rotation)
        results = hands.process(corpImg)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # for id, lm in enumerate(handLms.landmarks):
                mpDraw.draw_landmarks(whiteboard,handLms,mpHands.HAND_CONNECTIONS)
        if showInfo:
            fps = 1/(time.time()-pTime)
            pTime = time.time()
            cv2.putText(whiteboard, 'FPS: '+str(int(fps)), (SCREEN_WIDTH-150,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
        cv2.namedWindow("original", cv2.WINDOW_FULLSCREEN)
        # cv2.setWindowProperty("original", cv2.WND_PROP_FULLSCREEN, cv2.CV_CAP_PROP_FORMAT)
        cv2.imshow("original", whiteboard)
        if showCam:
            cv2.imshow("Cam", corpImg)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('i'):# toggle show info(FPS...)
            showInfo = not showInfo
        if key == ord('c'):# toggle show camera
            showCam = not showCam
        if key == ord('f'):
            flip=None
        if key == ord('h'):
            flip=0
        if key == ord('v'):
            flip=1
        if key == ord('b'):
            flip=-1
        if key == ord('r'):
            rotation= (rotation+90) % 360
        if key == ord('w'):
            brightness=(brightness+10) % 255
        if key == ord('d'):
            brightness=(brightness-10) % 255
        if key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    ShowBackground()
    img = cv2.imread('pygameproj/cap.jpg')
    approx = Calibre(img)
    Draw(approx)