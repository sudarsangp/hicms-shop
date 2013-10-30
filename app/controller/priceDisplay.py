from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class ListPDU(Command):

	def __init__(self):
		self.storageObject = StorageClass()
		self.feedback = Feedback()

	def execute(self, formData):
		return self.listAllPDU(formData)

	def listAllPDU(self, formData):
		return self.storageObject.getAllPriceDisplay(formData)

class ListPDUById(Command):

	def __init__(self):
		self.storageObject = StorageClass()
		self.feedback = Feedback()

	def execute(self, formData):
		return self.listById(formData)

	def listById(self, formData):
		return self.storageObject.getPriceDisplayById(formData)

class ListPDUByBarcode(Command):

	def __init__(self):
		self.storageObject = StorageClass()
		self.feedback = Feedback()

	def execute(self, formData):
		return self.listByBarcode(formData)

	def listByBarcode(self, formData):
		return self.storageObject.getPriceDisplayByBarcode(formData)

class AddPDU(Command):

	def __init__(self):
		self.storageObject = StorageClass()
		self.feedback = Feedback()

	def execute(self, formData):
		return self.storageObject.addPriceDisplayUnit(formData)
        
        




