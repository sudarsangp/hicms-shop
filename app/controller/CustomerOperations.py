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
'''
    This class is the command for adding new customer
'''

class AddCustomer(Command):
    
    def execute(self,formData):
        storageObject = StorageClass()
        storageObject.addCustomerTODatabase(formData)
        