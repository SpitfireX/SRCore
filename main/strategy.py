from motor_control import *
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
    distance = distance_m * 100/4.25 # convert meter to ticks
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
