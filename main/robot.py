from sr import *
from logger import debug
from strategy import Strategy
import motor_control, sensor_control, logic_control
import time

robot = Robot()
running = False

def initRobot():
    debug("Initializing Robot")

    sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)

    sensor_control.startThread()
    motor_control.startThread()
    debug("Finished robot initializsation")

def startEventLoop():
    debug("Starting event loop")
    global running
    running = True
    strategy = Strategy(robot)

    while running:
        events = sensor_control.getChanges()
        if len(events) != 0:
            debug("Markers: " + str(len(events)))
            strategy.act(events)

def stopEventLoop():
    global running
    running = False

initRobot()
startEventLoop()
