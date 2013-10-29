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