from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

from app.model.models import db,Products, Transaction
from sqlalchemy.sql import func

import datetime
import json

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

class ToJson(object):
    def __init__(self):
        self.storageObject = StorageClass()
        

    def retJSON(self):
        list1 = list()
        list2 = list()

        for row in db.session.query(Products).all():
            temp = row.currentStock + row.displayQty
            data_stock = {'Barcode' : row.barcode , 'ShopId' : '5' , 'Stock' : str(temp)}
            list1.append(data_stock)
        for row1 in db.session.query(Products).all():
            temp1 = db.session.query(func.avg(Products.price)).filter(Products.barcode == row1.barcode).scalar()
            temp2 = db.session.query(func.sum(Transaction.unitSold)).filter(Transaction.barcode == row1.barcode and Transaction.transactionDate == datetime.datetime.now().date()).scalar()
            data_soldstock = {'Barcode' : row1.barcode, 'priceSold' : str(temp1), 'unitSold' : str(temp2), 'ShopId' : '5'}
            list2.append(data_soldstock)

        final_json = {'Stock' : list1, 'SoldStock' : list2}
        return final_json