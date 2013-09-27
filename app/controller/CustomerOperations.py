'''
Created on Sep 12, 2013

@author: dinesh
'''
'''
    This file contains classes for operation of customer details like
    add, delete, modify. 
'''

from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback
'''
    This class is the command for adding new customer
'''

class AddCustomer(Command):
    
    def __init__(self):
    	self.storageObject = StorageClass()
    	self.feedbackObject = Feedback()
 		
    def execute(self,formData):

    	if self.__check_database(formData):
    		try:
    			self.storageObject.addCustomerTODatabase(formData)
    			self.feedbackObject.setinfo("Success: data added ")
    			self.feedbackObject.setdata(formData.emailid.data)
    			self.feedbackObject.setcommandtype("AddCustomer")
    		except Exception as e:
    			#populate feedback with exception data
    			self.feedbackObject.setinfo("Failed :Exception  Data cannot be added" + e)
    			self.feedbackObject.setdata(formData.emailid.data)
    			self.feedbackObject.setcommandtype("AddCustomer")
    	else:
    		#populate feedback with cannot be added data
    		self.feedbackObject.setinfo("Failed :Duplicate present Data cannot be added")
    		self.feedbackObject.setdata(formData.emailid.data)
    		self.feedbackObject.setcommandtype("AddCustomer")
    	
    	return self.feedbackObject
        
    def __check_database(self, formData):
    	return self.storageObject.query_database(formData)