from sr import *
from logger import log
import motor_control, sensor_control, calibrate2
import time

robot = Robot()

def initRobot():
    log("Initializing Robot")
    
    sensor_control.initSensorControl(robot)
    motor_control.initMotorControl(robot)
    
    sensor_control.startThread()
    motor_control.startThread()
    log("Finished robot initializsation")
    
    startEventLoop()
    
def startEventLoop():
    log("Nothing to see here, move along!")

initRobot()

while True:
    log("waiting for input...")
	wait_for(robot.io[0].input[0].query.d == 1, robot.io[0].input[1].query.d == 1)

	log("started program")

        if len(motor_control.instructions) == 0:
            for i in range(10, 110, 10):
                log("Adding instruction")
                motor_control.addMotorInstruction(robot.motors, [i, i], 5)
