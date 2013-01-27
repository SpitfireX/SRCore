from sr import *
import motor_control
import time

def calibrate():
  v=[]
  R=Robot()
	for pwr in range(10, 80, 10):
		t1 = time.time()
		markers = R.see()
		motor_control.addMotorInstruction(R.motors, [pwr, pwr], 1)
		t2 = time.time()
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
	
