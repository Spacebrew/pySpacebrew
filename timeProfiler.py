import datetime

class TimeProfiler(object):

	def __init__(self, printRoutine):
		self.printRoutine = printRoutine
		self.maps = {}

	def start(self, name):
		self.maps[name] = datetime.datetime.now()

	def end(self, name):
		now = datetime.datetime.now()
		delta = self.maps[name] - now
		self.printRoutine("{0}\t took {1} ms to run".format(name, delta.microseconds/1000))