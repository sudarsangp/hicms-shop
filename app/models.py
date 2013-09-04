from app import db
from werkzeug import generate_password_hash, check_password_hash

""" nets tuts tutorial flask login """
class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

""" this one from flask documentation """
#class User(db.Model):
#	id = db.Column(db.Integer, primary_key = True)
#	name = db.Column(db.String(64), index = True, unique = True)
#	
#	def is_authenticated(self):
#		return True
#
#	def is_active(self):
#		return True
#
#	def is_anonymous(self):
#		return False
#
#	def get_id(self):
#		return unicode(self.id)


""" to ensure whetehr database connection works """
class Check(db.Model):
	id_check = db.Column(db.Integer,primary_key=True)
	fullname = db.Column(db.String(80))

	def check_id(self):
		checklist = []
		all_query = Check.query.all()
		for x in range(len(all_query)):
			checklist.append(all_query[x].id_check)
		return str(checklist)