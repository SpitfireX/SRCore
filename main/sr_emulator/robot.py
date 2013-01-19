from motor import Motor
from io import IO

class Robot():
	motors = [Motor() for i in range(2)]
	io = [IO() for i in range(1)]
	servos = []
	
	power = None
	vision = None
