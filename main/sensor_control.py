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

        global r
        global changes

        pedestals = {32:Coordinate(2000, 6000),
                     33:Coordinate(4000, 6000),
                     34:Coordinate(6000, 6000),
                     35:Coordinate(2000, 4000),
                     36:Coordinate(4000, 4000),
                     37:Coordinate(6000, 4000),
                     38:Coordinate(2000, 2000),
                     39:Coordinate(4000, 2000),
                     40:Coordinate(6000, 2000)}

        m_info = {6:1, 5:2, 4:3, 3:4, 2:5, 1:6, 0:7,
                  27:1, 26:2, 25:3, 24:4, 23:5, 22:6, 21:7,
                  14:1, 15:2, 16:3, 17:4, 18:5, 19:6, 20:7,
                  7:1, 8:2, 9:3, 10:4, 11:5, 12:6, 13:7}

        x = y = None # Position des Roboters.

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
    r = robot

    markerThread = MarkerThread()
    ioThread = JointIOThread()

def getChanges():
    global changes
    ret = changes
    changes = []

    return ret
