from math import *
from sr_emulator import MARKER_ARENA
from strategy import *
import motor_control

global changes
global markers
global ios
global r_marker
x = y = 0 # Position des Roboters.


pedestals = {32:(2, 6),
             33:(4, 6),
             34:(6, 6),
             35:(2, 4),
             36:(4, 4),
             37:(6, 4),
             38:(2, 2),
             39:(4, 2),
             40:(6, 2)}

m_info = {6:(0,1,0), 5:(0,2,0), 4:(0,3,0), 3:(0,4,0), 2:(0,5,0), 1:(0,6,0), 0:(0,7,0),
          7:(1,0,-90), 8:(2,0,-90), 9:(3,0,-90), 10:(4,0,-90), 11:(5,0,-90), 12:(6,0,-90), 13:(7,0,-90),
          14:(8,1,180), 15:(8,2,180), 16:(8,3,180), 17:(8,4,180), 18:(8,5,180), 19:(8,6,180), 20:(8,7,180),
          27:(1,8,90), 26:(2,8,90), 25:(3,8,90), 24:(4,8,90), 23:(5,8,90), 22:(6,8,90), 21:(7,8,90)}

def getCoordinates():
    global x
    global y
    return [x, y]

def computeAbsolutePositionByArenaMarker(marker):
    if marker.info.marker_type != MARKER_ARENA: raise Exception("Wrong marker type.")
    (xm,ym,phim) = m_info[marker.info.code]
    x, y, motor_control.currentAngle = xm, ym, phim
    alpha = radians(marker.orientation.rot_y - marker.rot_y - phim)
    return ( xm + marker.dist * cos(alpha),
             ym + marker.dist * sin(alpha),
             (phim - marker.orientation.rot_y) % 360 - 180 )

def computeCoordinates(allticks, changePoints=[], currentAngle=0):
    print changePoints
    global x
    global y
    if len(changePoints)==0:
        return []

    elif len(changePoints)==1:
        return [x, y]

    else:
        if currentAngle == 0:
            y += allticks - changePoints[len(changePoints)-1][2]
            return [x, y]

        elif currentAngle == 180:
            y -= allticks - changePoints[len(changePoints) - 1][2]
            return [x, y]

        elif currentAngle == 90:
            x -= allticks - changePoints[len(changePoints) - 1][2]
            return [x, y]

        elif currentAngle == 270:
            x += allticks - changePoints[len(changePoints) - 1][2]
            return [x, y]

        else:
            currentTicks = allticks - changePoints[len(changePoints) - 1][2]
            xpart = cos(radians(currentAngle)) * currentTicks * 80 # in mm
            ypart = sin(radians(currentAngle)) * currentTicks * 80    # " "

            if currentAngle > 0 and currentAngle < 90:
                xpart *= -1
            elif currentAngle > 90 and currentAngle < 180:
                xpart *= -1
                ypart *= -1
            elif currentAngle > 180 and currentAngle < 270:
                ypart *= -1

            x = changePoints[1][0] + xpart
            y = changePoints[1][1] + ypart
            return [x, y]
