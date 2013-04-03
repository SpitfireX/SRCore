from sr import *
from logger import debug
from strategy import Strategy
from logic.computeChanges import computeAbsolutePositionByArenaMarker
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
        sensor_control.event.wait()
        markers = sensor_control.getChanges()
        sensor_control.event.clear()
        # debug("Markers: " + str(len(events)))
        # strategy.act(events)
        for m in markers:
            if m.info.marker_type == MARKER_ARENA:
              debug("Computed position:  " + str(computeAbsolutePositionByArenaMarker(m)))

def stopEventLoop():
    global running
    running = False

initRobot()
startEventLoop()
