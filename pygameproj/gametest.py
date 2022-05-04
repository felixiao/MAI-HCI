import numpy as np
from matplotlib import pyplot as plt
import os

import cv2 as cv
#Initialize video capture
# cap = cv.VideoCapture('rtsp://felixphone.local:8554/live')
cap = cv.VideoCapture(0)

scaling_factor = 0.2

tmp1 = cv.imread('pygameproj/tm1.JPG',0)
tmp2 = cv.imread('pygameproj/tm2.JPG',0)
tmp3 = cv.imread('pygameproj/tm3.JPG',0)
tmp4 = cv.imread('pygameproj/tm4.JPG',0)
tmp1 = cv.resize(tmp1, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)
tmp2 = cv.resize(tmp2, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)
tmp3 = cv.resize(tmp3, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)
tmp4 = cv.resize(tmp4, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv.INTER_AREA)
w1, h1 = tmp1.shape[::-1]
w2, h2 = tmp1.shape[::-1]
w3, h3 = tmp1.shape[::-1]
w4, h4 = tmp1.shape[::-1]
ws = [w1,w2,w3,w4]
hs = [h1,h2,h3,h4]
tmps= [tmp1,tmp2,tmp3,tmp4]

# Initialize the ORB detector algorithm
orb = cv.ORB_create()
matcher = cv.BFMatcher()
# Now detect the keypoints and compute
# the descriptors for the query image
# and train image
# tmp1_gray = cv.cvtColor(tmp1, cv.COLOR_BGR2GRAY)
queryKeypoints, queryDescriptors = orb.detectAndCompute(tmp1,None)


# # All the 6 methods for comparison in a list
# methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
#             'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
font = cv.FONT_HERSHEY_SIMPLEX

colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0)]
while True:
#     # Capture the current frame
    ret, frame = cap.read()
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    trainKeypoints, trainDescriptors = orb.detectAndCompute(frame_gray,None)
 
    # Initialize the Matcher for matching
    # the keypoints and then match the
    # keypoints
    
    matches = matcher.match(queryDescriptors,trainDescriptors)
    
    # draw the matches to the final image
    # containing both the images the drawMatches()
    # function takes both images and keypoints
    # and outputs the matched query image with
    # its train image
    final_img = cv.drawMatches(tmp1, queryKeypoints, frame_gray, trainKeypoints, matches[:20],None)
    
    final_img = cv.resize(final_img, (frame.shape[1],frame.shape[0]))
    
    # Show the final image
    cv.imshow("Matches", final_img)
    # # blank_image = np.ones((frame.shape[0],frame.shape[1],3), np.uint8)*255
    # for i,tmp in enumerate(tmps):
    #     res = cv.matchTemplate(frame_gray,tmp,cv.TM_CCOEFF_NORMED)
    #     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    #     top_left = max_loc
    #     bottom_right = (top_left[0] + ws[i], top_left[1] + hs[i])
    #     bottom_left = (top_left[0], top_left[1] + hs[i])
    #     cv.rectangle(frame_gray,top_left, bottom_right, colors[i], 2)
    #     cv.putText(frame_gray,f'Tag {i+1}',bottom_left, font, 1,colors[i],2,cv.LINE_AA)
    # cv.imshow('Webcam', frame_gray)
# Detect if the Esc key has been pressed
    c = cv.waitKey(1)
    if c == 27:
        break
# Release the video capture object
cap.release()
# Close all active windows
cv.destroyAllWindows()

# for meth in methods:
#     img = img2.copy()
#     method = eval(meth)
#     # Apply template Matching
#     res = cv.matchTemplate(img,template,method)
#     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
#     # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#     if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
#     bottom_right = (top_left[0] + w, top_left[1] + h)
#     cv.rectangle(img,top_left, bottom_right, (255,0,0), 3)
#     plt.subplot(121),plt.imshow(res,cmap='gray')
#     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(122),plt.imshow(img,cmap='viridis')
#     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)
#     plt.show()