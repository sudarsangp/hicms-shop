from Command import Command
from StorageClass import StorageClass
from Feedback import Feedback

from app.model.models import db,Products, Transaction
from sqlalchemy.sql import func

from ast import literal_eval

import datetime, os
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

        #for row in db.session.query(Products).all():
          #  temp = row.currentStock + row.displayQty
            #data_stock = {'Barcode' : row.barcode , 'ShopId' : '5' , 'Stock' : str(temp)}
            #list1.append(data_stock)
        fname = 'stockdata.txt'
        list_content = []
        try:
            with open(fname):
                f = open(fname,"r")
                contentdata = f.read()
                list_content = contentdata.split(';')
                del list_content[0]
                #print type(list_content)
                for eachbarcode in list_content:
                    #print type(eachbarcode)
                    newtypebarcode = literal_eval(eachbarcode)
                    #print type(newtypebarcode), newtypebarcode
                    eachvalueforbarcode = newtypebarcode['barcode']
                    eachvalue = Products.query.filter_by(barcode = eachvalueforbarcode).first()
                    total = eachvalue.currentStock + eachvalue.displayQty
                    data_stock = {'barcode' : eachvalueforbarcode , 'stock' : str(total)}
                    list1.append(data_stock)
                open(fname, 'w').close()
        except IOError:
          no_file = {'update':'No file'}  
        
        # comment this to avoid sending stock that have not changed used for setup purpose only
        #for row in Products.query.all():
        #    temp = row.currentStock + row.displayQty
        #    data_stock = {'Barcode' : row.barcode , 'Stock' : str(temp)}
        #    list1.append(data_stock)
        
        #    if int(row.barcode) == 2:
        #        print data_stock
       # for row1 in db.session.query(Products).all():
         #   temp1 = db.session.query(func.avg(Transaction.soldPrice)).filter(Transaction.barcode == row1.barcode and Transaction.transactionDate == datetime.datetime.now().date()).scalar()
         #   temp2 = db.session.query(func.sum(Transaction.unitSold)).filter(Transaction.barcode == row1.barcode and Transaction.transactionDate == datetime.datetime.now().date()).scalar()
         #   data_soldstock = {'Barcode' : row1.barcode, 'priceSold' : str(temp1), 'unitSold' : str(temp2), 'ShopId' : '5'}
         #   list2.append(data_soldstock)
        #total = 0
        for row1 in Products.query.all():
            temp1 = 0
            temp2 = 0
            for data1 in Transaction.query.filter_by(barcode = row1.barcode).filter_by(transactionDate = datetime.datetime.now().date()):
                temp1 = temp1 + data1.soldPrice
                #print data.soldPrice
                #print data1.transactionDate
                #print "now"
                #print datetime.datetime.now().date()
            count = Transaction.query.filter_by(barcode = row1.barcode).filter_by(transactionDate = datetime.datetime.now().date()).count()
            #total+= count
            if count != 0:
                temp1 = temp1/count
            for data2 in Transaction.query.filter_by(barcode = row1.barcode).filter_by(transactionDate = datetime.datetime.now().date()):
                temp2 = temp2 + data2.unitSold
            data_soldstock = {'barcode' : row1.barcode, 'priceSold' : str(temp1), 'unitSold' : str(temp2)}
            if(temp2 != 0):
                list2.append(data_soldstock)

        #print total
        #print len(list1), len(list2)
        final_json = {'Stock' : list1, 'SoldStock' : list2}
        send_shopid_json = {'1':final_json}
        print send_shopid_json
        return send_shopid_json