from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), index = True, unique = True)
	
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)


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