import cv2
import math
from cv2 import ROTATE_90_CLOCKWISE
from cv2 import ROTATE_90_COUNTERCLOCKWISE
from cv2 import ROTATE_180
import numpy as np
import imutils
from torch import embedding

class Calibration():
    def __init__(self,calibImagePath,capImagePath,SCREEN_WIDTH,SCREEN_HEIGHT):
        self.capturedImagePath = capImagePath
        self.calibimage = cv2.imread(calibImagePath)
        self.capturedImage = None
        self.transformMatrix = None
        self.dsize = None
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT= SCREEN_HEIGHT

    def Capture(self,cameraIndex=0,embeddedcam = True):
        cap = cv2.VideoCapture(cameraIndex)
        brightness = 127
        visualize = False
        # embeddedcam = False
        while cap.isOpened():
            _, frame = cap.read()
            if frame is None:
                break
            camimg = cv2.resize(frame,(self.SCREEN_WIDTH//2,self.SCREEN_HEIGHT//2))
            if visualize:
                gray_img = cv2.cvtColor(camimg, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray_img, (9, 9), 0)             # 高斯模糊去噪（设定卷积核大小影响效果）
                _, RedThresh = cv2.threshold(blurred, 122, 255, cv2.THRESH_BINARY)  # 设定阈值165（阈值影响开闭运算效果)


            whiteboard = np.ones((self.SCREEN_HEIGHT,self.SCREEN_WIDTH,3),dtype=np.uint8)*brightness
            if embeddedcam:
                cv2.destroyWindow('Cam')
                camimg_resize= cv2.resize(camimg,(camimg.shape[1]//2,camimg.shape[0]//2))
                whiteboard[10:10+camimg_resize.shape[0],10:10+camimg_resize.shape[1],:] =camimg_resize
                if visualize:
                    RedThresh_resize = cv2.resize(RedThresh,(RedThresh.shape[1]//2,RedThresh.shape[0]//2))
                    RedThresh_resize = cv2.cvtColor(RedThresh_resize, cv2.COLOR_GRAY2RGB)
                    whiteboard[10:10+RedThresh_resize.shape[0],10+camimg_resize.shape[1]:10+camimg_resize.shape[1]+RedThresh_resize.shape[1],:] =RedThresh_resize
            else:
                cv2.imshow("Cam", camimg)
            cv2.imshow("original", whiteboard)
            key = cv2.waitKey(1) & 0xFF    
            if key == ord('c'):
                self.capturedImage = frame
                cv2.imwrite(self.capturedImagePath,frame)
                break
            elif key == ord('w'):
                brightness=(brightness+10)%255
            elif key == ord('q'):
                return False
            elif key == ord('e'):
                embeddedcam = not embeddedcam
                
            elif key == ord('v'):
                visualize = not visualize
        cap.release()
        cv2.destroyAllWindows()
        return True
    
    def QuadDetection(self,show=False,blursize=9,threshold=122):
        if self.capturedImage is None:
            self.capturedImage = cv2.imread(self.capturedImagePath)
        gray_img = cv2.cvtColor(self.capturedImage, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_img, (blursize, blursize), 0)             # 高斯模糊去噪（设定卷积核大小影响效果）
        _, RedThresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)  # 设定阈值165（阈值影响开闭运算效果)
        # cv2.imwrite('Threshold.jpg',RedThresh)
        # cv2.imwrite('binary.jpg',RedThresh)
        cnts = cv2.findContours(RedThresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]              # 计算最大轮廓的旋转包围盒
        epsilon = 0.1*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)[:,0]

        # 获取画框宽高(x=orignal_W,y=orignal_H)
        orignal_W = math.ceil(np.sqrt((approx[3][1] - approx[2][1])**2 + (approx[3][0] - approx[2][0])**2))
        orignal_H= math.ceil(np.sqrt((approx[3][1] - approx[0][1])**2 + (approx[3][0] - approx[0][0])**2))
        # 原图中的四个顶点,与变换矩阵
        pts1 = np.float32([approx[0], approx[1], approx[2], approx[3]])
        pts2 = np.float32([[int(orignal_W+1),int(orignal_H+1)], [0, int(orignal_H+1)], [0, 0], [int(orignal_W+1), 0]])
        self.dsize = (int(orignal_W+3),int(orignal_H+1))
        # 生成透视变换矩阵；进行透视变换
        self.transformMatrix = cv2.getPerspectiveTransform(pts1, pts2)
        print(f'Approx: {approx}')
        
        if show:
            print(f'[1-0] = {approx[1]-approx[0]}')
            print(f'[2-0] = {approx[2]-approx[0]}')
            print(f'[3-0] = {approx[3]-approx[0]}')
            cv2.drawContours(self.capturedImage, [c], -1, (0, 255, 0), 3)
            cv2.imshow("Image", self.capturedImage)
            # cv2.imwrite('CamContour.jpg',self.capturedImage)
            flip = None
            rotation = 90
            while True:
                perTra = self.Process(self.capturedImage,flip=flip,rotation=rotation)
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

    def Process(self,original_img,flip=None,rotation=0):
        if self.transformMatrix is not None:
            result_img = cv2.warpPerspective(original_img, self.transformMatrix, self.dsize)
            if rotation==90:
                result_img = cv2.rotate(result_img,ROTATE_90_CLOCKWISE)
            elif rotation==180:
                result_img = cv2.rotate(result_img,ROTATE_180)
            elif rotation==270:
                result_img = cv2.rotate(result_img,ROTATE_90_COUNTERCLOCKWISE)
            if flip:
                result_img = cv2.flip(result_img,flip)
            return result_img
        else:
            print('Not calibrated yet')
    