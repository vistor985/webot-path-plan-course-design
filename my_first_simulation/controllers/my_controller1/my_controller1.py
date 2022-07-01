from controller import Robot
from controller import Motor
from controller import Camera
from controller import Robot
from controller import GPS
from controller import CameraRecognitionObject
import math
import numpy as np

def vec(me, you):
    vecget = np.array(you)-np.array(me)
    return vecget.tolist()


def costheta(me, forward, aim):
    vecm2f = np.array(vec(me, forward))
    vecm2a = np.array(vec(me, aim))
    # print("vecm2f",vecm2f)
    # print("vecm2a",vecm2f)
    costhe = np.multiply(vecm2f, vecm2a).sum(
    )/(np.sqrt((vecm2f**2).sum())*np.sqrt((vecm2a**2).sum()))
    # print("costhe",costhe)
    return costhe
    
    
def turnlef(vecm2f, vecm2a):
    lab = vecm2f[0]*vecm2a[2]-vecm2f[2]*vecm2a[0]
    # print("lab",lab)
    if lab < 0:
        return True
    else:
        return False


#模拟步长
TIME_STEP = 64
robot = Robot()
gps = robot.getDevice("gps")
gps.enable(TIME_STEP)
gps1 = robot.getDevice("gps(1)")
gps1.enable(TIME_STEP)
#初始化距离传感器
ds = []
dsNames = ['ds_right', 'ds_left']
for i in range(2):
   ds.append(robot.getDevice(dsNames[i]))
   ds[i].enable(TIME_STEP)
#初始化电机

CAMERA = robot.getDevice("camera");
CAMERA.enable(TIME_STEP);
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0


aim = [1,0.3976,0]
forpos = 0
avoidthen = 0
countstep = 0
turn180 = 0 # 防止180度角的震荡
turnon180 = 0
while robot.step(TIME_STEP) != -1:
    countstep += 1
    pos = gps.getValues() # 车头的gps
    pos1 = gps1.getValues() # 车尾的gps
    cos = costheta(pos1, pos, aim) # 夹角余弦值
    vecm2f = np.array(vec(pos1, pos)) # 车子向量
    vecm2a = np.array(vec(pos1, aim)) # 车尾到目标向量
    tlf = turnlef(vecm2f,vecm2a) # 判断是否左转
    CAMERA.recognitionEnable(TIME_STEP)
    numberOfObjects = CAMERA.getRecognitionNumberOfObjects()
    OBJECTS = CAMERA.getRecognitionObjects()
    if (CAMERA.hasRecognition):#如果图像中有可识别物体
        my_object = CAMERA.getRecognitionObjects()#把物体object返回到my_object
        for i in range (numberOfObjects):
            # print(my_object[i].model)
            pass

    # print(numberOfObjects)
    #初始化速度
    leftSpeed = 2.0
    rightSpeed = 2.0
    aimdis = math.sqrt(sum([(aim - pos)**2 for (aim,pos) in zip(aim,pos)]))
    # print("forpos",forpos)
    # print("aimdis",aimdis)
    if aimdis<0.5:
        leftSpeed = 0
        rightSpeed = 0
        
    elif avoidObstacleCounter > 0:
        if turnon180 > 0:
            leftSpeed = 2.0*turn180
            rightSpeed = -2.0*turn180
            turnon180 -= 1
        # print(avoidObstacleCounter)
        if avoidObstacleCounter >1:
            
            if tlf:
                leftSpeed = 2.0
                rightSpeed = -2.0
            else:
                leftSpeed = -2.0
                rightSpeed = 2.0
        else:
            avoidthen = 33
        avoidObstacleCounter -= 1
    elif (1 - cos)>(0.085/aimdis):
        if avoidthen>0:
            avoidthen -= 1
            leftSpeed = 2.0
            rightSpeed = 2.0
        else:
            # print("tlf",tlf)
            if tlf:
                leftSpeed = -2
                rightSpeed = 2
            else:
                leftSpeed = 2
                rightSpeed = -2
        
    # else:  # read sensors
    if turnon180 <= 0:
    
        for i in range(2):
            if ds[i].getValue() < 850.0:
                avoidObstacleCounter = 18
                if (1 - cos)>1.9:
                    if tlf:
                        turn180 = 1
                    else:
                        turn180 = -1
                    turnon180 = 150
                    avoidObstacleCounter = 150
            
    #设置电机速度
    forpos = aimdis
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
    if aimdis<0.5:
        print(countstep)
        break