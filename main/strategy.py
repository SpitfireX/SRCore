from motor_control import *
from vector_math import *
from math import *
from servo_control import *
# from computeChanges import *

class Objective():
    def __init__(self):
        self.preObjective = None

    def setPreObjective(self, obj):
        self.preObjective = obj

    def reach(self, markers):
        return ((self.preObjective and not self.preObjective.reach(markers))
               or self.doReach(markers))

    def doReach(self, markers):
        raise Exception("doReach not implemented")

class DeadEndException(Exception):
    pass

def allowedAngles(l, r, marker, lpl=0, rpl=0, i=0):
    if len(marker) == 0 or len(marker) == i:
        return (l,lpl,r,rpl)

    m = marker.pop()

    polarL = m.centre.polar.length
    ml = m.centre.polar.rot_y + 0.8/polarL
    mr = m.centre.polar.rot_y - 0.8/polarL

    if l > ml and r < mr:
        return allowedAngles(l, r, marker, lpl, rpl, i)
    elif (l < ml and l < mr) or (r > mr and r > ml):
        return allowedAngles(l, r, [m] + marker, lpl, rpl, i+1)
    else:
        return allowedAngles(l if l>ml else ml,
                             r if r<mr else mr,
                             marker
                             lpl if l>ml else polarL,
                             rpl if r<mr else polarL)

class DestinationObjective(Objective):
    def __init__(self, destination, noRecursion = False):
        Objective.__init__(self)
        self.destination = destination
        self.noRecursion = noRecursion

    def doReach(self, markers):
        orientation = getCurrentAngle()
        (x,y) = getCoordinates()
        (xd,yd) = (self.destination[0] - x, self.destination[1] - y)
        distance = vLen((xd,yd))
        if distance < 0.1:
            debug("Destination reached: " + str(self.destination))
            return True
        destAngle = - atan2(xd, yd)
        alpha = degrees(destAngle) - orientation

        (l, lPolarL, r, rPolarL) = allowedAngles(alpha, alpha, ( m for m in markers if m.centre.polar.length < distance ))
        if self.noRecursion and (l != alpha or r != alpha):
            raise DeadEndException()
        (preDestAngle, preDestDistance) = (l, lPolarL) if abs(destAngle - l) < abs(destAngle - r) else (r, rPolarR)
        absolutePreDestAngle = orientation + preDestAngle
        preDest = vAdd((x,y), sMult(preDestDistance+0.3, (cos(radians(absolutePreDestAngle)), sin(radians(absolutePreDestAngle)))))
        preObj = DestinationObjective(preDest, noRecursion = True)
        self.setPreObjective(preObj)
        try:
            self.reach(markers)
        except DeadEndException:
            debug("Caught DeadEndException")
            self.setPreObjective(None)
            self.reach(markers)
        return False

        addImmediateAngleInstruction(alpha)
        addMotorInstruction(toTicks(vLen))
        return False

home = None

class Strategy():
    def __init__(self, robot):
        self.hasToken = False
        self.targetToken = None
        self.r = robot
        self.ownPedestals=[]
        self.availablePedstals=[]
        self.stolenPedestals=[]
        self.deliveredTokens=0

    def act(self, markers):
        # self.position = position
        self.markers = markers

        for m in markers:
            for m2 in markers:
                if -160 <= (m.centre.world.x - m2.centre.world.x) <= 160:
                    pedestal = m if m.info.marker_type == MARKER_PEDESTAL else m2
                    if isMarkerIn(pedestal, self.availablePedestals):
                        self.availablePedestals.remove(pedestal)
                    if isMarkerIn(pedestal, self.ownPedestals):
                        self.ownPedestals.remove(pedestal)
                        self.stolenPedestals.append(pedestal)

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
            approachMarker(pedestal, 0.015)
            retVal = releaseTokenHigh()
            if retVal == True:
                if isMarkerIn(pedestal, availablePedestals):
                    ownPedestals.append(pedestal)
                    availablePedestals.remove(pedestal)
                deliveredTokens += 1
                return True

            return False

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

    addImmediateAngleInstruction(alpha)
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
