from flask import render_template, flash
from flask.ext.login import login_required
from app import app, login_manager, forms
from forms import LoginForm
from models import Check

@app.route('/check')
def default():
	return render_template("base layout.html")

#@login_manager.user_loader
#def load_user(userid):
#	return User.get(userid)

@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	#if form.validate_on_submit():
	#	login_user(user)
	#	flash("Logged in Success")
	#	return redirect(request.args.get("next") or url_for("index"))
	return render_template('login.html',form = form)

# to check whether this page is accesible 
@app.route("/settings")
@login_required
def settings():
    return "Welcome"

#to check the database part works fine
@app.route('/db')
def db_check():
	checkdb = Check()
	return checkdb.check_id()