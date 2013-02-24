from sr_emulator import *
import time

def calibrate(r):
	v=[]
	w=[]
        pwr=10
        
	while True:
		markers = r.see()
		addMotorInstruction(r.motors, [pwr, pwr], 1)
		markers2 = r.see()

		if len(markers) != 0 and len(markers2) != 0:
			gefahren = markers[0].dist - markers2[0].dist
			print "roboter faehrt pro Sekunde mit", pwr, "Prozent Motorleistung", gefahren, "Meter"
			v.append(gefahren)

		else:
                        print "Bitte den roboter richtig ausrichten!"
                        wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d == 1)
                        continue

		addMotorInstruction(r.motors, [-pwr, -pwr], 1)

		if pwr == 80:
                        break

                else:
                        pwr+=10

	print "Weitere Kalibrierung startet auf Knopfdruck."
	wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d ==1)

	pwr=10
	while True:
		markers = r.see()
		addMotorInstruction(r.motors, [pwr, -pwr], 1)
		markers2 = r.see()

		if len(markers) != 0 and len(markers2) != 0:
			winkel = markers2[0].rot_y - markers[0].rot_y
			print "Bei", pwr, "Prozent Motorleistung werden", winkel, "Grad zurueckgelegt."
			w.append(winkel)

		else:
			print "Bitte den roboter richtig ausrichten!"
			continue

                if pwr == 80:
                        break

                else:
                        print "Bitte roboter ausrichten!"
                        wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d == 1)
                        pwr+=10

	return v, w

def addMotorInstruction(self, motors, speeds, duration):
	for i in range(len(motors)):
		motors[i].target=speeds[i]
	
	lasttime = time.time()

        if duration > 0:
            log("running for " + str(duration) + " seconds")
            while True:
                now = time.time()
                diff = now - lasttime
                duration -= diff

                if duration <= 0:
                    break

                lasttime = now

if __name__ == '__main__':
	v, w=calibrate()
	print "v:", v, "\nw:", w
