from sr_emulator import *
from logger import debug
import time
import threading
from logic.computeChanges import computeCoordinates
from math import *

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
            debug("    nothing to skip")

class MotorInstruction():
    def __init__(self, speeds, ticks = 0):
        if (len(speeds) != 2): raise Exception("speeds needs to be a 2-list")
        if (not (ticks > 0)): raise Exception("ticks needs to be positive")
        self.speeds = speeds
        self.ticks = ticks
        self.skipped = False

    def setup(self):
        global r
        r.motors[0].target = self.speeds[0]
        r.motors[1].target = self.speeds[1] + 10

    def run(self):
        global r, allticks
        if self.ticks > 0:
            debug("Running for " + str(self.ticks) + " ticks")
            rightTicks = leftTicks = 0
    		
            wait_for(And(r.io[0].input[2].query.d==0, r.io[0].input[3].query.d==0))
            while rightTicks < self.ticks and leftTicks < self.ticks:
                if self.skipped:
                    break
                # TODO: use right pins
					
                debug("Waiting for pins")
                res = wait_for(r.io[0].input[2].query.d == 1, r.io[0].input[3].query.d == 1)
                if res[1] != None:
                    rightTicks += 1
                    debug("Right pin triggered")
                    if r.motors[0].target>1 and r.motors[1].target>1:
                        allticks += 1
                else:
                    leftTicks += 1
                    debug("Left pin triggered")
                    if r.motors[0].target>1 and r.motors[1].target>1:
                        allticks+=1
                print allticks
                time.sleep(0.4)
        else:
            debug("Running forever")
            while not self.skipped:
                time.sleep(0.4)

def getCurrentAngle():
	global currentAngle
	return currentAngle
	
def getTicks():
	global allticks
	return allticks

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
	
def startThread():
    global running
    running = True
    thread.start()

def stopThread():
    global running
    running = False

def addMotorInstruction(speeds = [70, 70], ticks = 0):
    i = MotorInstruction(speeds, ticks)
    instructions.append(i)

def skipCurrentInstruction():
    debug ("Attempting to skip instruction")
    thread.skip()

def getCurrentInstruction():
    global cI
    return cI.speeds, cI.ticks
	
def getCurrentAngle():
	global currentAngle
	return currentAngle

def addAngleInstruction(angle):
	global currentAngle
	global changePoints
	ticks = angle/(90/9)
	print changePoints
	#coor = computeCoordinates(allticks, changePoints, currentAngle)
	#recentTicks = allticks if len(changePoints) == 0 else allticks - changePoints[len(changePoints)-1][2]
	#changePoints.append([currentAngle, coor, recentTicks])
	if ticks < 1:
		ticks = 1
	speed = [70, -70] if angle < 0 else [-70, 70]
	addMotorInstruction(speed, ticks)
	currentAngle += angle
	time.sleep(0.5)

def driveUntilPressed():
    addMotorInstruction([30, 30], -1) 
    wait_for(And(r.io[0].input[6].query.d == 1, r.io[0].input[7].query.d == 1))
    skipCurrentInstruction()
