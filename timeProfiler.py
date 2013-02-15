import datetime

class TimeProfiler(object):

	def __init__(self, printRoutine):
		self.printRoutine = printRoutine
		self.maps = {}

	def start(self, name):
		self.maps[name] = datetime.datetime.now()

	def end(self, name):
		now = datetime.datetime.now()
		delta = now - self.maps[name]
		self.printRoutine("{0}\t took {1} seconds to run".format(name, delta.total_seconds()))