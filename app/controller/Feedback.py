
class Feedback(object):

	def __init__(self):
		pass

	def setinfo(self, info):
		self.info = info

	def getinfo(self):
		return self.info

	def setdata(self, data):
		self.data = data

	def getdata(self):
		return self.data
	
	# This is to indicate if the command executed successfully or not
	def setexecutionstatus(self,data):
		self.status = data
	
	def getexecutionstatus(self):
		return self.status
	
	def setcommandtype(self, commandtype):
		self.commandtype = commandtype

	def getcommandtype(self):
		return self.commandtype