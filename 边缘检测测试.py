#__author__='DP'
#encoding='utf-8'

import cv2
import numpy as np

#注意，只有经过


# H , W=canny_img.shape
image=cv2.imread('0.png')
#
# y_top = np.nonzero([max(row) for row in image[400:]])[0][0] + 400
# x_top = int(np.mean(np.nonzero(canny_img[y_top])))
#
# y_bottom = y_top + 50
# for row in range(y_bottom, 1080):
#     if canny_img[row, x_top] != 0:
#         y_bottom = row
#         break
#
# x_center, y_center = x_top, (y_top + y_bottom) // 2

image=cv2.GaussianBlur(image,(5,5),0)
canny_image=cv2.Canny(image,1,10)
for h in range(400,1900):
    for w in range(0,1080):
        if canny_image[h, w] != 0:
            print(h,w)
            break

print(canny_image)









