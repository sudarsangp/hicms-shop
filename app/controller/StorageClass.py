
'''
    This class will retrieve data from the database which inturn is represented
     by the SQL-alchemy classes.
     
'''
from app.model.models import db, Customer,Manufacturers,Category
from flask import session

class StorageClass(object):
    
    def addCustomerTODatabase(self,formData):
        newCustomerData = Customer(formData.customername.data,formData.customeraddress.data,
                                   formData.handphone.data,formData.emailid.data,formData.dateofjoining.data,
                                   formData.passwordcustomer.data)
    
        db.session.add(newCustomerData)
        try:
        	db.session.commit()
        except Exception as e:
        	#log data
        	# this part need to check whether exception works
        	db.session.flush()
        	raise e


    def query_database(self, formData):
    	emailquery = Customer.query.filter_by(email = formData.emailid.data).first()
    	if emailquery:
    		# email already present in database
    		return False
    	else:
    		return True
 
    def addManufacturerToDatabase(self,formData):
      #  newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.name.data, formData.isContractValid.data) 
        newManufacturerData = Manufacturers(formData.manufacturerId.data, formData.name.data, True) 
        #isManufacturerIdPresent
        
        db.session.add(newManufacturerData) 
        db.session.commit()
        # need to check if data is being added to database automatically
        #db.session.flush()
        #db.session.refresh(newCustomerData)
        #db.session.close()
        #return "from StorageClass"
    
    def check_if_manufacturer_exists(self,formData):
        manufacturer_id = Manufacturers.query.filter_by( manufacturerId = formData.manufacturerId.data).first()
        
        if manufacturer_id:
            return False
        else:
            return True
    
    def addCategoryToDatabase(self,formData):
        newManufacturerData = Category(formData.categoryId.data, formData.categoryDescription.data)
        
        db.session.add(newManufacturerData) 
        db.session.commit()    
               
    def check_if_category_exists(self,formData):
        category_id = Category.query.filter_by( categoryId = formData.categoryId.data).first()
        
        if category_id:
            return False
        else:
            return True
         