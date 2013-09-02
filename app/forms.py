from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField

class LoginForm(Form):
	userid = TextField('userid', [validators.Length(min=5, max=25),validators.Required()])
	password = PasswordField('password',[validators.Required()])
	remember_me = BooleanField('remember_me', default = False)

class RegisterShopForm(Form):
	shopname = TextField('shopname', validators = [validators.Required()])
	location = TextField('location', validators = [validators.Required()])
	shopid = TextField('userid', [validators.Length(min=5, max=25),validators.Required()])
	password = PasswordField('password',[validators.Required()])
	confirmpassword = PasswordField('confirmpassword',[validators.Required()])
