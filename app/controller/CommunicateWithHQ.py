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
		testvalue = {'TableName':'Value','Fields': 'values'}
		jdata = json.dumps(testvalue)
		r = requests.post(url,data=jdata)
		self.feedbackObject.setinfo("Success: data sent to server")
		self.feedbackObject.setdata(r.json())
		self.feedbackObject.setcommandtype("UpdateHQServer")
		return self.feedbackObject