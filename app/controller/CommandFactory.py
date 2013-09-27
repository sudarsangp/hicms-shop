'''
Created on Sep 10, 2013

@author: dinesh
'''

'''
     This class determines the correct type of command and
     returns the correct type to the caller.
     
'''
from CustomerOperations import AddCustomer
from ManufacturerOperations import AddManufacturer
from CategoryOperations import AddCategory
class CommandFactory(object):
    
    def createCommand(self,operation,formData):
        if operation == "addcustomer":
            addCustomerCommand = AddCustomer()
            return addCustomerCommand
        
        elif operation == "addmanufacturer":
            addManufacturerCommand = AddManufacturer()
            return addManufacturerCommand
        
        elif operation == "addcategory":
            addCategoryCommand = AddCategory()
            return addCategoryCommand