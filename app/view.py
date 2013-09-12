from flask import render_template, flash, request, session, redirect, url_for
from flask.ext.login import login_required
from app import app, login_manager
from form.forms import LoginForm, RegisterShopForm, SignupForm, SigninForm, ShopAdminFunction
from model.models import Check, User, db
from controller.Logic import Logic

@app.route('/check')
def default():
	return render_template("baselayout.html")

#@login_manager.user_loader
#def load_user(userid):
#	return User.get(userid)

@app.route('/register')
def register():
	form = RegisterShopForm();
	return render_template('registershop.html',form = form)

#############################################################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
  	return redirect(url_for('profile')) 

  if request.method == 'POST':
    if form.validate() == False:
    	return render_template('signup.html', form=form)
    else:
    	newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      	db.session.add(newuser)
      	db.session.commit()
      	session['email'] = newuser.email
     	return redirect(url_for('profile'))
   
  elif request.method == 'GET':
  	return render_template('signup.html', form=form)

@app.route('/')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'email' in session:
    return redirect(url_for('profile'))  

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('product_functions'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form) 

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('signin'))

@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')
##############################################################################################

# to check whether this page is accesible 
@app.route("/settings")
@login_required
def settings():
    return "Welcome"

#for manually adding product to the database or shop
@app.route('/product', methods = ['POST', 'GET'])
#@login_required
def product_functions():
  form = ShopAdminFunction();
  if request.method ==  "POST":
    
     operation = form.operations.data
     logicObject = Logic()
     logicObject.execute(operation)
    
  else:
    redirect(url_for('defaulterror')) 
 
  return render_template('SAproduct_operation.html',form=form)

@app.route('/defaulterror')
def defaulterror():
  return "Error found"

#to check the database part works fine
@app.route('/db')
def db_check():
	checkdb = Check()
	return checkdb.check_id()