import mediapipe as mp
import cv2
import numpy as np
# import pyautogui
# from pynput.mouse import Button, Controller


class HandTracker():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.historyData = np.zeros(20,dtype=np.float32)
        self.fingerpos = np.zeros((5,2),dtype=np.int32)
    def Detect(self,img,drawImg=None):
        results = self.hands.process(img)
        if drawImg is not None:
            h,w,c = drawImg.shape
        if results.multi_hand_landmarks:
            if drawImg is not None:
                for handLms in results.multi_hand_landmarks:
                # for id, lm in enumerate(handLms.landmarks):
                    for id,lm in enumerate(handLms.landmark):
                        if id%4 ==0 and id >0:
                            cx0,cy0 = int(handLms.landmark[id-1].x*w),int(handLms.landmark[id-1].y*h)
                            if id ==8:# only for indexing finger
                                self.historyData[1:] = self.historyData[:-1]
                                self.historyData[0] = lm.z
                                cx,cy = int(lm.x*w),int(lm.y*h)
                                cv2.circle(drawImg,(cx,cy),5,(200,0,0),2)
                                cv2.line(drawImg,(cx,cy),(2*cx-cx0,2*cy-cy0),(0,0,200),2,cv2.LINE_AA)
                                cv2.putText(drawImg,f'{lm.z:.3f}',(cx,cy), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
                                self.fingerpos[id//4-1] = [cx,cy]
                    # self.mpDraw.draw_landmarks(drawImg,handLms,self.mpHands.HAND_CONNECTIONS)
            return results.multi_hand_landmarks
        return None

    def ProcessInput(self):
        last3framemean = np.mean(self.historyData[:3])
        sumdistlast3 = np.sum([l-last3framemean for l in self.historyData[:3]])
        if sumdistlast3<0.1:
            tap=True
            for i in range(3,7):
                if self.historyData[i]>self.historyData[i+1]:
                    continue
                else:
                    tap = False
                    break
            if tap:
                print('TAP',self.historyData[0],self.fingerpos[1])
                # mouse = Controller()
                # # Read pointer position
                # print('The current pointer position is {0}'.format(
                #     mouse.position))

                # # Set pointer position
                # mouse.position = (950, 465)
                # print('Now we have moved it to {0}'.format(
                #     mouse.position))

                # # Move pointer relative to current position
                # mouse.move(5, -5)

                # # Press and release
                # mouse.press(Button.left)
                # mouse.release(Button.left)
                # pyautogui.moveTo(950,465)
                # pyautogui.click(self.fingerpos[1][0], self.fingerpos[1][1])
                return tap,self.historyData[0],self.fingerpos[1].copy()
            return False,None,None
        return False,None,None