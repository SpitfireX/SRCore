from sr import *
from motor_control import *
import os

r = Robot()

def initRobot():
    print "Initializing Robot"
    initMotorControl()
    print "Finished robot initializsation"
    startEventLoop()
    
def startEventLoop():
    print "Noting to see here, move along!"

initRobot()

addMotorInstruction(r.motors, [80, 80], 5)
addMotorInstruction(r.motors, [-80, -80], 5)
addMotorInstruction(r.motors, [20, 60], 2)
addMotorInstruction(r.motors, [60, 20], 2)
addMotorInstruction(r.motors, [80, 80], 0)