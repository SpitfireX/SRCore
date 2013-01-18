from sr_emulator import *
import threading
from robot import r

changes = []


class SensorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tokens = []
        self.inputs = []
    
    def run(self):
        print "Started SensorThread"
        
        while True:
            checkStuff()

def checkStuff():
    newToks = r.see()
    
    for token in newToks:
        for c in changes:
            if type(c) == Marker and token.info.code == c.info.code:
                changes.remove(c)
                changes.append(token)
                break
    
    #sensorIns = r.io[0].input

def getChanges():
    ret = changes
    changes = []
    
    return ret