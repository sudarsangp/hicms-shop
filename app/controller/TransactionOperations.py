from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

class CreateTransaction(Command):
    
    def __init__(self):
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
        self.barcodeQuantityDict = dict()
        self.lastTransactionNumber = 0 

        
    def execute(self,formData):
        
        customerId = formData.customerId.data        
        transactionDate = formData.transactionDate.data         
        cashierId = formData.cashierId.data
        self.barcodeQuantityDict = formData.barcode.data
       
        lastTransactionNumber = self.storageObject.getLastTransactionNo()
        transactionId = long(lastTransactionNumber) + 1
     
        feedbackObject = self.storageObject.buyProducts(self.barcodeQuantityDict,transactionId,customerId,cashierId,transactionDate)
      
        self.feedbackObject = feedbackObject
        
        return self.feedbackObject
    
class ListTransactions(Command):
    
    def __init__(self):    
        self.storageObject = StorageClass()
        self.feedbackObject = Feedback()
    
    def execute(self,formData):
        allTransactions = self.storageObject.getTransactions()
        return allTransactions     