from sr_emulator import *
from logger import debug
import time
import threading
from computeChanges import computeCoordinates

instructions = []
allticks = 0
global currentAngle
global changePoints
currentAngle = 0
changePoints = []

class MotorCotrolThread(threading.Thread):
    cI = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "MotorControl"

    def run(self):
        debug("Started MotorControl Thread")

        global running
        running = True

        while running:
            global cI
            if len(instructions) > 0:
                cI = instructions.pop(0)
                cI.setup()
                cI.run()
            else:
                #debug("no instructions")
                cI = None
                for m in r.motors:
                    m.target = 0

    def skip(self):
        if cI is not None:
            cI.skipped = True
            debug("    skipping instruction")
        else:
            debug("    noting to skip")

class MotorInstruction():
    def __init__(self, motors, speeds, ticks = 0):
        self.motors = motors
        self.speeds = speeds
        self.ticks = ticks
        self.skipped = False

    def setup(self):
        #debug("Instruction: " + str(self.motors) + " " + str(self.speeds) + " " + str(self.ticks))
        for i in range(len(self.motors)):
            self.motors[i].target = self.speeds[i]

    def run(self):
        global r
        if self.ticks > 0:
            debug("Running for " + str(self.ticks) + " ticks")
            rightTicks = leftTicks = 0

            while rightTicks < self.ticks and leftTicks < self.ticks:
                if self.skipped:
                    break

                # TODO: use right pins
                debug("Waiting for pins")
                res = wait_for(r.io[0].input[3].query.d == 1, r.io[0].input[4].query.d == 1)
                if res[1] != None:
                    rightTicks += 1
                    debug("Right pin triggered")
                    if r.motors[0].target>1 and r.motors[1].target>1:
                        allticks+=1
                else:
                    leftTicks += 1
                    debug("Left pin triggered")
                    if r.motors[0].target>1 and r.motors[1].target>1:
                        allticks+=1
        else:
            debug("Running forever")
            while not self.skipped:
                time.sleep(0.1)

def initMotorControl(robot):
    debug("Initializing MotorControl")

    global r
    r = robot

    global thread
    thread = MotorCotrolThread()

    global running
    running = False

    global v
    global w
    # v, w = calibrate(r)
    # checkCalibrating()

def getTicks():
    return allticks/2

def getCurrentAngle():
    return currentAngle

def startThread():
    global running
    running = True
    thread.start()

def stopThread():
    global running
    running = False

def addMotorInstruction(motors, speeds, ticks = 0):
    i = MotorInstruction(motors, speeds, ticks)
    instructions.append(i)

def skipCurrentInstruction():
    debug ("Attempting to skip instruction")
    thread.skip()

def getCurrentInstruction():
    global cI
    return cI.speeds, cI.ticks

def addAngleInstruction(angle):
    global currentAngle
	global changePoints
	ticks = angle/(180/15)
	print changePoints
	coor = computeCoordinates(allticks, changePoints, getCurrentAngle())
	recentTicks = getTicks() if len(changePoints) == 0 else getTicks() - changePoints[len(changePoints)-1][2]
	changePoints.append([getCurrentAngle(), coor, recentTicks])
	if ticks < 1:
		ticks = 1
	speed = [70, -70] if angle < 0 else [-70, 70]
	addMotorInstruction(r.motors, [70, -70], ticks)
	currentAngle += angle
