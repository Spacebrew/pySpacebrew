import datetime

class TimeProfiler(object):

	def __init__(self, printRoutine):
		self.printRoutine = printRoutine
		self.maps = {}
		self.disabled = False

	def start(self, name):
		if self.disabled:
			return

		self.maps[name] = datetime.datetime.now()

	def disable(self):
		self.disabled = True

	def enable(self):
		self.disabled = False

	def end(self, name):
		if self.disabled:
			return

		now = datetime.datetime.now()
		delta = now - self.maps[name]
		self.printRoutine("{0}\t took {1} seconds to run".format(name, delta.total_seconds()))