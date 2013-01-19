from sr_emulator import *
import motor_control
import time

robot = Robot()

def initRobot():
    print "Initializing Robot"
    motor_control.initMotorControl(robot)
    print "Finished robot initializsation"
    
    startEventLoop()
    
def startEventLoop():
    print "Noting to see here, move along!"

initRobot()

#motor_control.addMotorInstruction(robot.motors, [80, 80], 5)
#motor_control.addMotorInstruction(robot.motors, [-80, -80], 5)
#motor_control.addMotorInstruction(robot.motors, [20, 60], 2)
#motor_control.addMotorInstruction(robot.motors, [60, 20], 2)
motor_control.addMotorInstruction(robot.motors, [80, 80], 0)
time.sleep(2)
motor_control.skipCurrentInstruction()
