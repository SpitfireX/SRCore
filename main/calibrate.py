from sr import *
import time

def calibrate():
  v=[]
	for pwr in range(10, 80, 10):
		t1 = time.time()
		duration=1
		markers = R.see()
		if len(markers)!=0:
			R.motors[0].target = pwr
			R.motors[1].target = pwr
			while duration > 0:
				duration -= time.time() - t1
			
			R.motors[0].target = 0
			R.motors[1].target = 0
			markers2 = R.see()
		
			gefahren = markers[0].dist - markers2[0].dist
			print "Roboter fährt pro Sekunde mit", pwr, "Prozent Motorleistung", gefahren, "Meter"
			v.append(gefahren)
	
			return v
		else:
			print "Bitte den Roboter richtig ausrichten!"
			break
	
if __name__=='__main__':
	calibrate()
	
