from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField, TextAreaField, SubmitField, ValidationError, RadioField, DateField, SelectField,FormField
from app.model.models import User

# TODO: Remove this class from here
class RegisterShopForm(Form):
	shopname = TextField('shopname', validators = [validators.Required()])
	location = TextField('location', validators = [validators.Required()])
	shopid = TextField('userid', [validators.Length(min=5, max=25),validators.Required()])
	password = PasswordField('password',[validators.Required()])
	confirmpassword = PasswordField('confirmpassword',[validators.Required()])

class ShopAdminFunction(Form):
  operations = RadioField('operations', choices = [('addproduct','Add product'),('editproduct','Edit Product'),('removeproduct','Remove Product'),
  ('addcustomer','Add Customer'),('editcustomer','Edit Customer'),('removecustomer','Remove Customer'),('addmanufacturer','Add Manufacturer'),('addcategory','Add Category'),('addproduct','Add Product')])

class AddCustomer(Form):
  customername = TextField('customername', validators = [validators.Required()])
  customeraddress = TextAreaField('customeraddress', validators = [validators.Required()])
  handphone = TextField('handphone', validators = [validators.Required()])
  emailid = TextField('emailid', validators = [validators.Required(), validators.Email("Please enter your email address.")])
  dateofjoining = DateField('dateofjoining', validators = [validators.Required()])
  passwordcustomer = PasswordField('passwordcustomer', validators = [validators.Required()])
  
  def __init__(self, *args, **kwargs):
   Form.__init__(self, *args, **kwargs)

class AddManufacturer(Form):
  manufacturerId = TextField('manufacturerId',validators = [validators.Required("Please enter manufacturer Id")])
  mname = TextField('name',validators = [validators.Required("Please enter manufacturer Name")])
  isContractValid = TextField('isContractValid',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

class AddCategory(Form):
  categoryId = TextField('categoryId',validators = [validators.Required()])
  categoryDescription = TextField('categoryDescription',validators = [validators.Required()])
  isExpirable = TextField('isExpirable',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)  
    
class AddProduct(Form):
  barcode = TextField('barcode',validators = [validators.Required()])
  proname = TextField('name',validators = [validators.Required()])
  manufacturerId = SelectField('manufacturerId',choices=[])
  manufacturerForm = FormField(AddManufacturer)
#  manufacturerId = TextField('manufacturerId',validators = [validators.Required()])
  category = SelectField('category',choices=[])
  categoryForm = FormField(AddCategory)
  price = TextField('price',validators = [validators.Required()])
  minStock = TextField('minStock',validators = [validators.Required()])
  currentStock = TextField('currentStock',validators = [validators.Required()])
  bundleUnit = TextField('bundleUnit',validators = [validators.Required()])
  displayPrice = TextField('displayPrice',validators = [validators.Required()])
  displayQty = TextField('displayQty',validators = [validators.Required()])
	
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)  
  


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
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False
#####################################################################################################################################################