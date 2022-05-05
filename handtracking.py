import mediapipe as mp
import cv2
class HandTracker():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
    
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
                            cx,cy = int(lm.x*w),int(lm.y*h)
                            cv2.circle(drawImg,(cx,cy),5,(200,0,0),2)
                            cv2.line(drawImg,(cx,cy),(2*cx-cx0,2*cy-cy0),(0,0,200),2,cv2.LINE_AA)
                            cv2.putText(drawImg,f'{lm.z:.3f}',(cx,cy), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
                    # self.mpDraw.draw_landmarks(drawImg,handLms,self.mpHands.HAND_CONNECTIONS)

            return results.multi_hand_landmarks
        return None
        