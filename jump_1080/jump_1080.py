# !/usr/bin/env python
# -*- coding:utf-8 -*-
#__author__ = 'DP'
import os
import PIL
import matplotlib.pyplot as plt
import time
import numpy as np
import cv2
import random


#获取设备连接信息
def get_devices_message():
    print('查看是否有设备接入')
    print('-----------------分割线----------------')
    print('若显示List of devices attached')
    print('~~~~~~~~	device,则正确连接，否则请打开usb调试重新连接')
    print('-----------------分割线----------------')
    print('获得设备连接结果为:')
    os.system('adb devices')
    while True:
        if 'yes'==input('如果设备连接正常，请输入yes继续执行程序:\n'):
            break
        else:
            print('error!!!')


#获取屏幕截图
def get_screencap():
    os.system('adb shell screencap  /sdcard/image.png')
    os.system('adb pull /sdcard/image.png   jump.png')
    return cv2.imread('jump.png',0)



#跳跃指令
def jump(distance):
    #经过测试以及从网上获取的数据，1.35对于1080p的屏幕
    #其余分辨率的屏幕尚未测试，等待后续的完善
    press_time=int(distance*1.35)
    #生成移动的随机数
    rand=random.randint(1,10)*10
    click_cmd=('adb shell input swipe %i %i %i %i ' + str(press_time)) \
          % (320 + rand, 410 + rand, 320 + rand, 410 + rand)
    os.system(click_cmd)
    print('此次系统自动点击的坐标为:')
    print(320 + rand, 410 + rand, 320 + rand, 410 + rand)



#获取跳棋的中心的初始位置并返回
def image_match_jump(image,image_temp):
    res=cv2.matchTemplate(image,image_temp,cv2.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res)
    jump_x_center,jump_y_center=max_loc1[0]+39,max_loc1[1]+189
    cv2.rectangle(image,max_loc1,(jump_x_center+w2//2,jump_y_center+15),0,3)
    cv2.imwrite('jump.match.jpg',image)
    return jump_x_center,jump_y_center


def image_match_circle(image,image_temp,canny_image):
    res = cv2.matchTemplate(image, image_temp, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res)
    if max_val1 >0.95:
        print('Success match template  find circle hahahah!!!')
        x_center,y_center=max_loc1[0]+w1//2,max_loc1[1]+h1//2
        cv2.circle(image,(x_center,y_center), 10, (0,0,255), -1)
        cv2.imwrite('image_circle.jpg',image)
        return x_center,y_center
    else:
        print('Edge scanning')
        x_top,y_top=find_top(canny_image)
        y_bottom=find_botton(canny_image,x_top,y_top)
        return x_top,(y_top+y_bottom)//2


def find_top(canny_image):
    H,W=canny_image.shape
    for h in range(400, H):
        for w in range(W//8, W):
            if canny_image[h, w] != 0:
                x_top,y_top=w,h
                return x_top,y_top

def find_botton(canny_image,x_top,y_top):
    H, W = canny_image.shape
    for h in range(y_top+30,H):
        if  canny_image[h, x_top] != 0:
            y_bottom=h
            return y_bottom


def get_distance(x1,y1,x2,y2):
    dis=(x2-x1)**2+(y2-y1)**2
    dis=dis**0.5
    return dis




if __name__=='__main__':
    #获取设备连接信息
    get_devices_message()
    #获取已知图片的特征，方面下面的特征匹配
    # 小圆圈匹配
    temp_circle = cv2.imread('temp_white_circle.jpg', 0)
    w1, h1 = temp_circle.shape[::-1]
    # 跳棋的匹配
    temp_jump = cv2.imread('temp_player.jpg', 0)  #jump__play2.png  temp_player.jpg
    w2, h2 = temp_jump.shape[::-1]

    for m in range(1000):#默认循环1000次
        #获取屏幕截图 jump.png 并匹配跳棋的位置
        #获取跳棋的起始位置
        x1,y1=image_match_jump(get_screencap(),temp_jump)

        image=cv2.imread('jump.png',0)
        image_brg = cv2.GaussianBlur(image, (5, 5), 0)
        canny_image = cv2.Canny(image_brg, 1, 10)



        x2,y2=image_match_circle(get_screencap(), temp_circle, canny_image)
        cv2.line(image,(x1,y1),(x2,y2),0,5)

        cv2.imwrite('jump_line.jpg',image)
        distance=get_distance(x1,y1,x2,y2)
        jump(distance)


        #随机延时程序
        time.sleep(random.uniform(1,2))















