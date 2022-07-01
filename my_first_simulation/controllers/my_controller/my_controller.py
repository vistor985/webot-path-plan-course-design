# from controller import Robot, DistanceSensor, Motor
# import time
# time in [ms] of a simulation step
# TIME_STEP = 2

# MAX_SPEED = 6.28

# create the Robot instance.
# robot = Robot()

# tstart=0
# tend=0

# initialize devices
# ps = []
# psNames = [
    # 'ps0', 'ps1', 'ps2', 'ps3',
    # 'ps4', 'ps5', 'ps6', 'ps7'
# ]

# for i in range(8):
    # ps.append(robot.getDevice(psNames[i]))
    # ps[i].enable(TIME_STEP)

# leftMotor = robot.getDevice('left wheel motor')
# rightMotor = robot.getDevice('right wheel motor')
# leftMotor.setPosition(10)
# rightMotor.setPosition(10)
# leftMotor.setVelocity(0.0)
# rightMotor.setVelocity(0.0)
# leftSpeed  = 0.8 * MAX_SPEED
# rightSpeed = 0.7 * MAX_SPEED
# feedback loop: step simulation until receiving an exit event
# while robot.step(TIME_STEP) != -1:
    # read sensors outputs
    # psValues = []
    # for i in range(8):
        # psValues.append(ps[i].getValue())

    # detect obstacles
    # right_obstacle = psValues[0] > 80.0 or psValues[1] > 80.0 or psValues[2] > 80.0
    # left_obstacle = psValues[5] > 80.0 or psValues[6] > 80.0 or psValues[7] > 80.0

    # initialize motor speeds at 50% of MAX_SPEED.
    # leftSpeed  = 0.8 * MAX_SPEED
    # rightSpeed = 0.7 * MAX_SPEED
    
    # if tstart==0:
       # tstart=time.time()
    # tend=time.time()
    # if tend-tstart>10:
       # leftMotor.setVelocity(0.3 * MAX_SPEED)
       # rightMotor.setVelocity(0.3 * MAX_SPEED)
    # modify speeds according to obstacles
    # if left_obstacle:
        # turn right
        # leftSpeed  = 0.5 * MAX_SPEED
        # rightSpeed = -0.5 * MAX_SPEED
    # elif right_obstacle:
        # turn left
        # leftSpeed  = -0.5 * MAX_SPEED
        # rightSpeed = 0.5 * MAX_SPEED
    # write actuators inputs
    # leftMotor.setVelocity(leftSpeed)
    # rightMotor.setVelocity(rightSpeed)
    
from controller import Robot, Motor
import time
TIME_STEP = 2
MAX_SPEED = 6.28
# create the Robot instance.
robot = Robot()


# get a handler to the motors and set target position to infinity (speed control)
tstart=0
tend=0

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
# leftMotor.setPosition(10)
# rightMotor.setPosition(10)
# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(0.8 * MAX_SPEED)
rightMotor.setVelocity(0.7 * MAX_SPEED)


while robot.step(TIME_STEP) != -1:
   if tstart==0:
       tstart=time.time()
   tend=time.time()
   if tend-tstart>5.5:
       leftMotor.setVelocity(0.3 * MAX_SPEED)
       rightMotor.setVelocity(0.3 * MAX_SPEED)
   pass