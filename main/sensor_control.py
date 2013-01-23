from sr_emulator import *
import threading, math
from robot import r

changes = []

class Coordinate():
    def __init__(self, x, y):
        self.x=x
        self.y=y

class SensorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tokens = []
        self.inputs = []

    def run(self):
        print "Started SensorThread"
        key = 32
        pedestals = {}
        for c in [Coordinate(x, y) for y in ns for x in reversed(ns)]:
            pedestals[key] = c
            key += 1

        m_info={6:1, 5:2, 4:3, 3:4, 2:5, 1:6, 0:7,
                27:1, 26:2, 25:3, 24:4, 23:5, 22:6, 21:7,
                14:1, 15:2, 16:3, 17:4, 18:5, 19:6, 20:7,
                7:1, 8:2, 9:3, 10:4, 11:5, 12:6, 13:7}

        x=y=None #Position des Roboters.

        while True:
            tokens=r.see()
            for m in markers:
                if m.info.marker_type==MARKER_ARENA:
                    if 0 <= m.info.code <= 6:
                        if m.centre.rot_y != 0: #(Falls der Marker nicht genau parallel zum Roboter aufgehängt ist)
                            ank=math.degrees(sin(m.centre.rot_y))*m.centre.dist #Der Roboter bildet mit dem Abstand zum Marker und dem Abstand von der Wand ein Dreieck. Da wir den Winkel zum Marker wissen und den Abstand dorthin, kann das mit Sinus ausgerechnet werden.
                            y=sqrt(m.centre.dist**2-ank**2) #x wird mit Pythagoras ausgerechnet
                        else:
                            y=m.centre.dist

                        x=m_info(m.info.code) #Abstand der Marker: 1 Meter ->
                        x-=ank if m.centre.rot_y<0 else -ank #Aber: die Marker können auch schief aufgehängt sein (ich gehe hier davon aus, dass
                                                                #bei Verschiebung nach links rot_y negativ ist und bei Verschiebung nach rechts positiv.
                                                                #unbedingt ausprobieren!!!
                    elif 14 <= m.info.code <= 20:
                        if m.centre.rot_y != 0:
                            ank = math.degrees(sin(m.centre.rot_y))*m.centre.dist
                            y = 8-sqrt(m.centre.dist**2-ank**2) #hier 8 m(Breite der Arena) minus der Abstand von der Wand.
                        else:
                            y=8-m.centre.dist

                        x=m_info(m.info.code)
                        x+=ank if m.centre.rot_y < 0 else -ank #hier ist es andersherum!

                    elif 7 <= m.info.code <= 13:
                        if m.centre.rot_y != 0:
                            ank=math.degrees(sin(m.centre.rot_y))*m.centre.dist
                            x=8-sqrt(m.centre.dist**2-ank**2)
                        else:
                            x=8-m.centre.dist

                        y=m_info(m.info.code)
                        y+=ank if m.centre.rot_y<0  else -ank

                    else:
                        if m.centre.rot_y!=0:
                            ank=math.degrees(sin(m.centre.rot_y))*m.centre.dist
                            x=sqrt(m.centre.dist**2-ank**2)
                        else:
                            x=m.centre.dist

                        y=m_info(m.info.code)
                        y+=ank if m.centre.rot_y<0 else -ank


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
