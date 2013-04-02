grab_servo = 0
turn_servo = 1
has_token = False

def getGrabServo():
    return r.servos[0][grab_servo]

def getTurnServo():
    return r.servos[0][turn_servo]

def setGrabServo(position):
    r.servos[0][grab_servo] = position
    
def setTurnServo(position):
    r.servos[0][turn_servo] = position

def initServoControl(robot):
    global r
    r = robot
    
    setGrabServo(0.0)
    setTurnServo(0.0)
    
def grabTokenLow():
    if getGrabServo() == 0 and getTurnServo() == 0:
        setGrabServo(100)
        setTurnServo(100)
        
        global has_token
        has_token = True
        
        return True
    else:
        return False

def grabTokenHigh():
    if getGrabServo() == 0 and getTurnServo() == 0:
        if getTurnServo() < 100:
            setTurnServo(100)
        
        setGrabServo(100)
        
        global has_token
        has_token = True
        
        return True
    else:
        return False

def releaseTokenLow():
    if has_token:
        setTurnServo(0)
        setGrabServo(0)
        
        global has_token
        has_token = False
        
        return True
    else:
        return False

def releaseTokenHigh():
    if has_token:
        setGrabServo(0)
        
        global has_token
        has_token = False
        
        return True
    else:
        return False