import mediapipe as mp

class HandTracker():
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
    
    def Detect(self,img,drawImg=None):
        results = self.hands.process(img)

        if results.multi_hand_landmarks:
            if drawImg is not None:
                for handLms in results.multi_hand_landmarks:
                # for id, lm in enumerate(handLms.landmarks):
                    self.mpDraw.draw_landmarks(drawImg,handLms,self.mpHands.HAND_CONNECTIONS)
            return results.multi_hand_landmarks
        return None
        