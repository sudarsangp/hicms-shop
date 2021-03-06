from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField, TextAreaField, SubmitField, ValidationError, RadioField, DateField, SelectField,FormField
from app.model.models import User

import re

def validateNotEmpty(form,field):
  s = field.data
  s = s.replace(' ','')
  if len(s) == 0:
    raise ValidationError('Cannot give empty space')

def validateNumber(form,field):
  s = field.data
  if re.match("^\D+$",s):
    raise ValidationError('please enter only numbers')


class RegisterShopForm(Form):
	shopname = TextField('shopname', validators = [validators.Required()])
	location = TextField('location', validators = [validators.Required()])
	shopid = TextField('userid', [validators.Length(min=5, max=25),validators.Required()])
	password = PasswordField('password',[validators.Required()])
	confirmpassword = PasswordField('confirmpassword',[validators.Required()])

class ShopAdminFunction(Form):
  operations = RadioField('operations', choices = [('searchBarcode','Search Barcode'),('viewproducts','View Product'),('submittransaction','Submit Transaction'),
  ('retrieveserverinformation','Retrieve Server Information'),('viewproducttransactions','View Transactions'),('adddisplaystock','Add Display Stock'),('requeststock','Request Stock'),('getprice','Get Price'),('viewpdubyid', 'Search PDU'),
   ('addpricedisplayunit','Add price Display Unit'),('setdiscount','Set Discount'),('addcustomer','Add Customer') ])

  # for testing use this /product url
  """[('addproduct','Add product'),('editproduct','Edit Product'),('removeproduct','Remove Product'),
  ,('editcustomer','Edit Customer'),('removecustomer','Remove Customer'),('addstock', 'Add Stock'), 
  ('addmanufacturer','Add Manufacturer'),('addcategory','Add Category')])"""


class AddCustomer(Form):
  #customername = TextField('customername', validators = [validators.Required(), validateNotEmpty])
  #customeraddress = TextAreaField('customeraddress', validators = [validators.Required(), validateNotEmpty ])
  #handphone = TextField('handphone', validators = [validators.Required(), validateNotEmpty, validateNumber])
  customerId = TextField('customerId', validators = [validators.Required(), validateNotEmpty]) 
  #dateofjoining = DateField('dateofjoining', validators = [validators.Required()])
  email = TextField("Email")
  
  def __init__(self, *args, **kwargs):
   Form.__init__(self, *args, **kwargs)

  def validateNotEmpty(self,field):
    s = field.data
    s = s.replace(' ','')
    if len(s) == 0:
      return 'Cannot give empty space'
  
  def validateNumber(form,field):
    s = field.data
    if re.match("^\d{8}$",s) is None:
      return 'please enter only 8 digit numbers'

class AddManufacturer(Form):
  manufacturerId = TextField('manufacturerId',validators = [validators.Required("Please enter manufacturer Id"), validateNotEmpty])
  mname = TextField('name',validators = [validators.Required("Please enter manufacturer Name"), validateNotEmpty])
  isContractValid = TextField('isContractValid',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class AddCategory(Form):
  categoryId = TextField('categoryId',validators = [validators.Required(), validateNotEmpty])
  categoryDescription = TextField('categoryDescription',validators = [validators.Required(), validateNotEmpty])
  isExpirable = TextField('isExpirable',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)  
    
class AddProduct(Form):
  barcode = TextField('barcode',validators = [validators.Required(), validateNotEmpty, validateNumber])
  proname = TextField('name',validators = [validators.Required(), validateNotEmpty])
  manufacturerId = SelectField('manufacturerId',choices=[])
  manufacturerForm = FormField(AddManufacturer)
#  manufacturerId = TextField('manufacturerId',validators = [validators.Required()])
  category = SelectField('category',choices=[])
  categoryForm = FormField(AddCategory)
  price = TextField('price',validators = [validators.Required(), validateNotEmpty, validateNumber])
  minStock = TextField('minStock',validators = [validators.Required(), validateNotEmpty, validateNumber])
  currentStock = TextField('currentStock',validators = [validators.Required(), validateNotEmpty, validateNumber])
  bundleUnit = TextField('bundleUnit',validators = [validators.Required(), validateNumber, validateNotEmpty])
  displayPrice = TextField('displayPrice',validators = [validators.Required(), validateNumber, validateNotEmpty])
  displayQty = TextField('displayQty',validators = [validators.Required(), validateNumber, validateNotEmpty])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)  
  
class BuyItem(Form):
  barcode = TextField('barcode')
  quantity = TextField('quantity')

  def __init__(self, *args, **kwargs): # needed for importing in view.py
    Form.__init__(self, *args, **kwargs)

class SearchBarcode(Form):
  barcode = TextField('barcode')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
  
  def validateNotEmpty(self,field):
    s = field.data
    s = s.replace(' ','')
    if len(s) == 0:
      return 'Cannot give empty space'
  
  def validateNumber(form,field):
    s = field.data
    if re.match("^\d+$",s) is None:
      return 'please enter only numbers'

class AddDisplayStock(Form):    
  barcode = TextField('barcode')
  quantity = TextField('quantity')

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
  
  def validateNotEmpty(self,field):
    s = field.data
    s = s.replace(' ','')
    if len(s) == 0:
      return 'Cannot give empty space'
  
  def validateNumber(form,field):
    s = field.data
    if re.match("^\d+$",s) is None:
      return 'please enter only numbers'

class AddDisplayUnit(Form):
   displayId = TextField('displayId')
   barcode = TextField('barcode')
   
   def __init__(self, *args, **kwargs):
       Form.__init__(self, *args, **kwargs)
   
   def validateNotEmpty(self,field):
    s = field.data
    s = s.replace(' ','')
    if len(s) == 0:
      return 'Cannot give empty space'
  
   def validateNumber(form,field):
    s = field.data
    if re.match("^\d+$",s) is None:
      return 'please enter only numbers'

################################################################################################################################################
class SignupForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    #print user.check_password(self.password.data)
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
#####################################################################################################################################################
class GetStockForm(Form):
  barcode = TextField('barcode')
    
  def __init__(self, *args, **kwargs): # needed for importing in view.py
      Form.__init__(self, *args, **kwargs)

class HardwareImitater(Form):
    
    transactionDate =  TextField('transactionDate')
    cashierId = TextField('cashierId')
    customerId = TextField('customerId')
    barcode = TextField('barcode')
    
    def __init__(self, *args, **kwargs): # needed for importing in view.py
        Form.__init__(self, *args, **kwargs)


class SearchPDUBarcode(Form):

      barcode = TextField('barcode')

      def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class SearchPDUId(Form):

      Id = TextField('id')

      def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

      def validateNotEmpty(self,field):
        s = field.data
        s = s.replace(' ','')
        if len(s) == 0:
          return 'Cannot give empty space'
  
      def validateNumber(form,field):
        s = field.data
        if re.match("^\d+$",s) is None:
          return 'please enter only numbers'

class SettingsForm(Form):
  pricefreq = TextField('pricefreq')
  
  def __init__(self, *args, **kwargs): # needed for importing in view.py
      Form.__init__(self, *args, **kwargs)

  def validateNotEmpty(self,field):
    s = field.data
    s = s.replace(' ','')
    if len(s) == 0:
      return 'Cannot give empty space'
  
  def validateNumber(form,field):
    s = field.data
    if re.match("^\d+$",s) is None:
      return 'please enter only integers'

class SetDiscount(Form):
  barcode = TextField('barcode')
  discount = TextField('discount')
  def __init__(self, *args, **kwargs): # needed for importing in view.py
      Form.__init__(self, *args, **kwargs)

  def validateNotEmpty(self,field):
        s = field.data
        s = s.replace(' ','')
        if len(s) == 0:
          return 'Cannot give empty space'
  
  def validateNumber(form,field):
    s = field.data
    if re.match("^\d+$",s) is None:
      return 'please enter only numbers'