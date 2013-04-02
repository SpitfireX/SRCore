from sr_emulator import *
from logger import debug
import motor_control, sensor_control, calibrate2, logic_control

robot = Robot()
running = False

def initRobot():
    debug("Initializing Robot")

    # sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)

    # sensor_control.startThread()
    motor_control.startThread()
    debug("Finished robot initializsation")

def startEventLoop():
    global running
    running = True

    while running:
        events = sensor_control.getChanges()
        logic_control.processEvents(events)

def stopEventLoop():
    global running
    running = False

initRobot()
# startEventLoop()
debug("Waiting for button")
angle=0
while True:
    wait_for(robot.io[0].input[0].query.d==0, robot.io[0].input[1].query.d==0)
    wait_for(robot.io[0].input[0].query.d==1, robot.io[0].input[1].query.d==1)
    if angle == 0:
        robot.servos[0][0]=angle=60
    else:
        robot.servos[0][0]=angle=0
    
