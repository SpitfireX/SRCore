from sr import *
from logger import debug
from strategy import *
from logic.computeChanges import *
import motor_control, sensor_control, logic_control
import time

robot = Robot()
running = False

def initRobot():
    debug("Initializing Robot")

    sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)

    motor_control.startThread()
    initialActions()
    sensor_control.startThread()
    debug("Finished robot initializsation")

def initialActions():
    ctr = 0
    while True:
        motor_control.addAngleInstruction(20)
        markers = robot.see()
    	for m in markers:
            if m.info.marker_type == MARKER_ARENA and m.dist < 2100:
                code = m.info.code
                coor = m_info(code)
                motor_control.currentAngle = 0 if code == 0 or code == 3 else 180
				home = (coor[0]-m.centre.world.x, coor[1]-m.centre.world.y)
				strategy.home = home
                motor_control.addAngleInstruction(-ctr*20)
                break
        
        ctr += 1

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
