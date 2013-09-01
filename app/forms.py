from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, BooleanField

class LoginForm(Form):
	userid = TextField('userid', [validators.Length(min=5, max=25),validators.Required()])
	password = PasswordField('password',[validators.Required()])
	remember_me = BooleanField('remember_me', default = False)