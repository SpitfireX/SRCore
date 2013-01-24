from sr import *
import time

def calibrate():
  v=()
	for pwr in range(10, 80, 10):
		t1 = time.time()
		duration=1
		markers = R.see()
		while duration > 0:
			duration -= time.time() - t1
		
		markers2 = R.see()
		
		gefahren = markers[0].dist - markers2[0].dist
		print "Roboter fährt pro Sekunde mit", pwr, "Prozent Motorleistung", gefahren, "Meter"
		v.append(gefahren)
	
	return v
	
if __name__=='__main__':
	calibrate()
	
