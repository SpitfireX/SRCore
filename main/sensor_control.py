from sr_emulator import *
from logger import debug
import threading
import time
from computeChanges import *

changes = []


class MarkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        debug("Started MarkerThread")

        while True:
            global r
            markers = r.see()
            # computeMarkers(r, markers)
            changes.extend(markers)


# class JointIOThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def run(self):
#         debug("Started JointIOThread")

#         global r
#         global changes
#         localChanges = []
#         initial = r.io[0].input
#         for i in range(len(initial)):
#             event = Event(time.time(), "Pin", (i, initial[i].d))
#             localChanges.append(event)
#             changes.append(event)
#         while True:
#             ins = r.io[0].input
#             for i in range(0, len(ins)):
#                 digIn = ins[i].d
#                 event = Event(time.time(), "Pin", (i, digIn))
#                 oldIn = filter(lambda e: e.eventValue[0] == i, localChanges)[0]
#                 if digIn != oldIn:
#                     localChanges.remove(oldIn)
#                     localChanges.append(event)
#                     changes.append(event)


class Event():
    def __init__(self, timestamp, eventType, eventValue):
        self.timestamp = timestamp
        self.eventType = eventType
        self.eventValue = eventValue


def initSensorControl(robot):
    global r
    r = robot

    global markerThread
    # global ioThread

    markerThread = MarkerThread()
    # ioThread = JointIOThread()

def startThread():
    global markerThread
    # global ioThread

    markerThread.start()
    # ioThread.start()

def getChanges():
    global changes
    ret = changes
    changes = []

    return ret
