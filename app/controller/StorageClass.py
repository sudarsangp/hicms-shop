
'''
    This class will retrieve data from the database which inturn is represented
     by the SQL-alchemy classes.
     
'''
from app.model.models import db
from app.model.models import Customer
from flask import session

class StorageClass(object):
    
    def addCustomerTODatabase(self,formData):
        newCustomerData = Customer(formData.customername.data,formData.customeraddress.data,
                                   formData.handphone.data,formData.emailid.data,formData.dateofjoining.data,
                                   formData.passwordcustomer.data)
    
        db.session().add(newCustomerData)
        db.session().commit()