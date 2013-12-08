from StorageClass import StorageClass
from Feedback import Feedback
import json, requests
from flask.ext.mail import Message
from app import mail
from config import ADMINS,RECIPIENTS
from app import app

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
        if str(messageforemail) == "cannot":
            shopidvalue = 0
        return shopidvalue

    def getBundleUnitForBarcode(self,enteredBarcode):
        productEntered = self.storageObject.get_product_for_barcode(enteredBarcode)
        if productEntered is None:
            print "Product not present"
            return -1
        else:
            return productEntered.bundleUnit

    def split_into_dictionary_barcode(self,formData):
        input = formData.barcode.data
        result = input.split(',')
        barcodeQtyDict = dict()
        
        x = 0   
        while x < (len(result) - 1) :
             if(result[x] not in barcodeQtyDict.keys()):
                 barcodeQtyDict[result[x]] = result[x+1]
             else:    
                 barcodeQtyDict[result[x]] = int(barcodeQtyDict[result[x]]) + int(result[x+1])
             x = x + 2
             
        return barcodeQtyDict

    def send_email(self,recipientemail, transactiondetail, totalpriceinfo):
      
      transactionfinal = "<b> Transaction Details </b> </thead>"
      list_recipient = list()
      list_recipient.append(recipientemail)
      transactionfinal += '<table> <thead> <tr> <th> Barcode </th> <th> Quantity </th> <th> Price </th> </tr> </thead> <tbody> '
      for eachbarcodedetail in transactiondetail:
        print eachbarcodedetail
        detailinfo = eachbarcodedetail.split(',')
        transactionfinal += '<tr>' + '<td>' + str(detailinfo[0]) + '</td>' + '<td>' + str(detailinfo[1]) + '</td>' +  '<td>' + str(detailinfo[2]) + '</td> </tr>'
      transactionfinal += '</tbody> </table>'
      msg = Message("Transaction Details", sender = ADMINS[0], recipients = list_recipient)
      msg.body = 'text body'
      msg.html = transactionfinal + '<br>' + '<b>' + str(totalpriceinfo) + '</b>' + '<br>'
      with app.app_context():
        mail.send(msg)
      return "checking"

    def get_check_email(self, feedback, customerid):
      if feedback.getcommandtype() == "transaction success":
          #storageObject = StorageClass()
          #customerid = form.customerId.data
          emailid = self.storageObject.get_email_for_customer(customerid)
          #print "ok" + str(feedback.getdata())
          self.send_email(emailid, feedback.getdata(), feedback.getinfo())

    def check_if_email_exists (self,customerId):
        return self.storageObject.getCustomerId(customerId)