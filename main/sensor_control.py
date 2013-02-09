from sr_emulator import *
from logger import log
import threading
import math

changes = []

class MarkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log("Started MarkerThread")

        while True:
            global r
            markers = r.see()
            changes.extend(markers)



class JointIOThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log("Started JointIOThread")


        global r
        global changes
        localChanges = []
        for i in r.io[0].input:
            localChanges.append(i.d)
            changes.append(i.d)
        while True:
            ins = r.io[0].input
            for i in range(0, len(ins)):
                digIn = ins[i].d
                oldIn = filter(lambda c: c[0] == i, localChanges)[0]
                if digIn != oldIn:
                    localChanges.remove((i, oldIn))
                    localChanges.append((i, digIn))
                    changes.append((i, digIn))


def initSensorControl(robot):
    global r
    r = robot

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
