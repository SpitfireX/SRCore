
from sr import *
from logger import debug
from strategy import *
from logic.computeChanges import *
import motor_control, sensor_control, logic_control, servo_control
import time

robot = Robot()
running = False

def initRobot():
    debug("Initializing Robot")

    sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)
    motor_control.currentAngle = 0
    motor_control.startThread()
    initialActions()
    sensor_control.startThread()
    servo_control.initServoControl(robot)
    debug("Finished robot initializsation")

def initialActions():
    ctr = 0
    while True:
        motor_control.addAngleInstruction(45)
        time.sleep(2)
        sensor_control.event.wait()
        markers = sensor_control.getMarkers()
        sensor_control.event.clear()
        if len(markers)>0:
            for m in markers:
                if m.info.marker_type == MARKER_ARENA and m.dist < 2100:
                    code = m.info.code
                    strategy.homenumber = 0 if 0 <= code <= 6 else 1 if 21 <= code <= 27 else 2 if 14 <= code <= 20 else 3
                    coor = m_info[code]
                    homecoor = computeAbsolutePositionByArenaMarker(m)
                    motor_control.currentAngle = homecoor[2]
                    home = (homecoor[0], homecoor[1])
                    strategy.home = home
                    motor_control.addAngleInstruction(-ctr*30)
                    debug("Token found!")
                    break
        else:
            debug("No token found!")
        
        ctr += 1

def startEventLoop():
    debug("Starting event loop")
    global running
    running = True
    strategy = Strategy(robot) 
    while running:
        sensor_control.event.wait()
        markers = sensor_control.getMarkers()
        sensor_control.event.clear()
        strategy.reach(markers)

def stopEventLoop():
    global running
    running = False

initRobot()
startEventLoop()
