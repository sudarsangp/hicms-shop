from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class BuyItem(Command):

	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()

	def execute(self, formData):
		inverse = self.storageObject.check_if_Product_exists(formData)
		actual = not inverse
		""" if comparison operator does not work check the type of operator form data is of type unicode """
		if actual:
			quantity = self.storageObject.get_stock_quantity_for_barcode(formData.barcode.data)
			form_quantity = long(formData.quantity.data)
			
			if form_quantity <= quantity:
				quantity = quantity - form_quantity
				self.storageObject.set_stock_quantity_for_barcode(formData.barcode.data, quantity)

				self.feedbackObject.setinfo("Success :quantity has been bought")
				self.feedbackObject.setdata(formData.barcode.data)
    			self.feedbackObject.setcommandtype("BuyItem")
		
		return self.feedbackObject
			#else:
			#	self.feedbackObject.setinfo("Failed :Entered quantity more than batch quantity")
			#	print "falied case"
		#else:
		#	self.feedbackObject.setinfo("Failed :Barcode not found")
    	#	self.feedbackObject.setdata(formData.barcode.data)
    	#	self.feedbackObject.setcommandtype("BuyItem")
    	#	print "prod does not exist"
		

