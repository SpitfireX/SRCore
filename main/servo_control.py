from time import sleep
from logger import debug
from sr_emulator import *

grab_servo = 1
turn_servo = 0
has_token = True

def getGrabServo():
    return r.servos[0][grab_servo]

def getTurnServo():
    ios = [r.io[0].input[0], r.io[0].input[4], r.io[0].input[5]]
    return ios.index(1)

def setGrabServo(position):
    if position >= 14 and position <= 85:
        r.servos[0][grab_servo] = position
    else:
        debug("Invalid servo position")

def setTurnServo(position):
    if position >= 14 and position <= 80:
        r.servos[0][turn_servo] = position
    else:
        debug("Invalid servo position")

def initServoControl(robot):
    global r
    r = robot

    setGrabServo(100)
    setTurnServo(15)

def grabTokenLow():
    if getGrabServo() == 82:
        setTurnServo(15)
        setGrabServo(2)
        setTurnServo(75)

        global has_token
        has_token = True

        setTurnServo(50)

        return True
    else:
        return False

def grabTokenHigh():
    if getGrabServo() == 82:
        if getTurnServo() != 0:
            setTurnServo(75)

        setGrabServo(2)

        setTurnServo(50)

        global has_token
        has_token = True

        return True
    else:
        return False

def releaseTokenLow():
    global has_token

    if has_token:
        setTurnServo(15)
        setGrabServo(0)

        has_token = False

        setTurnServo(50)

        return True
    else:
        return False

def releaseTokenHigh():
    global has_token

    if has_token:
        setGrabServo(0)

        has_token = False

        setTurnServo(50)

        return True
    else:
        return False

def interpolateServo(value, setFunction, getFunction, steps=10, time=1):
    svalue = getFunction()

    for step in range(steps):
        setFunction(svalue + step*((value-svalue)/steps))
        sleep(time/steps)

    setFunction(value)
