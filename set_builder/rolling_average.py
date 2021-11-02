"""
	File: rolling_average.py

	This file will contain a class which will make calculating a rolling
	average easier.
"""

from collections import deque

class Rolling_Average:

	def __init__(self, max, quiescent = None):
		self.max = max
		
		self.d = deque()
		
		if(quiescent == None):
			self.running_total = 0
			return

		self.running_total = max*quiescent
		for i in range(max):
			self.d.append(quiescent)

	def add(self, val):
		if len(self.d) == self.max:
			to_remove = self.d.popleft()
			self.running_total -= to_remove
		self.d.append(val)
		self.running_total += val

	def get_average(self):
		return float(self.running_total/len(self.d))

		