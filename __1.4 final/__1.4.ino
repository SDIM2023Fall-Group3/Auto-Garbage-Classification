#include <Servo.h>
#include <AccelStepper.h>
#include <FastLED.h>

#define DirectionPin 4
#define PulsePin 11
#define LED_PIN 13
#define NUM_LEDS 20

int hereHand = 0;

Servo myservo;// 创建Servo对象
AccelStepper myStepper(1, PulsePin, DirectionPin);//创建一个步进电机对象
CRGB leds[NUM_LEDS];

void setup() 
{
pinMode(9,OUTPUT);//设置引脚9是发出舵机控制信号的引脚
pinMode(12,OUTPUT);//设置引脚12是发出树莓派激活信号的引脚
pinMode(2,INPUT);//设置引脚2为接受树莓派信号的引脚
pinMode(3,INPUT);//设置引脚3为接受树莓派信号的引脚
pinMode(5,INPUT_PULLUP);//设置引脚5是接收激光1信号的引脚
pinMode(6,INPUT_PULLUP);//设置引脚6是接收激光2信号的引脚
pinMode(A3,INPUT_PULLUP);//设置引脚A3是接收开灯信号的引脚
pinMode(13,OUTPUT);//设置引脚13是发出开灯信号的引脚

Serial.begin(9600);//设置串口波特率9600
myStepper.setMaxSpeed(80000.0);    // 设置电机最大速度为每秒500步,最大值20000左右（最初step_motor代码所测）
myStepper.setSpeed(80000.0);  //设置电机当前速度为每秒500步
myStepper.setAcceleration(7000);  // 设置电机加速度

myservo.attach(9,500,2500);// 将舵机连接到数字9接口
myservo.writeMicroseconds(500);

FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
turnOffLight();
}

int laser() //读取2个激光信号
{
 int hereIsHand = 0;
 int laser2 = digitalRead(5);
 int laser3 = digitalRead(6);
 if(laser3 == 0||laser2 == 0)
   hereIsHand = 1;//如果激光检测到东西，说明有手，hereIsHand改为1
 return hereIsHand;
}

void move1()  //向一侧移动
{
myStepper.move(5500);
myStepper.runToPosition();
}

void move2()
{
myStepper.move(-5500);
myStepper.runToPosition();
}

void turnover1()//其他
{
move1();
delay(10);
move2();
delay(10);
}

void turnover2()//可回收
{
move2();
delay(10);
move1();
delay(10);
}

void shutDoor()//自动关门
{
 myservo.writeMicroseconds(1076);
 delay(2000);
 myservo.writeMicroseconds(500);
}

void openLight()
{
    for (int i = 0; i <= 19; i++) {
    leds[i] = CRGB ( 255, 255, 255);
    FastLED.show();}
}

void turnOffLight()
{
    for (int i = 0; i <= 19; i++) {
    leds[i] = CRGB ( 0, 0, 0);
    FastLED.show();}
}

void loop() 
{
/*if(setUpPosition == 0)//还未初始化位置
 {
  delay(500);
  myStepper.move(30000);
  myStepper.run();
  int button = digitalRead(10); //没东西-0，有东西-1
  Serial.println(button);
  if(button == 1) 
  {
    setUpPosition = 1;  
    Serial.println(button);
    Serial.print("111111setUpPosition = ");
    Serial.println(setUpPosition);
    myStepper.setCurrentPosition(0); //初始化位置：设置当前位置为0，同时将当前速度设为0
    myStepper.setSpeed(10000.0);  //重设速度
    move2();//到达中点
    delay(10);
  }
 }
else //已经初始化位置
 {*/


//如果激光开始有1，再没1，就激活树莓派
hereHand = laser();//读取3个激光信号
delay(50);
if(hereHand == 1)
{
  delay(250);
  hereHand = laser();
  if(hereHand == 0)//手进来又出去
 {
  if(digitalRead(A3) == HIGH)//如果需要开灯
  {
    openLight();
  }
  else{turnOffLight();}
  delay(1000);
  digitalWrite(12,HIGH);//给树莓派高电平
  delay(200);
  digitalWrite(12,LOW);
  
  myservo.writeMicroseconds(1100);
 }
}
//else if(hereHand == 0) Serial.println("0");

/*if(digitalRead(A3) == HIGH)//如果需要开灯
  {
    Serial.println("开灯");
    for (int i = 0; i <= 59; i++) {
    leds[i] = CRGB ( 255, 255, 255);
    FastLED.show();}
  }
  else{
    Serial.println("关灯");
    for (int i = 0; i <= 59; i++) {
    leds[i] = CRGB ( 0, 0, 0);
    FastLED.show();}
 }*/

 
if (digitalRead(2) == 1 || digitalRead(3) == 1)  //树莓派有数据输入时，执行下面语句
  {
  if (digitalRead(2) == 1)
   {
   turnover1();
   delay(10); //单位为ms
   myservo.writeMicroseconds(500);
   turnOffLight();
   }
  if (digitalRead(3) == 1)
   {
   turnover2();
   delay(10); //单位为ms
   myservo.writeMicroseconds(500);
   turnOffLight();
   }
  }
}
