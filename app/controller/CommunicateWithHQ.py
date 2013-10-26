from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

import requests, json

class UpdateHQServer(Command):
	def __init__(self):
		self.storageObject = StorageClass()
		self.feedbackObject = Feedback()
	
	def execute(self, formData):
		url = 'http://127.0.0.1:5000/serverinfo'
		stock_json = {'barcode': '2', 'shopId':'5', 'stockQty':'4'}
		soldstock_json = {'barcode': '2', 'pricesold': '3.2', 'unitsold':'32', 'shopId':'5', 'timestamp':'11.11.13 22:00'}
		final_json = {'stock':stock_json,'soldstock':soldstock_json}
		stock_soldstock = json.dumps(final_json)
		r = requests.post(url,data=stock_soldstock)
		self.feedbackObject.setinfo("Success: data sent to server")
		self.feedbackObject.setdata(r.json())
		self.feedbackObject.setcommandtype("UpdateHQServer")
		return self.feedbackObject