from pyzbar.pyzbar import decode
import cv2
import numpy as np

def trackingQRCode(image,drawImg=None,show=True):
    try:
        qrobj =decode(image)
        if qrobj and show and drawImg is not None:
            for obj in qrobj:
                pts = obj.polygon
                pts = np.array([pts],np.int32)
                pts = pts.reshape((4,1,2))
                cv2.polylines(drawImg,[pts],True,(255,255,0),2) 
        return decode(image)
    except:
        return []
