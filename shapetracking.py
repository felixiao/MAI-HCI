import cv2
import math
from cv2 import ROTATE_90_CLOCKWISE
from cv2 import ROTATE_90_COUNTERCLOCKWISE
from cv2 import ROTATE_180
import numpy as np
import imutils

class ShapeTracker():
    def __init__(self):
        print('init shape')
    
    def Detect(self,image,drawImg=None,blursize=9,threshold=170,show=False):
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_img, (blursize, blursize), 0)             # 高斯模糊去噪（设定卷积核大小影响效果）
        _, RedThresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)  # 设定阈值165（阈值影响开闭运算效果
        # cv2.imshow('Binary',RedThresh)
        RedThresh = np.invert(RedThresh)
        # cv2.putText(RedThresh,f'T={threshold}',(0,30),cv2.FONT_HERSHEY_SIMPLEX,1, (threshold, threshold, threshold), 2)
        if show and drawImg is not None:
            RedThresh_show = cv2.resize(RedThresh,(128,80))
            RedThresh_show = cv2.cvtColor(RedThresh_show, cv2.COLOR_GRAY2RGB)
            drawImg[80:80+RedThresh_show.shape[0],:RedThresh_show.shape[1],:] = RedThresh_show
            # cv2.imshow('BinaryInv',drawImg)

        # cv2.imwrite('binary.jpg',RedThresh)
        cnts = cv2.findContours(RedThresh.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)              

        # cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
        # cv2.imshow("Cam", image)
        for i,c in enumerate(cnts):
        # c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]              # 计算最大轮廓的旋转包围盒
            epsilon = 0.1*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)[:,0]
            # if len(approx)>=3:
                # print(f'{i}  {approx}')
            rotatedRect = cv2.minAreaRect(c)
            # vertices = cv2.RotatedRect.points(rotatedRect)
            # print(rotatedRect)

            if drawImg is not None:
                scaleX = drawImg.shape[0]/image.shape[0]
                scaleY = drawImg.shape[1]/image.shape[1]
                approx = np.array([[ap[0]*scaleX,ap[1]*scaleY] for ap in approx],dtype=np.int32)

                cv2.polylines(drawImg,[np.array(approx)],True,(0,255,0),2)
                # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

                # for i in range(4):
                # cv2.polylines(drawImg, [rotatedRect], (255,0,0), 2, cv2.LINE_AA, 0)
            # cv2.imshow("Cam", image)