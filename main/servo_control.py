from time import sleep
from logger import debug
from sr_emulator import *

grab_servo = 1
turn_servo = 0
r = None

def getGrabServo():
    global r
    return r.servos[0][grab_servo]

def getTurnServo():
    global r
    ios = [r.io[0].input[0].d, r.io[0].input[4].d, r.io[0].input[5].d]
    if (1 in ios):
        return ios.index(1)
    else:
        return 10

def setGrabServo(position):
    global r
    if position >= 14 and position <= 82:
        r.servos[0][grab_servo] = position
    else:
        debug("Invalid servo position")
    
def setTurnServo(position):
    global r
    if position >= 15 and position <= 75:
        if position == 75:
            r.servos[0][turn_servo] = 65 
            wait_for(r.io[0].input[0].query.d) 
			
        elif position == 50:
            if r.io[0].input[5].d == 1:
                r.servos[0][turn_servo] = 65
            elif r.io[0].input[0].d == 1:
                r.servos[0][turn_servo] = 8
            wait_for(r.io[0].input[4].query.d)
			
        else:
            r.servos[0][turn_servo] = 8
            wait_for(r.io[0].input[5].query.d)
			
        r.servos[0][turn_servo] = 40
    else:
        debug("Invalid servo position")

def initServoControl(robot):
    global r
    r = robot
    if getTurnServo() != 0:
        setTurnServo(50)
    
def grabTokenLow():
    while True:
        if getTurnServo() != 2:
            setTurnServo(15)
            setGrabServo(13)
        if r.io[0].input[1] == 1:
            setTurnServo(50)
            break
        else:
            setGrabServo(82)

def grabTokenHigh():
    while True:
        setGrabServo(13)
        if r.io[0].input[1] == 1:
            break
        else:
            setGrabServo(82)


def releaseTokenLow():
    setTurnServo(15)
    setGrabServo(82)
    setTurnServo(50)

def releaseTokenHigh():
    if r.io[0].input[1].d == 1:
        setGrabServo(82)
