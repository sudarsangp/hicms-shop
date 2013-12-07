from StorageClass import StorageClass
from Feedback import Feedback


class InterfaceForPos(object):
    '''
     This is a class for interfacing the Pos with shop server.
     
    '''
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
    
    def parseForSoftwareImitater(self,formData):
        input = formData.barcode.data
        result = input.split(',')
        barcodeQtyDict = dict()
        
        x = 0   
        while x < (len(result) - 1) :
             barcodeQtyDict[result[x]] = result[x+1] 
             x = x + 2   
             
            
        return barcodeQtyDict
    
    def parseForPoS(self,inputDataFromPOS):
        input = inputDataFromPOS
        result = input.split(',')
        barcodeQtyDict = dict()
        
        x = 0   
        while x < (len(result) - 1) :
             barcodeQtyDict[result[x]] = result[x+1] 
             x = x + 2   
             
        return barcodeQtyDict
          
    
    def getPriceForBarcode(self,barcode):
        productEntered = self.storageObject.get_product_for_barcode(barcode)
        if productEntered is None:
            print "Product not present"
            
        else:
            return productEntered.displayPrice
    
    def getCashiers(self):
        cashiers_all = self.storageObject.get_cashier_id_from_db()
        return cashiers_all

    def getQuantityForBarcode(self,barcode):
        productEntered = self.storageObject.get_product_for_barcode(barcode)
        if productEntered is None:
            print "Product not present"
            
        else:
            return productEntered.displayQty