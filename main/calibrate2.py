from sr_emulator import *
from logger import debug
import time
import motor_control

def calibrate2(robot):
    motor_control.addMotorInstruction(robot.motors, [100,100], 0)
    t = time.time()
    robot.see()
    motor_control.skipCurrentInstruction()
    t2 = time.time()
    
    log(t2 - t)
