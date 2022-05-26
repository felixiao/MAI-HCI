import pyqrcode
import cv2
import numpy as np


def trackingQRCode(image,drawImg=None,show=True):
    scaleX = drawImg.shape[0]/image.shape[0]
    scaleY = drawImg.shape[1]/image.shape[1]
    try:
        detector = cv2.QRCodeDetector()
        data,bbox,straight_qrcode= detector.detectAndDecode(image)
    except:
        return
    if bbox is not None and show and drawImg is not None:
        for box in bbox:
            new_bbox = [tuple((pb[0]*scaleX+20,pb[1]*scaleY)) for pb in box]
            new_bbox = np.int32(new_bbox)
            cv2.polylines(drawImg,[new_bbox],True,(255,0,0),2)
            cv2.putText(drawImg, f'{data}', (new_bbox[0][0]-10,new_bbox[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 200, 0), 2)
            # print((np.int32(new_bbox[0][0]),np.int32(new_bbox[0][1])))

def createQRCode(content,path):
    qr = pyqrcode.create(content)
    # qr.png(path,scale=10)