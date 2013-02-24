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
            for m in markers:
                changes.append(Event(time.time(), "Marker", m))


class JointIOThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log("Started JointIOThread")


        global r
        global changes
        localChanges = []
        initial = r.io[0].input
        for i in len(initial):
            event = Event(time.time(), "Pin", (i, initial[i].d))
            localChanges.append(event)
            changes.append(event)
        while True:
            ins = r.io[0].input
            for i in range(0, len(ins)):
                event = Event(time.time(), "Pin", (i, ins[i].d))
                oldIn = filter(lambda e: e.value[0] == i, localChanges)[0]
                if digIn != oldIn:
                    localChanges.remove(oldIn)
                    localChanges.append(event)
                    changes.append(event)


class Event():
    def __init__(self, timestamp, eventType, eventValue):
        self.timestamp = timestamp
        self.eventType = eventType
        self.eventValue = eventValue


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
