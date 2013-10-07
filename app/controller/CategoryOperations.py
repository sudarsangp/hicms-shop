'''
    This file contains classes for operation of Category details like
    add, delete, modify. 
'''

from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

'''
    This class is the command for adding new Category
'''

class AddCategory(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):
        
 
         if self.check_existing_item(formData):
                self.storageObject.addCategoryToDatabase(formData)
                self.feedbackObject.setinfo("Success: data added ")
                self.feedbackObject.setdata(formData.categoryDescription.data)
                self.feedbackObject.setcommandtype("AddCategory")
         
         else:
                 #populate feedback with cannot be added data
                 self.feedbackObject.setinfo("Failed :Duplicate present Data cannot be added")
                 self.feedbackObject.setdata(formData.categoryDescription.data)
                 self.feedbackObject.setcommandtype("AddCategory") 
         
         return self.feedbackObject
    
    def check_existing_item(self, formData):
        return self.storageObject.check_if_category_not_exists(formData.categoryId.data)

class ViewCategories(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):
        return self.get_categories(formData)
    
    def get_categories(self,formData):
        return self.storageObject.get_categories_from_db(formData)     
                    