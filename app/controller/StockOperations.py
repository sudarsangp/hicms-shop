
from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class AddStock(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):

        if self.check_existing_item(formData):
            self.storageObject.addStockToDatabase(formData)
            self.feedbackObject.setinfo("Success: data added ")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("AddStock")
     
        else:
            #populate feedback with cannot be added data
            self.feedbackObject.setinfo("Failed :Duplicate present Data cannot be added")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("AddStock") 
     
        return self.feedbackObject

    def check_existing_item(self, formData):
        return self.storageObject.check_if_stock_exists(formData) 