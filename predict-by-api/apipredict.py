# -*- coding: utf-8 -*-
# 导入库
print('Importing time')
import time

print('Importing Image...')
from PIL import Image

print('Importing plt...')
import matplotlib.pyplot as plt
print('Importing cv2...')
import cv2
print('Importing RPi.GPIO...')
import RPi.GPIO as GPIO

#import os
#import io
print('Importing alibabacloud...')
# 防止导入失败
while True:
    try:
        from urllib.request import urlopen
        from alibabacloud_imagerecog20190930.client import Client
        from alibabacloud_imagerecog20190930.models import ClassifyingRubbishAdvanceRequest
        from alibabacloud_tea_openapi.models import Config
        from alibabacloud_tea_util.models import RuntimeOptions
        break
    except Exception as e:
        #img = Image.open("/home/pi/predict-garbage-with-pi-master/tools/photo1.jpg")
        print("error:",e)
        continue

print('Import finished')

#设置相关引脚

GPIO.setmode(GPIO.BCM)

ReceiveGPIO = 18 #接收ardiuno信号的引脚

GPIO_LEFT = 22#给ardiuno发送向左运动信号的引脚
GPIO_RIGHT = 23#给ardiuno发送向右运动信号的引脚

GPIO.setup(GPIO_LEFT,GPIO.OUT)#将给ardiuno发送信号的引脚设置为输出模式
GPIO.setup(GPIO_RIGHT,GPIO.OUT)

GPIO.setup(ReceiveGPIO,GPIO.IN)#将接收ardiuno信号的引脚设置为输入模式

print('Openning camera...')

cap = cv2.VideoCapture(0)#打开摄像头                               
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)#设置图片分辨率
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print('Camera opened')

print('启动！')

if __name__ == '__main__':
    try:
        while True:
            item = 0
            
            if(GPIO.input(ReceiveGPIO) == 1):
                item = 1
                print('Garbage detected')#当接收到信号时，标记检测到垃圾
                
            if(item == 1):
                print('Capturing...')
                cur_time = time.time()
                
                ret, frame = cap.read()
                cv2.imwrite("/home/pi/predict/photo1.jpg", frame)
                
                img = cv2.imread('/home/pi/predict/photo1.jpg')
                print(img.shape)
                cropped = img[96:463,265:1030]#将图片裁剪为适当的大小
                cv2.imwrite("/home/pi/predict/photo1.jpg", cropped)
                
                end_time = time.time()
                print('Capture time:',end_time - cur_time,'s')#显示拍摄用时
                #cap.release()
                print('Recognizing...')
                
                cur_time = time.time()
                
                #设置api的id与secret
                config = Config(
                  access_key_id="YOUR_ACCESS_KEY_ID",
                  access_key_secret='YOUR_ACCESS_KEY_SECRET',
                  endpoint='imagerecog.cn-shanghai.aliyuncs.com',
                  region_id='cn-shanghai'
                )
                img = open('/home/pi/predict/photo1.jpg', 'rb')
                classifying_rubbish_request = ClassifyingRubbishAdvanceRequest()
                classifying_rubbish_request.image_urlobject = img
                runtime = RuntimeOptions()
                try:
                  client = Client(config)
                  response = client.classifying_rubbish_advance(classifying_rubbish_request, runtime)
                  print(response.body)
                  a = str(response.body.data.elements[0])
                  b=((a.split(','))[0])[14:-1]#将返回信号缩减为必要信息
                  #print(b)
                  
                except Exception as error:
                  print(error)
                  print(error.code)
                  
                if(b == '可回收垃圾'):
                    print(b)
                    print('Recyclable')
                    level = 1
                elif(b ==''):
                    print('Invalid item')
                    level = 2
                else:
                    print(b)
                    print('Others')
                    level = 2
                    
                if(level == 1):
                    GPIO.output(GPIO_LEFT,GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(GPIO_LEFT,GPIO.LOW)
                    print('Left')
                    
                elif(level == 2):
                    GPIO.output(GPIO_RIGHT,GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(GPIO_RIGHT,GPIO.LOW)
                    print('Right')
                    
                elif(level == 0):
                    print('Failed to recognize')
                    
                end_time = time.time()
                print('Recogonition time：',end_time - cur_time,'s')#显示识别时间
                #time.sleep(5)
                        
    except KeyboardInterrupt:
        print("Measurement stopped by User")#按ctrl+C退出程序
        print('Closing camera...')
        cap.release()
        print('Camera closed')
        GPIO.cleanup()
        
