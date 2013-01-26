from motor import Motor
from io import IO
from vision import *

class Robot():
	motors = [Motor() for i in range(2)]
	io = [IO() for i in range(1)]
	servos = []
	
	power = None
	
	def see(self):
		return Vision().see()
