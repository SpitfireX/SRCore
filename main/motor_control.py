from sr_emulator import *
from logger import debug
import threading, time
from logic.computeChanges import computeCoordinates
from math import *

instructions = []
allticks = 0
global currentAngle
global changePoints
currentAngle = 0
changePoints = []

class MotorInstruction():
    def __init__(self, speeds, ticks = 0):
        if (len(speeds) != 2): raise Exception("speeds needs to be a 2-list")
        #if (not (ticks > 0)): raise Exception("ticks needs to be positive")
        self.speeds = speeds
        self.ticks = ticks

    def run(self):
        debug("Running for " + str(self.ticks) + " ticks")
        left.addInstruction(self.speeds[0], self.ticks)
        right.addInstruction(self.speeds[1], self.ticks)

class WheelTickCount(threading.Thread):
    def __init__(self, mode):
        threading.Thread.__init__(self)
        self.mode = mode
        self.cI = None
        self.ticks = 0
        self.skipped = False
    	
    def run(self):
        global r, allticks
        while True:
            if self.cI != None:
                r.motors[self.mode].target = self.cI[0]
                while self.ticks < self.cI[1] and not self.skipped:
                    if self.mode == 0:
                        wait_for(r.io[0].input[2].query.d == 1)
                    else:
                        wait_for(r.io[0].input[3].query.d == 1)
                    self.ticks+=1
                    if r.motors[0].target>=1 and r.motors[1].target>=1:
                        allticks+=1
                    time.sleep(0.02)
                    r.motors[self.mode].target = 0
                    self.cI=None
                    self.skipped=False
					
    def addInstruction(self, speed, ticks):
        self.cI=[speed, ticks]
		
    def skip():
        self.skipped = True
        debug("Skipped current Instruction")
        
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

    global left, right
    left=WheelTickCount(1)
    right=WheelTickCount(0)

    global running
    running = False

def startThread():
    global running
    running = True
    left.start()
    right.start()

def stopThread():
    global running
    running = False

def addMotorInstruction(speeds = [80, 80], ticks = 0):
    global left, right
    if len(speeds) > 0:
        left.addInstruction(speeds[1], ticks)
        right.addInstruction(speeds[0], ticks)
        debug(str(speeds)+" "+str(ticks))

def skipCurrentInstruction():
    global left, right
    debug ("Attempting to skip instruction")
    left.skip()
    right.skip()

def getCurrentInstruction():
    global cI
    return cI.speeds, cI.ticks

def getCurrentAngle():
    global currentAngle
    return currentAngle

def addAngleInstruction(angle):
    global currentAngle
    global changePoints
    ticks = angle/(90/8)
    #print changePoints
    #coor = computeCoordinates(allticks, changePoints, currentAngle)
    #recentTicks = allticks if len(changePoints) == 0 else allticks - changePoints[len(changePoints)-1][2]
    #changePoints.append([currentAngle, coor, recentTicks])
    if ticks < 1:
        ticks = 1
    speed = [100, -100] if angle < 0 else [-100, 100]
    addMotorInstruction(speed, ticks)
    currentAngle += angle

def addImmediateInstruction(speeds = [100, 100], ticks = 0):
    global instructions
    instructions = []
    skipCurrentInstruction()
    addMotorInstruction(speeds, ticks)

def addImmediateAngleInstruction(angle):
    global instructions
    skipCurrentInstruction()
    instructions = []
    addAngleInstruction(angle)

def driveUntilPressed():
    addMotorInstruction([70, 70], -1)
    wait_for(And(r.io[0].input[6].query.d == 1, r.io[0].input[7].query.d == 1))
    skipCurrentInstruction()
