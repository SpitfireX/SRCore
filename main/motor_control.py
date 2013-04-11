from sr_emulator import *
from logger import debug
import time
import threading
# from computeChanges import computeCoordinates
from math import *

instructions = []
allticks = 0
currentAngle = None
changePoints = None
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
        if (len(speeds) != 2): raise Exception("speeds needs to be a 2-tuple")
        if (not (ticks > 0)): raise Exception("ticks needs to be positive")

        self.speeds = speeds
        self.ticks = ticks
        self.skipped = False

    def setup(self):
        global r
        r.motors[0].target = self.speeds[0] # + 10*cmp(self.speeds[0],0)
        r.motors[1].target = self.speeds[1]

    def run(self):
        global r
        global allticks
        if self.ticks > 0:
            debug("Running for " + str(self.ticks) + " ticks")
            rightTicks = leftTicks = 0

            while rightTicks < self.ticks and leftTicks < self.ticks:
                if self.skipped:
                    break

                res = wait_for(r.io[0].input[3].query.d == 1, r.io[0].input[4].query.d == 1)
                if res[1] != None:
                    rightTicks += 1
                    if r.motors[0].target>1 and r.motors[1].target>1:
                        allticks+=1
                else:
                    leftTicks += 1
                    if r.motors[0].target>1 and r.motors[1].target>1:
                        allticks+=1
            debug("Instruction done")
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

def addPositionInstruction(coor):
    global currentAngle
    global changePoints
    currentCoor = computeCoordinates(allticks, changePoints, currentAngle)
    waypoints = [coor[0] - currentCoor[0], coor[1] - currentCoor[1]]
    angle = degrees(atan2(waypoints[0], waypoints[1]))
    way = sqrt(waypoints[0]**2 + waypoints[1]**2)
    addAngleInstruction(angle)
    addMotorInstruction(way / 80)

def getCurrentAngle():
    global currentAngle
    return currentAngle

def addAngleInstruction(angle):
    global currentAngle
    global changePoints
    ticks = angle/(180/16)
    #print changePoints
    # coor = computeCoordinates(allticks, changePoints, currentAngle)
    # recentTicks = allticks if len(changePoints) == 0 else allticks - changePoints[len(changePoints)-1][2]
    # changePoints.append([currentAngle, coor, recentTicks])
    if ticks < 1:
        ticks = 1
    speed = [70, -70] if angle < 0 else [-70, 70]
    addMotorInstruction(speed, ticks)
    currentAngle += angle

def addImmediateInstruction(speeds = [70,70], ticks = 0):
    global instructions
    instructions = []
    skipCurrentInstruction()
    addMotorInstruction(speeds, ticks)

def addImmediateAngleInstruction(angle):
    global instructions
    skipCurrentInstruction()
    instructions = []
    addAngleInstruction(angle)
