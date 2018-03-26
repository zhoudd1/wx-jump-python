#__author__='DP'
#encoding='utf-8'


#识别退出游戏和小白点采用模板匹配，即用一个相似的照片进行遍历
#详情请查看opencv3教程
import cv2

temp_image=cv2.imread('0.png',0)

temp_circle=cv2.imread('temp_white_circle.jpg',0)
w1,h1=temp_circle.shape[::-1]
#跳棋的匹配
print('w1:',w1,'h1:',h1)
temp_jump=cv2.imread('temp_player.jpg',0)
w2,h2=temp_jump.shape[::-1]


res=cv2.matchTemplate(temp_jump,temp_image,cv2.TM_CCOEFF_NORMED)


# &minVal 和 &maxVal: 在矩阵 result 中存储的最小值和最大值
# &minLoc 和 &maxLoc: 在结果矩阵中最小值和最大值的坐标.
min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res)


center1_loc = (max_loc1[0] + 39, max_loc1[1] + 189)
cv2.rectangle(temp_image, max_loc1, (center1_loc[0]+w2//2,center1_loc[1]+15),0, 3)#15为随机数
# cv2.circle(temp_image,center1_loc, 10, (0,255,0), -1)
#确定跳棋的位置



# cv2.imshow('123',temp_image)
# cv2.imwrite('image.jpg',temp_image)
# cv2.waitKey(0)

image=cv2.GaussianBlur(temp_image,(5,5),0)
canny=cv2.Canny(image,1,10)

cv2.imwrite('image2.jpg',canny)
# 消去小跳棋轮廓对边缘检测结果的干扰
#
for k in range(max_loc1[1] - 10, max_loc1[1] + 189):
    for b in range(max_loc1[0] - 10, max_loc1[0] + 100):
        canny[k][b] = 0

cv2.imwrite('image.jpg',canny)






