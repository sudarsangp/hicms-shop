
'''
    This class will retrieve data from the database which inturn is represented
     by the SQL-alchemy classes.
     
'''

from app.model.models import db, Customer,Manufacturers,Category,Products,Transaction, PriceDisplay
from Feedback import Feedback
from flask import session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

fname = 'stockdata.txt'

class StorageClass(object):
    
    def __init__(self):
        self.storageFeedback = Feedback()
    
    def addCustomerTODatabase(self,formData):
        newCustomerData = Customer(formData.customername.data,formData.customeraddress.data,
                                   formData.handphone.data,formData.customerId.data,formData.dateofjoining.data,
                                   formData.passwordcustomer.data)
    
        db.session.add(newCustomerData)
        try:
        	db.session.commit()
        except IntegrityError as err:
        	#log data
        	# this part need to check whether exception works
        	db.session.flush()
        	raise e


    def query_database(self, formData):
    	idQuery = Customer.query.filter_by(customerId = formData.customerId.data).first()
    	if idQuery:
    		# email already present in database
    		return False
    	else:
    		return True
 
    def addManufacturerToDatabase(self,formData):
      #  newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.name.data, formData.isContractValid.data) 
        newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.mname.data, True) 
        
        db.session.add(newManufacturerData) 
        db.session.commit()

    
    def check_if_manufacturer_not_exists(self,newManufacturerId):
        manufacturer_id = Manufacturers.query.filter_by( manufacturerId = newManufacturerId).first()
        
        if manufacturer_id:
            return False
        else:
            return True
    
    def addCategoryToDatabase(self,formData):
        newManufacturerData = Category(formData.categoryId.data, formData.categoryDescription.data,formData.isExpirable.data)
        
        db.session.add(newManufacturerData) 
        db.session.commit()    

    def check_if_category_not_exists(self,newCategoryId):
        category_id = Category.query.filter_by( categoryId = newCategoryId).first()
        
        if category_id:
            return False
        else:
            return True
    
    def addProductToDatabase(self,formData):
        newProductData = Products(formData.barcode.data,formData.proname.data,formData.manufacturerId.data,formData.category.data,formData.price.data,
                                  formData.minStock.data,formData.currentStock.data,formData.bundleUnit.data,formData.displayPrice.data,formData.displayQty.data)

        
        db.session.add(newProductData) 
        try:
            db.session.commit() 
        except IntegrityError as err:
                self.storageFeedback.setinfo("Transaction Failed due to improper data") 
                print self.storageFeedback.info
    
    def check_if_Product_exists(self,formData):
        product_id = Products.query.filter_by( barcode = formData.barcode.data).first()
        
        if product_id:
            return False
        else:
            return True    
    
    def get_manufacturers_from_db(self,formData):
        existingManufacturers = Manufacturers.query.all()
        return existingManufacturers    
    
    def get_categories_from_db(self,formData):
        existingCategories = Category.query.all()
        return existingCategories    

    def get_products_from_db(self, formData):
        existingProduct = Products.query.all()
        return existingProduct

    def get_stock_quantity_for_barcode(self, enteredBarcode):
#         stockData = Stock.query.filter_by(barcode = enteredBarcode).first()
        productData = Products.query.filter_by(barcode = enteredBarcode).first()    
        return productData.currentStock
        
    def set_stock_quantity_for_barcode(self, enteredBarcode, quantity):
#         stockData = Stock.query.filter_by(barcode = enteredBarcode).first()
#         stockData.batchQty = quantity
        productData = Products.query.filter_by(barcode = enteredBarcode).first()
        productData.currentStock = quantity
        db.session.commit()
    
    def buyProducts(self,barcodeQuantityDict,transactionId,customerId,cashierId,transactionDate):
        productsBought = list()
        totalPrice = 0
                
        for enteredBarcode in barcodeQuantityDict.iterkeys():
            productData = Products.query.filter_by(barcode = enteredBarcode).first()
            if(productData is None):
                self.storageFeedback.setinfo(" Barcode " + enteredBarcode + " is not present")
                self.storageFeedback.setexecutionstatus(False)
                self.storageFeedback.setcommandtype("No barcode")
                return self.storageFeedback
                
            soldPrice = productData.displayPrice
            purchaseQty = long(barcodeQuantityDict[enteredBarcode])
            
            if(purchaseQty > productData.displayQty):
                self.storageFeedback.setinfo("Quantity in shelf less than quantity requested" + productData.name + "Transaction Did not occur ")
                self.storageFeedback.setexecutionstatus(False)
                if productData.currentStock >= purchaseQty:
                    self.storageFeedback.setcommandtype("Transaction")
                    self.storageFeedback.setinfo("Move quantity from current stock to displayQty")
                    self.storageFeedback.setdata("cannot buy from displayQty")
                    return self.storageFeedback
                else:                    
                    self.storageFeedback.setcommandtype("Ask other shop")
                    self.storageFeedback.setinfo(enteredBarcode)
                    self.storageFeedback.setdata(purchaseQty)
                    return self.storageFeedback
            
            productData.displayQty = productData.displayQty - purchaseQty  
            newTransaction = Transaction(transactionId,customerId,cashierId,transactionDate, enteredBarcode, barcodeQuantityDict[enteredBarcode], soldPrice)
            db.session.add(newTransaction)
            #db.session.commit()
            self.storageFeedback.setcommandtype("Buy product")

            f = open(fname,'a')
            barcodedict = {}
            barcodedict['barcode'] = unicode(enteredBarcode)
            f.write(';')
            f.write(str(barcodedict))
            f.close() 
            # These are for output
            newProductBoughtPrice = int(barcodeQuantityDict[enteredBarcode])*soldPrice
            productsBought.append(str(enteredBarcode)+ ',' + str(barcodeQuantityDict[enteredBarcode]) + ',' + str(newProductBoughtPrice  ) )
                        
            totalPrice = totalPrice + newProductBoughtPrice
            
            #print productsBought
        try:             
            db.session.commit()
            self.storageFeedback.setinfo("Transaction Successfully Completed with total price = " + str(totalPrice))
            self.storageFeedback.setdata(productsBought)
            self.storageFeedback.setcommandtype("transaction success")
            print totalPrice
            self.storageFeedback.setexecutionstatus(True)
        except IntegrityError as err:
                self.storageFeedback.setinfo("Transaction Failed due to improper data")
                print err
        return self.storageFeedback    
    
    def get_display_price(self,barcode):
        productDisplayPrice = self.get_product_for_barcode(barcode).first().displayPrice
        return productDisplayPrice    
            
    def get_product_for_barcode(self,enteredBarcode):
        existingProduct = Products.query.filter_by(barcode = enteredBarcode).first()
        return existingProduct

    def set_product_details(self, formData):

        updateproduct = Products.query.filter_by(barcode = formData.barcode.data).first()
        updateproduct.price = formData.price.data
        updateproduct.minStock = formData.minStock.data
        updateproduct.bundleUnit = formData.bundleUnit.data
        db.session.commit()
    
    def getLastTransactionNo(self):
        lastTransaction = Transaction.query.order_by(db.cast(Transaction.transactionId,db.BigInteger).desc())
        
#         y = 0
#         for x in lastTransaction:
#             print lastTransaction[y].transactionId
#             y = y + 1
            
        if lastTransaction.first() is None:
            return 0
        
        return lastTransaction.first().transactionId
    
    def getTransactions(self):
        transactions = Transaction.query.all()
        return transactions

    def getPriceDisplayById(self, givenID):
        priceDisplay = PriceDisplay.query.filter( PriceDisplay.priceDisplayId == givenID.Id.data)
        return priceDisplay

    def getPriceDisplayByBarcode(self, givenBarcode):
        priceDisplay = PriceDisplay.query.filter(givenBarcode == PriceDisplay.barcode)
        return priceDisplay

    def getAllPriceDisplay(self, formData):
        priceDisplay = PriceDisplay.query.all()
        return priceDisplay


    def delete_product_info(self, enteredBarcode):
        producttodelete = Products.query.filter_by(barcode = enteredBarcode).first()
        db.session.delete(producttodelete)
        db.session.commit()
    
    def addDisplayStockToDb(self,formData):
        productToIncreaseDisplay = Products.query.filter_by(barcode = formData.barcode.data).first()
        
        if productToIncreaseDisplay is None:
            self.storageFeedback.setinfo("Sorry the barcode does not exist")
            self.storageFeedback.setexecutionstatus(False)
        
        elif(int(productToIncreaseDisplay.currentStock) > int(formData.quantity.data)):

            productToIncreaseDisplay.currentStock = productToIncreaseDisplay.currentStock- int(formData.quantity.data)
            productToIncreaseDisplay.displayQty =  productToIncreaseDisplay.displayQty + int(formData.quantity.data)
            productToIncreaseDisplay.displayPrice = productToIncreaseDisplay.price 
            db.session.add(productToIncreaseDisplay)
            db.session.commit()

            self.storageFeedback.setexecutionstatus(True)
            self.storageFeedback.setinfo("Successfully increased Display Stock levels")
        
        else:
            self.storageFeedback.setinfo("Sorry the current Stock level is less than requested Quantity")
            self.storageFeedback.setexecutionstatus(False)
                 
        return self.storageFeedback   
         

    def add_current_stock(self, givenbarcode, quantity_to_add):
        existingprod = Products.query.filter_by(barcode = givenbarcode).first()
        #print existingprod.currentStock, quantity_to_add
        existingprod.currentStock += quantity_to_add
        #print existingprod.currentStock
        db.session.commit()

    def set_price_from_hq(self, enteredbarcode, newprice):

        existingprod = Products.query.filter_by(barcode = enteredbarcode).first()
        existingprod.price = newprice
        db.session.commit()
        
    def addPriceDisplayUnit(self,formData):
        product = Products.query.filter_by(barcode = formData.barcode.data).first()
        if product is None:
           self.storageFeedback.setinfo("Sorry Product does not exist with barcode " + barcode)     
        
        else:
           newPriceDisplay = PriceDisplay(formData.displayId.data,formData.barcode.data)
           db.session.add(newPriceDisplay)
           db.session.commit()
           self.storageFeedback.setinfo("PDU successfully added")  
           
           return self.storageFeedback

    def data_check_product(self, enteredbarcode):
        product_id = Products.query.filter_by( barcode = enteredbarcode).first()
        if product_id:
            return True
        else:
            return False

    def get_email_for_customer(self, inputid):
        customerdetail = Customer.query.filter_by(customerId = inputid).first()
        return customerdetail.email

    def set_discount_for_barcode(self, enteredBarcode, discount):
        existingProduct = Products.query.filter_by(barcode = enteredBarcode).first()
        pricevalue = float(existingProduct.price)
        #print type(existingProduct.price)
        pricevalue -= (float(discount)* 0.01 *pricevalue)
        pricevalue = 0.05*round(pricevalue/0.05)
        pricevalue = int(pricevalue*100)/100.0
        existingProduct.price = pricevalue
        db.session.commit()

        newfile = "pricechange.txt"
        f = open(newfile,'a')
        pricedisplayunit = PriceDisplay.query.filter_by(barcode = enteredBarcode).first()
        data_written = {}
        final_data = {}
        data_written['barcode'] = enteredBarcode
        data_written['pricedisplayid'] = pricedisplayunit.priceDisplayId
        data_written['price'] = pricevalue
        data_written['name'] = existingProduct.name
        final_data['pricedetail'] = data_written
        f.write(';')
        f.write(str(final_data))
        f.close()
        
        self.storageFeedback.setinfo("Success Discount set")
        self.storageFeedback.setdata(pricevalue)
        self.storageFeedback.setcommandtype("Set discount")
        return self.storageFeedback
        #return existingProduct