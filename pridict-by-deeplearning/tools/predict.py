# -*- coding: utf-8 -*-
#该程序含有激光代码
import torch

from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt
import json

import time

from torchvision.models import MobileNetV2

import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LaserGPIO = 17
ReceiveGPIO = 18

GPIO_LEFT = 22
GPIO_RIGHT = 23

GPIO.setup(GPIO_LEFT,GPIO.OUT)
GPIO.setup(GPIO_RIGHT,GPIO.OUT)

GPIO.setup(LaserGPIO,GPIO.OUT)
GPIO.setup(ReceiveGPIO,GPIO.IN)
GPIO.output(LaserGPIO,GPIO.HIGH)

print('aaa')

cap = cv2.VideoCapture(0)                               
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print('bbb')
hand = 0


if __name__ == '__main__':
    try:
        while True:
            level = 0
            item = 0
            if(GPIO.input(ReceiveGPIO) == 1 and hand == 0):
                hand = 1
                item = 0
            elif(GPIO.input(ReceiveGPIO) == 0 and hand == 1):
                hand = 0
                item = 1
            else:
                item = 0
            time.sleep(1)
            print(f'item= {item}, hand= {hand}')
            
            if(item == 1):
                cur_time=time.time()
                ret, frame = cap.read()
                cv2.imwrite("photo1.jpg", frame)
                #cap.release()
                

                #print(torch.__version__)
                #将图片裁剪，转化为张量
                data_transform = transforms.Compose(
                    [transforms.Resize(256),
                     transforms.CenterCrop((144,256)),
                     transforms.ToTensor()])
                
                '''data_transform = transforms.Compose(
                    [transforms.Resize(256),
                     transforms.CenterCrop((144,256)),
                     transforms.ToTensor(),
                     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])'''#将图片归一化

                # load image
                img = Image.open("/home/pi/predict-garbage-with-pi-master/tools/photo1.jpg")
                #plt.imshow(img)
                # [N, C, H, W]
                img = data_transform(img)
                
                plt.imshow(img.permute(1,2,0))
                plt.show()#显示转化后的图片
                # expand batch dimension
                img = torch.unsqueeze(img, dim=0)
                #print("img:", img)


                try:
                    json_file = open('./class_indices.json', 'r')
                    class_indict = json.load(json_file)
                except Exception as e:
                    print(e)
                    exit(-1)

                # create model
                model = MobileNetV2(num_classes=1085)
                # load model weights
                model_weight_path = "./mobilenet_v2_xxx.pth"
                model.load_state_dict(torch.load(model_weight_path))
                # torch.load(model_weight_path)
                model.eval()
                with torch.no_grad():
                    # predict class
                    output = torch.squeeze(model(img))
                    predict = torch.softmax(output, dim=0)
                    predict_cla = torch.argmax(predict).numpy()
                print(predict_cla)
                #predict_cla = int(predict_cla)
                #print(type(predict_cla))
                #plt.show()
                if(predict_cla == 0):
                    print("bag")
                    level = 2
                elif(predict_cla == 1):
                    print("bottle")
                    level = 1
                elif(predict_cla == 2):
                    print("metal")
                    level = 1
                elif(predict_cla == 3):
                    print("tissue")
                    level = 2
                    
                end_time=time.time()
                print('Time taken:',end_time - cur_time)
                    
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
                    
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        cap.release()
        GPIO.cleanup()
        
