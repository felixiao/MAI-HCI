from calibration import *
from handtracking import *
from objecttracking import *
from shapetracking import *
from imutils.video import FPS
import qrtracker
import time

# from pyzbar.pyzbar import decode
import cv2
import numpy as np

# def trackingQRCode(image,drawImg=None,show=True):
#     try:
#         qrobj =decode(image)
#         if qrobj and show and drawImg is not None:
#             for obj in qrobj:
#                 pts = obj.polygon
#                 pts = np.array([pts],np.int32)
#                 pts = pts.reshape((4,1,2))
#                 cv2.polylines(drawImg,[pts],True,(255,255,0),2) 
#         return decode(image)
#     except:
#         return []

class HCI():
    def __init__(self,cameraIndex=1):
        print('init')
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT= 800
        self.calib = Calibration('pygameproj/calib.jpg','pygameproj/cap.jpg',self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
        self.handTracker = HandTracker()
        self.objectTracker = ObjectTracker()
        self.shapeTracker = ShapeTracker()
        self.cameraIndex= cameraIndex
        self.cap = cv2.VideoCapture(cameraIndex)
        self.tappoints = []
        self.fps = None

    def FingerTipTest(self):
        self.fps = FPS().start()
        showInfo = True
        showCam =True
        while self.cap.isOpened():
    
            _, frame = self.cap.read()
            if frame is None:
                break
            
            imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            imgRGB = cv2.flip(imgRGB,1)
            results = self.handTracker.Detect(imgRGB,imgRGB)
            
            if showInfo:
                self.fps.update()
                self.fps.stop()
                cv2.putText(imgRGB, f'FPS: {self.fps.fps():.1f}', (self.SCREEN_WIDTH-150,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
            
            if showCam:
                imgRGB = cv2.cvtColor(imgRGB,cv2.COLOR_RGB2BGR)
                cv2.imshow("Cam", imgRGB)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('i'):# toggle show info(FPS...)
                showInfo = not showInfo
            if key == ord('p'):
                cv2.imwrite('screenshot.jpg',imgRGB)
            if key == ord("q"):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    

    def setup(self,capture=True,showQuadDetec=True):
        success = True
        if capture:
            success = self.calib.Capture(self.cameraIndex)
        if success:
            self.calib.QuadDetection(show=showQuadDetec)
            qrtracker.createQRCode('Test','UI/qrcode.png')
            self.qrcode= cv2.imread('UI/qrcode.png')
            return True
        else:
            return False

    def render(self):
        self.fps = FPS().start()
        flip = None
        rotation = 90
        showInfo = True
        showCam =True
        brightness = 127
        threshold = 127

        while self.cap.isOpened():
            whiteboard = np.ones((self.SCREEN_HEIGHT,self.SCREEN_WIDTH,3),dtype=np.uint8)*brightness
            # whiteboard[:]
            _, frame = self.cap.read()
            if frame is None:
                break
            # posx = np.random.randint(0,2)-1
            # posy = np.random.randint(0,2)-1
            # print(posx,posy,self.qrcode.shape)r
            # whiteboard[300+posx:300+posx+self.qrcode.shape[0],500+posy:500+posy+self.qrcode.shape[1],:] = self.qrcode
            imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            corpImg = self.calib.Process(imgRGB,flip=flip,rotation=rotation)
            gray_corp = cv2.cvtColor(corpImg,cv2.COLOR_RGB2GRAY)
            results = self.handTracker.Detect(corpImg,whiteboard)
            bboxes = self.objectTracker.Detect(corpImg,whiteboard)

            # self.shapeTracker.Detect(corpImg,whiteboard,threshold=threshold,show=showCam)
            qrtracker.trackingQRCode(gray_corp,whiteboard,show=showCam)
            tap,_,pts = self.handTracker.ProcessInput()
            if tap and pts is not None:
                self.tappoints.append(pts)
                print('add point at',pts,len(self.tappoints))
            for p in self.tappoints:
                cv2.circle(whiteboard,(p[0],p[1]),20,(0,0,255),2)
            if showInfo:
                self.fps.update()
                self.fps.stop()
                cv2.putText(whiteboard, f'FPS: {self.fps.fps():.1f}', (self.SCREEN_WIDTH-150,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
            cv2.namedWindow("original", cv2.WINDOW_FULLSCREEN)
            # cv2.setWindowProperty("original", cv2.WND_PROP_FULLSCREEN, cv2.CV_CAP_PROP_FORMAT)
            # cv2.imshow("original", whiteboard)
            if showCam:
                
                corpImg = cv2.resize(corpImg,(128,80))
                corpImg = cv2.cvtColor(corpImg,cv2.COLOR_RGB2BGR)
                whiteboard[:corpImg.shape[0],:corpImg.shape[1],:] = corpImg
                gray_corp = cv2.resize(gray_corp,(128,80))
                gray_corp = cv2.cvtColor(gray_corp,cv2.COLOR_GRAY2BGR)
                whiteboard[:gray_corp.shape[0],corpImg.shape[1]:corpImg.shape[1]+gray_corp.shape[1],:] = gray_corp
                # cv2.imshow("Cam", corpImg)
            cv2.imshow("original", whiteboard)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('t'):
                threshold = (threshold+10) % 255
            if key == ord('s'):
                self.objectTracker.Marking(corpImg,reset=True)
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
            if key == ord('p'):
                cv2.imwrite('screenshot.jpg',corpImg)

            if key == ord("q"):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def painter(self,point):
        whiteboard = np.ones((self.SCREEN_HEIGHT,self.SCREEN_WIDTH,3),dtype=np.uint8)*255
        self.points.append(point)

        for p in self.points:
            cv2.circle(whiteboard,(p[0],p[1]),5,(200,0,0),2)
if __name__ == '__main__':
    hci=HCI()
    # hci.FingerTipTest()
    # success = hci.setup(False,False)
    success = hci.setup(True,True)
    if success:
        hci.render()