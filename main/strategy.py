from motor_control import *
from vector_math import *
from math import *
# from computeChanges import *

class Strategy():
    def __init__(self, robot):
        self.hasToken = False
        self.targetToken = None
        self.r = robot
        self.ownPedestals=[]
        self.availablePedstals=[]
        self.stolenPedestals=[]

    def act(self, markers):
        # self.position = position
        self.markers = markers

        # for m in markers:
        #     for m2 in markers:
        #         if -160 <= (m.centre.world.x - m2.centre.world.x) <= 160:
        #             pedestal = m if m.info.marker_type == MARKER_PEDESTAL else m2
        #             if isMarkerIn(pedestal, self.availablePedestals):
        #                 self.availablePedestals.remove(pedestal)
        #             if isMarkerIn(pedestal, self.ownPedestals):
        #                 self.ownPedestals.remove(pedestal)
        #                 self.stolenPedestals.append(pedestal)

        if self.hasToken:
            delivered = self.deliverToken()
            if delivered:
                self.hasToken = False
        else:
            token = self.getToken()
            if token:
                self.hasToken = True

    def getToken(self):
        if self.targetToken:
            token = filter(lambda t: t.info.code == self.targetToken.info.code, self.markers)
            if len(token) > 0:
                arrived = driveTo(token[0])
                if arrived:
                    grabToken()
                    return True
        else:
            # TODO: s/home/point in front of tokens
            arrived = True #driveTo(home)
            if arrived:
                debug("Searching for tokens")
                tokens = filter(isToken, self.markers)
                if len(tokens) == 0:
                    debug("No tokens found")
                    addAngleInstruction(20)
                else:
                    self.targetToken = min(tokens, key=lambda t: t.centre.polar.length)
                    driveTo(self.targetToken)
            return False



    def deliverToken(self):
        pedestal = findEmptyPedestal()

        if pedestal == None:
            search()
        else:
            coor = pedestals(pedestal.info.code)
            coor[1] -= 420
            addPositionInstruction(coor)
            addAngleInstruction(0 - currentAngle)
            addMotorInstruction([70, 70], 2)
            ownPedestals.append(pedestal)
            if isMarkerIn(pedestal, availablePedestals):
                availablePedestals.remove(pedestal)

def enclosedAngle(v, w):
    "only normalized vectors allowed"
    return degrees(acos(sProd(v,w)))*cmp(v[2]*w[0] - v[0]*w[2],0.)

def approachMarker(marker, d):
    # Approach a given marker to distance d on its normal
    coords = marker.centre.world
    debug("Coords: ({0},{1},{2})".format(coords.x,coords.y,coords.z))
    rot_y = radians(marker.orientation.rot_y)
    debug("rot_y: " + str(rot_y))
    n = (-sin(rot_y), 0, -cos(rot_y))
    v = vAdd((coords.x, coords.y, coords.z), sMult(d, n))
    lenv = vLen(v)
    vn = sMult(1./lenv, v)

    alpha = enclosedAngle((0,0,1.), vn)
    beta = enclosedAngle(vn,sMult(-1.,n))

    debug("Alpha: {0},beta:{1}, len:{2}".format(alpha,beta,lenv))

    addAngleInstruction(alpha)
    addMotorInstruction(ticks = toTicks(lenv))

    addAngleInstruction(beta)

# def approachMarkerTest(x, y, z, rot_y, d):
#     # Approach a given marker to distance d on its normal
#     rot_y = radians(rot_y)
#     n = (-sin(rot_y), 0, -cos(rot_y))
#     v = vAdd((x, 0, z), sMult(d, n))
#     lenv = vLen(v)
#     vn = sMult(1./lenv, v)

#     alpha = enclosedAngle((0,0,1.), vn)
#     beta = enclosedAngle(vn,sMult(-1.,n))

#     print("Alpha: {0},beta:{1}, len:{2}".format(alpha,beta,lenv))

def isMarkerIn(m, list):
    for l in list:
        if l.info.code == m.info.code:
            return True
    return False

def findEmptyPedestal():
    markers = getMarkers()
    pedestals = filter(isPedestal, markers)
    while len(pedestals) != 0 and len(markers) != 0:
        m = markers.pop()
        for p in pedestals:
            if p.world.x == m.world.x and p.world.y == m.world.y:
                pedestals.remove(p)
                break
    if len(pedestals) == 0:
        return None
    else:
        return min(pedestals, key=lambda p: p.centre.polar.length)

def driveTo(dest):
    distance_m = dest.centre.polar.length
    debug("Driving for " + str(distance_m))
    distance = toTicks(distance_m) # convert meter to ticks
    if distance < 1:
        return True
    else:
        skipCurrentInstruction()
        angle = dest.centre.polar.rot_y
        if angle > 1:
            addAngleInstruction(angle)
        addMotorInstruction([80,80], round(distance))
        return False

def isToken(m):
    return True

def toTicks(n):
    return n * 100/4.24
