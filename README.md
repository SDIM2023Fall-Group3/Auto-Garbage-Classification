# Auto-Garbage-Classification
classify garbage by mobilenetV2/api based on ali cloud

基于课程要求制作的智能分类垃圾桶，对识别算法没有要求所以除了深度学习代码还有一个调用api的代码（api的使用详情请查询阿里云相关文档），可将垃圾分为可回收垃圾和其他垃圾。

分别包含树莓派可用的python文件以及arduino使用的ino文件。

树莓派控制摄像头，arduino控制开关门的舵机、翻转平台的电机、光敏模块、灯带。

整体流程为遮挡激光并取消遮挡被视为垃圾投入，期间根据光敏模块信号控制led灯带。投入后舵机控制关门，接着摄像头拍照，在树莓派中进行图像识别（识别时间3s以内，除非网不好），返回信号，电机控制翻转平台将垃圾导入垃圾桶。流程结束舵机控制开门，如果灯带为开则关闭灯带。

![image](https://github.com/SDIM2023Fall-Group3/Auto-Garbage-Classification/blob/main/img/ke.jpg)

整机上半部分长这样，大概能想象出来工作流程吧（笑）。

总之基本就这样，第一次传github可能写的有问题，但是无所谓。

以后看心情更新（基本不会）。
