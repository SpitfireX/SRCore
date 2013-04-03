from math import *

global changes
global markers
global ios
global r_marker
x = y = None # Position des Roboters.


pedestals = {32:(2000, 6000),
			33:(4000, 6000),
			34:(6000, 6000),
			35:(2000, 4000),
			36:(4000, 4000),
			37:(6000, 4000),
			38:(2000, 2000),
			39:(4000, 2000),
			40:(6000, 2000)}

m_info = {6:1000, 5:2000, 4:3000, 3:4000, 2:5000, 1:6000, 0:7000,
		27:1000, 26:2000, 25:3000, 24:4000, 23:5000, 22:6000, 21:7000,
		14:1000, 15:2000, 16:3000, 17:4000, 18:5000, 19:6000, 20:7000,
		7:1000, 8:2000, 9:3000, 10:4000, 11:5000, 12:6000, 13:7000}
		
def getCoordinates():
	global x
	global y
	return [x, y]

def computeMarkers(robot, ms, activeToken=None, side=None):
	r=robot
	markers=ms
	
	global r_marker
	r_marker=[]
	
	global x
	global y
	global m_info
	global pedestals

	for m in markers:
		if m.info.marker_type == MARKER_ARENA:
			if 0 <= m.info.code <= 6:
				if m.centre.orientation.rot_y != 0: # Falls der Marker nicht genau parallel zum Roboter aufgehaengt ist
										# Der Roboter bildet mit dem Abstand zum Marker und dem Abstand von der Wand ein Dreieck.
										# Da wir den Winkel zum Marker wissen und den Abstand dorthin, kann das mit Sinus ausgerechnet werden.
					ank = degrees(sin(radians(m.centre.orientation.rot_y))) * m.centre.dist * 1000
					y = sqrt((m.centre.dist*1000)**2 - ank**2) # y wird mit Pythagoras ausgerechnet, in mm
                
				else:
					y = m.centre.dist*1000

				x = m_info(m.info.code) # Abstand der Marker: 1 Meter ->
				x -= ank if m.centre.orientation.rot_y < 0 else -ank # Aber: die Marker koennen auch schief aufgehaengt sein (ich gehe hier davon aus, dass
														# bei Verschiebung nach links orientation.rot_y negativ ist und bei Verschiebung nach rechts positiv.
														# unbedingt ausprobieren!!!
			elif 14 <= m.info.code <= 20:
				if m.centre.orientation.rot_y != 0:
					ank = degrees(sin(radians(m.centre.orientation.rot_y))) * m.centre.dist * 1000
					y = 8000 - sqrt((m.centre.dist*1000)**2 - ank**2) # hier 8m (Breite der Arena) minus der Abstand von der Wand.
                
				else:
					y = 8 - m.centre.dist*1000

					x = m_info(m.info.code)
					x += ank if m.centre.orientation.rot_y < 0 else -ank # hier ist es andersherum!

			elif 7 <= m.info.code <= 13:
				if m.centre.orientation.rot_y != 0:
					ank = degrees(sin(radians(m.centre.orientation.rot_y))) * m.centre.dist * 1000
					x = 8000 - sqrt((m.centre.dist*1000)**2 - ank**2)
                    
				else:
					x = 8000 - m.centre.dist * 1000

					y = m_info(m.info.code)
					y += ank if m.centre.orientation.rot_y < 0  else -ank

			else:
				if m.centre.orientation.rot_y != 0:
					ank = degrees(sin(radians(m.centre.orientation.rot_y))) * m.centre.dist * 1000
					x = sqrt((m.centre.dist*1000)**2 - ank**2)
                
				else:
					x = m.centre.dist*1000

					y = m_info(m.info.code)
					y += ank if m.centre.orientation.rot_y < 0 else -ank

			motor_control.changePoints.append(motor_control.getCurrentAngle(), [x, y])
               
		elif m.info.marker_type == MARKER_ROBOT:
			global r_marker
			if len(r_marker) == 0:
				r_marker=[m.info.code, m.dist * 1000]
                    
			else:
				if m.info.code == r_marker[0]:
					distsOld = r_markers[1]
					distsNew = m.dist * 1000
                            
					change = distsNew-distsOld
                            
					if change > 0:
						global r_marker
						r_marker=[]
						continue
                    
					else:
						pointdist=math.degrees(tan(radians(m.orientation.rot_y))*m.dist*1000)
						if pointdist <= 450:
							speeds, duration=motor_control.getCurrentInstruction()
							skipCurrentInstruction()
							angle = -m.orientation.rot_y - 10 if m.orientation.rot_y > 0 else -m.orientation.rot_y +10 
							addAngleInstruction(angle)
							addMotorInstruction(r.motors, speeds, duration)

		elif m.info.marker_type == MARKER_PEDESTAL:
			if activeToken != None:
				currentAngle = motor_control.getCurrentAngle()
				coor = pedestals(activeToken)
				xped = coor[0]
				yped = coor[1]
				if side == "down":
					y -= m.dist * 1000 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * m.dist * 1000
					x -= 0 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * (x - xped) * 1000
			
				elif side == "up":
					y += m.dist * 1000 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * m.dist * 1000
					x -= 0 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * (x - xped) * 1000
			
				elif side == "right":
					x += m.dist * 1000 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * m.dist * 1000
					y -= 0 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * (y - yped) * 1000
			
				else:
					x -= m.dist * 1000 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * m.dist * 1000
					y -= 0 if currentAngle == 0 else cos(radians(m.orientation.rot_y)) * (y - yped) * 1000
				
				#addTokenInstruction(currentToken, xped, yped, x, y)
			
			else:
				for m2 in marker:
					diff = m2.dist * 1000 - m.dist * 1000
					#if diff <= 10 or diff <= -10:
						#onPedestals.append(m2)
						#break
		
				
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
			xpart = cos(math.radians(currentAngle)) * currentTicks * 80 # in mm
			ypart = sin(math.radians(currentAngle)) * currentTicks * 80	# " "
				
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
