from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback
from TransactionOperations import ToJson

import requests, json
url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/serverinfo'
class UpdateHQServer(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()
		self.json = ToJson()
	
	def execute(self, formData):
		#url = 'http://127.0.0.1:5000/serverinfo'
		testvalue = self.json.retJSON()
		jdata = json.dumps(testvalue)
		r = requests.post(url,data=jdata)
		self.feedbackObject.setinfo("Success: data sent to server")
		self.feedbackObject.setdata(r.json())
		self.feedbackObject.setcommandtype("UpdateHQServer")
		return self.feedbackObject

class GetStockFromHQ(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()

	def execute(self, formData):
		#url = 'http://127.0.0.1:5000/getstock'
		givenbarcode = formData.barcode.data
		givenquantity = formData.quantity.data
		#inverted = self.storageObject.check_if_Product_exists(formData)
        #if inverted:
        #	pass
    	#self.feedbackObject.setinfo("Failure: barcode not present")
    	#self.feedbackObject.setdata("Barcode not present")
    	#self.feedbackObject.setcommandtype("GetStockFromHQ")
    	#return self.feedbackObject
        #else:
		send_bar_quantity = {'barcode':givenbarcode,'quantity':givenquantity}
		jsend = json.dumps(send_bar_quantity)
		r = requests.get(url,data = jsend)
		json_gotquantity = r.json()
		#gotquantity = json.loads(json_gotquantity)
		quantity_to_add = long(json_gotquantity['quantity'])
		if quantity_to_add >= 0:
			self.storageObject.add_current_stock(givenbarcode, quantity_to_add)
			self.feedbackObject.setinfo("Success: quantity got")
			self.feedbackObject.setdata(r.json())
			self.feedbackObject.setcommandtype("GetStockFromHQ")
			#return self.feedbackObject
		else:
			self.feedbackObject.setinfo("Failure: cannot add quantity")
			self.feedbackObject.setdata(r.json())
			self.feedbackObject.setcommandtype("GetStockFromHQ")
		return self.feedbackObject