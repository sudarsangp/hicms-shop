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
		url = 'http://127.0.0.1:5000/serverinfo'
		#url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/serverinfo'
		testvalue = self.json.retJSON()
		jdata = json.dumps(testvalue)
		requests.post(url,data=jdata)
		#r = requests.post(url,data=jdata)
		self.feedbackObject.setinfo("Success: data sent to server")
		self.feedbackObject.setdata("sent data") #r.json()
		self.feedbackObject.setcommandtype("UpdateHQServer")
		return self.feedbackObject

class GetStockFromHQ(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()

	def parsebarcodequantity(self,formData):
		inputs = formData.barcode.data
		result = inputs.split(',')
		barcodeQtyDict = dict()
		x = 0
		while x <(len(result) - 1):
			barcodeQtyDict[result[x]] = result[x+1]
			x = x+2
		return barcodeQtyDict

	def execute(self, formData):
		url = 'http://127.0.0.1:5000/getstock'
		#url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/getstock'
		dict_bar_quantity = self.parsebarcodequantity(formData)
		#givenbarcode = formData.barcode.data
		#givenquantity = formData.quantity.data
		#inverted = self.storageObject.check_if_Product_exists(formData)
        #if inverted:
        #	pass
    	#self.feedbackObject.setinfo("Failure: barcode not present")
    	#self.feedbackObject.setdata("Barcode not present")
    	#self.feedbackObject.setcommandtype("GetStockFromHQ")
    	#return self.feedbackObject
        #else:
		print dict_bar_quantity, type(dict_bar_quantity)
		send_list = []
		for key, value in dict_bar_quantity.items():
			send_bar_quantity = {'barcode':key,'quantity':value}
			send_list.append(send_bar_quantity)
		send_data = {'getstock':send_list}
		jsend = json.dumps(send_data)
		r = requests.get(url,data = jsend)
		json_gotquantity = r.json()
		for bar_quantity in json_gotquantity['getstockdata']:

			barcode_got = bar_quantity['barcode']
			quantity_to_add = long(bar_quantity['quantity'])
			if quantity_to_add >= 0:
				self.storageObject.add_current_stock(barcode_got, quantity_to_add)
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
		url = 'http://127.0.0.1:5000/getprice'
		#url = 'http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/getprice'
		#givenbarcode = formData.barcode.data
		#send_bar = {'barcode': givenbarcode}
		#jsend = json.dumps(send_bar)
		r = requests.get(url)
		allbarprice = r.json()
		self.feedbackObject.setinfo("Failed: barcode not found ")
		self.feedbackObject.setdata("new price")
		self.feedbackObject.setcommandtype("GetStockFromHQ")
		list_bar_price = allbarprice['barcodeprice']
		print list_bar_price
		print len(list_bar_price)
		for i in range(len(list_bar_price)):
			bar_price_info = literal_eval(json.dumps(list_bar_price[i]))
			in_barcode = bar_price_info['barcode']
			in_newprice = bar_price_info['newprice']
			#print in_barcode, in_newprice
			actual = self.storageObject.data_check_product(in_barcode)
        	#actual = not inverted
        	#print actual
        	if actual:
				self.storageObject.set_price_from_hq(in_barcode, in_newprice)
				print in_newprice, in_barcode
				self.feedbackObject.setinfo("Success: price got")
				self.feedbackObject.setdata("new price")
				self.feedbackObject.setcommandtype("GetStockFromHQ")
				#print "insdie actual"
			#else:

			#	self.feedbackObject.setinfo("Failed: barcode not found ")
			#	self.feedbackObject.setdata("new priec")
			#	self.feedbackObject.setcommandtype("GetStockFromHQ")

		return self.feedbackObject
		#json_gotprice = r.json()
		#print r.text()

