from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback
from TransactionOperations import ToJson

import requests, json
from ast import literal_eval

class UpdateHQServer(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()
		self.json = ToJson()
	
	def execute(self, formData):
		#url = 'http://127.0.0.1:5000/serverinfo'
		url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/serverinfo'
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
		url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/getstock'
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

class GetPriceFromHQ(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()

	def execute(self, formData):
		#url = 'http://127.0.0.1:5000/getprice'
		url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/getprice'
		#givenbarcode = formData.barcode.data
		#send_bar = {'barcode': givenbarcode}
		#jsend = json.dumps(send_bar)
		r = requests.get(url)
		allbarprice = r.json()
		list_bar_price = allbarprice['barcodeprice']
		for i in range(len(list_bar_price)):
			bar_price_info = literal_eval(json.dumps(list_bar_price[i]))
			in_barcode = bar_price_info['barcode']
			in_newprice = bar_price_info['newprice']
			#print in_barcode, in_newprice
			self.storageObject.set_price_from_hq(in_barcode, in_newprice)

		#json_gotprice = r.json()
		#print r.text()

