from sr_emulator import *
from logger import log
import motor_control, sensor_control, calibrate2, logic_control

robot = Robot()
running = False

def initRobot():
    log("Initializing Robot")

    # sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)

    # sensor_control.startThread()
    motor_control.startThread()
    log("Finished robot initializsation")

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
# log("Waiting for input 0")
# wait_for(robot.io[0].input[0].query.d == 1, robot.io[0].input[1].query.d == 1)
log("Waiting for button")
wait_for(robot.io[0].input[0].query.d, robot.io[0].input[1].query.d)
log("Adding instructions")
motor_control.addMotorInstruction(robot.motors,[50,50],1)
