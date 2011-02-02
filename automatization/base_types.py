#from decimal import self

# base types of automatization

class point:
	x = 0
	y = 0
	
	def __init__(self, x = 0, y = 0 ):
		self.x = x
		self.y = y
		
	def __str__(self):
		return "automatization.point : %d, %d." % (self.x, self.y)