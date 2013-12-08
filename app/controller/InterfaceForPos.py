from StorageClass import StorageClass
from Feedback import Feedback
import json, requests

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

    def from_cashier_internshop(self, enteredBarcode, enteredQuantity):
        productData = self.storageObject.get_product_for_barcode(enteredBarcode)
        #print type(productData.currentStock), productData.currentStock
        #print type(enteredQuantity) , enteredQuantity
        if productData.currentStock >= long(enteredQuantity):
            #self.storageFeedback.setcommandtype("Transaction")
            #self.storageFeedback.setinfo("Move quantity from current stock to displayQty")
            #self.storageFeedback.setdata("cannot buy from displayQty")
            shopidsame = 5
            return shopidsame
        else:                    
            #self.storageFeedback.setcommandtype("Ask other shop")
            #self.storageFeedback.setinfo(enteredBarcode)
            #self.storageFeedback.setdata(enteredQuantity)
            shopidreturn = self.get_from_shop(enteredBarcode, enteredQuantity)
            return shopidreturn

    def get_from_shop(self, barcode,quantity):
        urldest = 'http://g10cg3002.ngrok.com/getfromshop'
        bar_quant = {'barcode':barcode,'quantity':quantity}
        send_data = {'barcodequantity':bar_quant}
        print barcode, quantity
        jsend = json.dumps(send_data)
        r = requests.get(urldest,data = jsend)
        responsestatus = r.json()
        shopidvalue = responsestatus['shopid']
        messageforemail = responsestatus['status']
        return shopidvalue