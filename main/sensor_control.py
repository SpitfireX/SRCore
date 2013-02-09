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
        ins = r.io[0].input
        for i in range(0, len(ins)):
            digIn = ins[i].d
            samePins = filter(lambda c: c[0] == i, changes)
            if len(samePins) == 0:
                changes.append((i, digIn))
            elif samePins[0][1] != digIn:
                changes.remove(samePins[0])
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
