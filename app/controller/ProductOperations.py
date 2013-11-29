'''
    This file contains classes for operation of Product details like
    add, delete, modify. 
'''

from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

'''
    This class is the command for adding new Product
'''

class AddProduct(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
         
    def execute(self,formData):
         
         if (self.check_manufacturer_not_exists(formData.manufacturerId.data) == True):
                self.feedbackObject.setinfo("Incomplete: No manufacturer") 
                self.feedbackObject.setdata(formData.proname.data)
                self.feedbackObject.setcommandtype("AddProduct")
                         
         elif self.check_category_not_exists(formData.category.data) == True:
                self.feedbackObject.setinfo("Incomplete: No category") 
                self.feedbackObject.setdata(formData.proname.data)
                self.feedbackObject.setcommandtype("AddProduct")
                
 
         elif self.check_existing_item(formData):
                self.storageObject.addProductToDatabase(formData)
                self.feedbackObject.setinfo("Success: data added ")
                self.feedbackObject.setdata(formData.proname.data)
                self.feedbackObject.setcommandtype("AddProduct")
         
         else:
                 #populate feedback with cannot be added data
                 self.feedbackObject.setinfo("Failed :Duplicate present Data cannot be added")
                 self.feedbackObject.setdata(formData.proname.data)
                 self.feedbackObject.setcommandtype("AddProduct") 
         
         return self.feedbackObject
    
    def check_manufacturer_not_exists(self,newManufacturerId):
        return self.storageObject.check_if_manufacturer_not_exists(newManufacturerId)
    
    def check_category_not_exists(self,newCategoryId):
        return self.storageObject.check_if_category_not_exists(newCategoryId)
    
    def check_existing_item(self, formData):
        return self.storageObject.check_if_Product_exists(formData)               

class ViewProduct(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        return self.get_products(formData)

    def get_products(self, formData):
        return self.storageObject.get_products_from_db(formData)

class SearchProductBarcode(Command):
    def __init__(self):
        self.storageObject = StorageClass()

    def execute(self, formData):
        return self.get_product_for_barcode(formData)

    def get_product_for_barcode(self, formData):
        return self.storageObject.get_product_for_barcode(formData.barcode.data)

class UpdateProduct(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
        
    def execute(self, formData):
        inverted = self.storageObject.check_if_Product_exists(formData)
        actual = not inverted
        if actual:
            self.storageObject.set_product_details(formData)
            self.feedbackObject.setinfo("Success: data updated ")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("Update Product")
        else:
            self.feedbackObject.setinfo("Failed: barcode not found ")
            self.feedbackObject.setdata("Barcode not found")
            self.feedbackObject.setcommandtype("Update Product")
        return self.feedbackObject

class DeleteProduct(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        inverted = self.storageObject.check_if_Product_exists(formData)
        actual = not inverted
        if actual:
            self.storageObject.delete_product_info(formData.barcode.data)
            self.feedbackObject.setinfo("Success: data deleted ")
            self.feedbackObject.setdata(formData.barcode.data)
            self.feedbackObject.setcommandtype("Delete Shop")
        else:
            self.feedbackObject.setinfo("Failed: barcode not found ")
            self.feedbackObject.setdata("barcode not found")
            self.feedbackObject.setcommandtype("Delete Product")
        return self.feedbackObject
    
class AddDisplayProduct(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
        
    def execute(self,formData):
        feedbackObject = self.storageObject.addDisplayStockToDb(formData)
        self.feedbackObject = feedbackObject
        return self.feedbackObject
        
class SetDiscountBarcode(Command):
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()

    def execute(self, formData):
        inverted = self.storageObject.check_if_Product_exists(formData)
        actual = not inverted
        if actual and int(formData.discount.data)>=0 and int(formData.discount.data) <= 50:
            self.feedbackObject = self.storageObject.set_discount_for_barcode(formData.barcode.data, formData.discount.data)
            return self.feedbackObject
        elif actual is False:
            self.feedbackObject.setinfo("Failed: barcode not found ")
            self.feedbackObject.setdata("barcode not found")
            self.feedbackObject.setcommandtype("Set Discount")
            return self.feedbackObject
        else:
            self.feedbackObject.setinfo("Failed: discount not in range 0 to 50%")
            self.feedbackObject.setdata("discount above limit ")
            self.feedbackObject.setcommandtype("Set Discount")
            return self.feedbackObject