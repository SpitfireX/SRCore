global r_marker

global x
global y
x = y = None # Position des Roboters.

def computeMarkers(robot, ms):
    r=robot
	markers=ms
	
	global r_marker
	r_marker=[]
	
	global x
	global y

	pedestals = {32:(2000, 6000),
				33:(4000, 6000),
                34:(6000, 6000),
                35:(2000, 4000),
                36:(4000, 4000),
                37:(6000, 4000),
                38:(2000, 2000),
                39:(4000, 2000),
                40:(6000, 2000)}

	m_info = {6:1, 5:2, 4:3, 3:4, 2:5, 1:6, 0:7,
			27:1, 26:2, 25:3, 24:4, 23:5, 22:6, 21:7,
			14:1, 15:2, 16:3, 17:4, 18:5, 19:6, 20:7,
			7:1, 8:2, 9:3, 10:4, 11:5, 12:6, 13:7}

	for m in markers:
		if m.info.marker_type == MARKER_ARENA:
			if 0 <= m.info.code <= 6:
				if m.centre.rot_y != 0: # Falls der Marker nicht genau parallel zum Roboter aufgehaengt ist
										# Der Roboter bildet mit dem Abstand zum Marker und dem Abstand von der Wand ein Dreieck.
										# Da wir den Winkel zum Marker wissen und den Abstand dorthin, kann das mit Sinus ausgerechnet werden.
					ank = math.degrees(sin(m.centre.rot_y)) * m.centre.dist
					y = sqrt(m.centre.dist**2 - ank**2) # x wird mit Pythagoras ausgerechnet
                
				else:
					y = m.centre.dist

				x = m_info(m.info.code) # Abstand der Marker: 1 Meter ->
				x -= ank if m.centre.rot_y < 0 else -ank # Aber: die Marker koennen auch schief aufgehaengt sein (ich gehe hier davon aus, dass
														# bei Verschiebung nach links rot_y negativ ist und bei Verschiebung nach rechts positiv.
														# unbedingt ausprobieren!!!
			elif 14 <= m.info.code <= 20:
				if m.centre.rot_y != 0:
					ank = math.degrees(sin(m.centre.rot_y)) * m.centre.dist
					y = 8 - sqrt(m.centre.dist**2 - ank**2) # hier 8m (Breite der Arena) minus der Abstand von der Wand.
                
				else:
					y = 8 - m.centre.dist

					x = m_info(m.info.code)
					x += ank if m.centre.rot_y < 0 else -ank # hier ist es andersherum!

			elif 7 <= m.info.code <= 13:
				if m.centre.rot_y != 0:
					ank = math.degrees(sin(m.centre.rot_y)) * m.centre.dist
					x = 8 - sqrt(m.centre.dist**2 - ank**2)
                    
				else:
					x = 8 - m.centre.dist

					y = m_info(m.info.code)
					y += ank if m.centre.rot_y < 0  else -ank

			else:
				if m.centre.rot_y != 0:
					ank = math.degrees(sin(m.centre.rot_y)) * m.centre.dist
					x = sqrt(m.centre.dist**2 - ank**2)
                
				else:
					x = m.centre.dist

					y = m_info(m.info.code)
					y += ank if m.centre.rot_y < 0 else -ank

			motor_control.changePoints.append(motor_control.getCurrentAngle(), [x, y])
               
		elif m.info.marker_type == MARKER_ROBOT:
			global r_marker
			if len(r_marker) == 0:
				r_marker=[m.info.code, m.dist]
                    
			else:
				if m.info.code == r_marker[0]:
					distsOld = r_markers[1]
					distsNew = m.dist
                            
					change = distsNew-distsOld
                            
					if change > 0:
						global r_marker
						r_marker=[]
						continue
                    
					else:
						pointdist=math.degrees(tan(m.rot_y)*m.dist)
						if pointdist <= 50:
							speeds, duration=motor_control.getCurrentInstruction()
							skipCurrentInstruction()
							angle = -m.rot_y - 10 if m.rot_y > 0 else -m.rot_y +10 
							addAngleInstruction(angle)
							addMotorInstruction(r.motors, speeds, duration)

		elif m.info.marker_type == MARKER_PEDESTAL:
			currentAngle=motor_control.getCurrentAngle()           
	
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
			y += allticks  -changePoints[len(changePoints)-1][2]
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
			xpart = cos(currentAngle) * currentTicks
			ypart = sin(currentAngle) * currentTicks
				
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
