import random, time, collections

random.seed()

class Vision():
	def see(self):
		
		Marker=collections.namedtuple("MarkerBasis", "info dist rot_y");
		MarkerInfo=collections.namedtuple("MarkerInfo", "code marker_type");	
		i=random.randint(0, 5)
		dist=random.randint(0, 8)
		
		if i == 0:
			return []
		
		else:
			global inf
			if i == 1:
				inf = MarkerInfo(random.randint(0, 27), 0)
		
			elif i == 2:
				inf = MarkerInfo(random.randint(28, 31), 1)
		
			elif i == 3:
				inf = MarkerInfo(random.randint(32, 40), 2)
		
			elif i == 4:
				inf = MarkerInfo(random.randint(41, 64), 3)
				
			marker = Marker(inf, dist, random.randint(-180, 180))
			return [marker]
	
		time.sleep(0.5)
