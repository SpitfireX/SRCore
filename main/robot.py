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
wait_for(robot.io[0].input[0].query.d, robot.io[0].input[1].query.d)
debug("Adding instructions")
for i in 90, 180, 25:
    debug("Add instruction "+str(i)+" degrees?") 
    wait_for(robot.io[0].input[0].query.d, robot.io[0].input[1].query.d)
    motor_control.addAngleInstruction(i)
