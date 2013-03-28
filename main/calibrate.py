from sr_emulator import *
import time, math
from logger import debug

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
                if pwr>0:
                        addMotorInstruction(r.motors, [0, pwr], 1)

                else:
                        addMotorInstruction(r.motors, [pwr, 0], 1)
		markers2 = r.see()

		if len(markers) != 0 and len(markers2) != 0:
			dist1=markers[0].dist
                        dist2=markers2[0].dist
                        winkel=math.degrees(math.cos(dist1/dist2))
                        print "Bei", pwr, "Prozent Motorleistung werden", winkel, "Grad zurueckgelegt."
			w.append(winkel)

		else:
			print "Bitte den roboter richtig ausrichten!"
                        wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d == 1)
                        continue

                if pwr == 80:
                        break

                else:
                        print "Bitte roboter ausrichten!"
                        wait_for(r.io[0].input[0].query.d == 1, r.io[0].input[1].query.d == 1)
                        pwr+=10

	return v, w

def addMotorInstruction(motors, speeds, duration):
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

        for i in range(len(motors)):
        	motors[i].target=0

if __name__ == '__main__':
	v, w=calibrate()
	print "v:", v, "\nw:", w
