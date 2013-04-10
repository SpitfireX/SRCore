from time import sleep
from logger import debug

grab_servo = 1
turn_servo = 0
has_token = True

def getGrabServo():
    return r.servos[0][grab_servo]

def getTurnServo():
    return r.servos[0][turn_servo]

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
    if getGrabServo() == 0:
    	setTurnServo(15)
        setGrabServo(100)
        setTurnServo(85)
        
        global has_token
        has_token = True
        
        return True
    else:
        return False

def grabTokenHigh():
    if getGrabServo() == 0:
        if getTurnServo() < 85:
            setTurnServo(85)
        
        setGrabServo(100)
        
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
        
        return True
    else:
        return False

def releaseTokenHigh():
    global has_token
    
    if has_token:
        setGrabServo(0)
        
        has_token = False
        
        return True
    else:
        return False

def interpolateServo(value, setFunction, getFunction, steps=10, time=1):
    svalue = getFunction()
    
    for step in range(steps):
        setFunction(svalue + step*((value-svalue)/steps))
        sleep(time/steps)
        
    setFunction(value)
