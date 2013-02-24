from sr_emulator import *
import motor_control

def calibrate(r):
	v=[]
	w=[]

	for pwr in range(10, 80, 10):
		markers = r.see()
		motor_control.addMotorInstruction(r.motors, [pwr, pwr], 1)
		markers2 = r.see()

		if len(markers) != 0 and len(markers2) != 0:
			gefahren = markers[0].dist - markers2[0].dist
			print "roboter faehrt pro Sekunde mit", pwr, "Prozent Motorleistung", gefahren, "Meter"
			v.append(gefahren)

		else:
			print "Bitte den roboter richtig ausrichten!"
			break

		motor_control.addMotorInstruction(r.motors, [-pwr, -pwr], 1)

	print "Weitere Kalibrierung startet auf Knopfdruck."
	wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d ==1)

	for pwr in range(10, 80, 10):
		markers = r.see()
		motor_control.addMotorInstruction(r.motors, [pwr, -pwr], 1)
		markers2 = r.see()

		if len(markers) != 0 and len(markers2) != 0:
			winkel = markers2[0].rot_y - markers[0].rot_y
			print "Bei", pwr, "Prozent Motorleistung werden", winkel, "Grad zurueckgelegt."
			w.append(winkel)

		else:
			print "Bitte den roboter richtig ausrichten!"
			break

		print "Bitte roboter ausrichten!"
		wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d == 1)

	return v, w

if __name__ == '__main__':
	v, w=calibrate()
	print "v:", v, "\nw:", w
