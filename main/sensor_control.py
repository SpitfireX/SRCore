from sr_emulator import *
from logger import log
import threading
import math

changes = []

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class MarkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log("Started MarkerThread")

        while True:
            markers = r.see()

            for marker in markers:
                for c in changes:
                    if type(c) == Marker and marker.info.code == c.info.code:
                        changes.remove(c)
                        changes.append(marker)
                        break


class JointIOThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log("Started JointIOThread")

        global r
        global changes
        while True:
            changes.append(r.io[0].input)


def initSensorControl(robot):
    global r
    r = Robot()
    
    global markerThread
    global ioThread
    
    markerThread = MarkerThread()
    ioThread = JointIOThread()

def startThread():
    global markerThread
    global ioThread
    
    markerThread.start()
    ioThread.start()

def getChanges():
    global changes
    ret = changes
    changes = []

    return ret
