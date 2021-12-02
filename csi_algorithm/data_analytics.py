"""
FileName: data_analytics.py

This file will be used for testing different aspects of the analytics algorithm
"""

import math

NUM_BINS = 6
NUM_COLUMNS = 106

class DataSet:
	def __init__(self, file: str):
		self.set = dict()
		self.mean = dict()
		self.variance = dict()

		with open(file, "r") as f:
			header = f.readline()
			
			for line in f.readlines():
				line_lst = line.split(",")

				if not self.set.get(line_lst[0], ""):
					self.set[line_lst[0]] = [list() for _ in range(NUM_COLUMNS)] 

				if not self.mean.get(line_lst[0], ""):
					self.mean[line_lst[0]] = [0 for _ in range(NUM_COLUMNS)]

				if not self.variance.get(line_lst[0], ""):
					self.variance[line_lst[0]] = [0 for _ in range(NUM_COLUMNS)]

				for column in range(len(line_lst)-1):
					try:
						self.set[line_lst[0]][column].append(float(line_lst[column+1]))
						self.mean[line_lst[0]][column] += float(line_lst[column+1])

					except Exception as e:
						self.set[line_lst[0]][column].append(0)
		
		for bin in self.mean.keys():
			for column in range(len(self.mean[bin])):
				self.mean[bin][column] = float(self.mean[bin][column] / len(self.set["0"][0]))

		for bin in self.set.keys():
			for column in range(len(self.set[bin])):
				for point in self.set[bin][column]:
					self.variance[bin][column] += (self.mean[bin][column] - point)**2
				self.variance[bin][column] /= (len(self.set[bin][column]) - 1)


class PointRange:
	def __init__(self, mean, variance):
		self.mean = mean
		self.variance = variance
		self.upper_bound = mean + math.sqrt(variance)
		self.lower_bound = mean - math.sqrt(variance)

	def detect_overlap(self, pr: 'PointRange'):
		print(f"[{self.lower_bound}, {self.upper_bound}] [{pr.lower_bound}, {pr.upper_bound}]")
		return (
			(self.upper_bound <= pr.upper_bound and self.upper_bound >= pr.lower_bound) or
			(self.lower_bound <= pr.upper_bound and self.lower_bound >= pr.lower_bound) or
			(self.upper_bound >= pr.upper_bound and self.lower_bound <= pr.lower_bound) or
			(self.upper_bound <= pr.upper_bound and self.lower_bound >= pr.lower_bound)
		)


prefix = "C:\\Users\\Owner\\Github\\Magic-Sensors-Reimagined\\csi_algorithm"

if __name__ == '__main__':
	dataset = DataSet(f"{prefix}\\dataset.csv")

	point_list = list()

	print(f"Overlap T1: {PointRange(5, 25).detect_overlap(PointRange(15, 25))}")
	print(f"Overlap T2: {PointRange(5, 36).detect_overlap(PointRange(15, 36))}")
	print(f"Overlap T3: {PointRange(5, 20).detect_overlap(PointRange(15, 20))}")
	print(f"Overlap T4: {PointRange(5, 25).detect_overlap(PointRange(5, 16))}")
	print(f"Overlap T5: {PointRange(5, 4).detect_overlap(PointRange(5, 25))}")
	print(f"Overlap T6: {PointRange(5, 25).detect_overlap(PointRange(15, 25))}")
	print(f"Overlap T7: {PointRange(15, 25).detect_overlap(PointRange(5, 36))}")
	print(f"Overlap T8: {PointRange(15, 16).detect_overlap(PointRange(5, 16))}")
	
	for column in range(NUM_COLUMNS):
		point_list.append([])
		for bin in dataset.mean.keys():

			point_list[column].append(
				PointRange(dataset.mean[bin][column], 
				dataset.variance[bin][column])
			)


	print(point_list)