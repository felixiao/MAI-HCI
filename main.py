from concurrent.futures import thread
from calibration import *
from handtracking import *
from objecttracking import *
from shapetracking import *
from imutils.video import FPS
import time

class HCI():
    def __init__(self):
        print('init')
        self.calib = Calibration('pygameproj/calib.jpg','pygameproj/cap.jpg')
        self.handTracker = HandTracker()
        self.objectTracker = ObjectTracker()
        self.shapeTracker = ShapeTracker()
        self.cap = cv2.VideoCapture(0)
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT= 720
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

    def setup(self,capture=True):
        if capture:
            self.calib.Capture()
        self.calib.QuadDetection()

    def render(self):
        self.fps = FPS().start()
        flip = 1
        rotation = 90
        showInfo = True
        showCam =True
        brightness = 127
        threshold = 127
        while self.cap.isOpened():
            whiteboard = np.ones((self.SCREEN_HEIGHT,self.SCREEN_WIDTH,3),dtype=np.uint8)*brightness
            _, frame = self.cap.read()
            if frame is None:
                break
            
            imgRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            corpImg = self.calib.Process(imgRGB,flip=flip,rotation=rotation)
            results = self.handTracker.Detect(corpImg,whiteboard)
            bboxes = self.objectTracker.Detect(corpImg,whiteboard)
            self.shapeTracker.Detect(corpImg,whiteboard,threshold=threshold)
            
            if showInfo:
                self.fps.update()
                self.fps.stop()
                cv2.putText(whiteboard, f'FPS: {self.fps.fps():.1f}', (self.SCREEN_WIDTH-150,30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
            cv2.namedWindow("original", cv2.WINDOW_FULLSCREEN)
            # cv2.setWindowProperty("original", cv2.WND_PROP_FULLSCREEN, cv2.CV_CAP_PROP_FORMAT)
            cv2.imshow("original", whiteboard)
            if showCam:
                corpImg = cv2.cvtColor(corpImg,cv2.COLOR_RGB2BGR)
                cv2.imshow("Cam", corpImg)
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

if __name__ == '__main__':
    hci=HCI()
    hci.FingerTipTest()
    # hci.setup(False)
    # hci.render()