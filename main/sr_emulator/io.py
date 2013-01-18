import random
	
class Input():
	def __init__(self):
		self.a = random.random()*3.3
		self.d =  1 if self.a > 1.65 else 0
		
class Output():
	d = 0
	
class IO():
	input = [Input() for i in range(8)]
	output = [Output() for i in range(8)]