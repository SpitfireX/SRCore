from sr import *
from logger import log
import motor_control, sensor_control, calibrate2, logic_control
import time

robot = Robot()
running = False

def initRobot():
    log("Initializing Robot")
    
    sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)
    
    sensor_control.startThread()
    motor_control.startThread()
    log("Finished robot initializsation")
    
def startEventLoop():
    global running
    running = True
    
    while running:
        events = sensor_control.getChanges()
        logic_control.processChanges(events)
        
def stopEventLoop():
    global running
    running = False

initRobot()
startEventLoop()
