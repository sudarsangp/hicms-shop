'''
Created on Sep 10, 2013

@author: dinesh
'''

'''
     This class determines the correct type of command and
     returns the correct type to the caller.
     
'''
from CustomerOperations import AddCustomer
from ManufacturerOperations import AddManufacturer,ViewManufacturers
from CategoryOperations import AddCategory,ViewCategories
from ProductOperations import AddProduct, ViewProduct, SearchProductBarcode, UpdateProduct, DeleteProduct,AddDisplayProduct
from UserOperations import BuyItem
from TransactionOperations import CreateTransaction,ListTransactions
from CommunicateWithHQ import UpdateHQServer, GetStockFromHQ
from PriceDisplay import ListPDUById


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
        
        elif operation == "addproduct":
            addProductCommand = AddProduct()
            return addProductCommand
        
        elif operation == "viewmanufacturers":
            viewManufacturersCommand = ViewManufacturers()
            return viewManufacturersCommand
        
        elif operation == "viewcategories":
            viewCategoriesCommand = ViewCategories()
            return viewCategoriesCommand

        elif operation == "viewproducts":
            viewProductCommand = ViewProduct()
            return viewProductCommand

        elif operation == "buyitem":
            buyItemCommand = BuyItem()
            return buyItemCommand
        
        elif operation == "searchBarcode":
            searchBarcodeCommand = SearchProductBarcode()
            return searchBarcodeCommand
     
        elif operation == "hwImitateBuy":
            makeTransaction = CreateTransaction()
            return makeTransaction
        
        elif operation == "submittransaction":
            updateHQServerCommand = UpdateHQServer()
            return updateHQServerCommand

        elif operation == "updateproduct":
            updateProductCommand = UpdateProduct()
            return updateProductCommand
        
        elif operation == "viewproducttransactions":
            viewTransactions = ListTransactions()
            return viewTransactions

        elif operation == "viewpdubyid":
            viewPduById = ListPDUById()
            return viewPduById

        elif operation == "deleteproduct":
            deleteProductCommand = DeleteProduct()
            return deleteProductCommand
        
        elif operation == "adddisplaystock":
            addDisplayProductCommand = AddDisplayProduct()
            return addDisplayProductCommand

        elif operation == "requeststock":
            getStockCommand = GetStockFromHQ()
            return getStockCommand
