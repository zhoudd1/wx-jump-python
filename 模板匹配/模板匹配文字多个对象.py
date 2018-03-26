#__author__='DP'
#encoding='utf-8'

import cv2
import numpy as np

image1=cv2.imread('dp.png',0)
image2=cv2.imread('dpp.png',0)
w,h=image2.shape[::-1]

res=cv2.matchTemplate(image1,image2,cv2.TM_CCOEFF_NORMED)
loc = np.where( res >= 0.8)
for pt in zip(*loc[::-1]):
    cv2.rectangle(image1, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
cv2.imshow('1',image1)
cv2.imwrite('123.jpg',image1)
cv2.waitKey(0)



