'''
    This file contains classes for operation of Manufacturer details like
    add, delete, modify. 
'''

from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

'''
    This class is the command for adding new Manufacturer
'''

class AddManufacturer(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):
         
         if self.check_existing_item(formData):
                self.storageObject.addManufacturerToDatabase(formData)
                self.feedbackObject.setinfo("Success: data added ")
                self.feedbackObject.setdata(formData.mname.data)
                self.feedbackObject.setcommandtype("AddManufacturer")
         
         else:
                 #populate feedback with cannot be added data
                 self.feedbackObject.setinfo("Failed :Duplicate present Data cannot be added")
                 self.feedbackObject.setdata(formData.mname.data)
                 self.feedbackObject.setcommandtype("AddManufacturer") 
         
         return self.feedbackObject
    
    def check_existing_item(self, formData):
        return self.storageObject.check_if_manufacturer_not_exists(formData.manufacturerId.data)
 
class ViewManufacturers(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
    
    def execute(self,formData):
        return self.get_manufacturers(formData)
    
    def get_manufacturers(self,formData):
        return self.storageObject.get_manufacturers_from_db(formData)    
                       