from flask import render_template, flash, request, session, redirect, url_for, jsonify, abort, make_response
from flask.ext.login import login_required
from app import app, login_manager

from form.forms import RegisterShopForm, SignupForm, SigninForm, ShopAdminFunction, AddCustomer ,AddManufacturer , AddCategory, AddProduct, BuyItem, HardwareImitater

from form.forms import SearchBarcode

from model.models import Check, User, db, Customer
from controller import Logic,InterfaceForPos

@app.route('/check')
def default():
	return render_template("baselayout.html")

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
      return redirect(url_for('sa_operation'))
                 
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

#shop admin actual functions
@app.route('/saoperation', methods = ['POST','GET'])
def sa_operation():
  form = ShopAdminFunction()
  if request.method == "POST":
    operation = form.operations.data

    if operation == "searchBarcode":
      return redirect(url_for('search_barcode',operation = operation))

    elif operation == "viewproducts":
      return redirect(url_for('view_all_products', operation = operation))

    elif operation == "submittransaction":
      return redirect(url_for('submit_transaction', operation = operation))

    elif operation == "viewproducttransactions":
      return redirect(url_for('view_all_transactions', operation = operation))  
    
    else:
      return "Mapping not yet implemented"

  elif request.method == 'GET':
    return render_template('SAproduct_operation.html', form = form)

@app.route('/transaction/<operation>', methods = ['POST', 'GET'])
def submit_transaction(operation):
  logicObject = Logic.Logic()
  feedback = logicObject.execute(operation,None)
  return render_template('feedback.html', feedback = feedback)

@app.route('/productsearch/<operation>', methods = ['POST','GET'])
def search_barcode(operation):
  form = SearchBarcode()
  if request.method == "POST":
    logicObject = Logic.Logic()
    productobj = logicObject.execute(operation,form)
    if productobj:
      return render_template('productdetailsforbarcode.html', productobj = productobj)
    else:
      return redirect(url_for('defaulterror'))

  elif request.method == 'GET':
    return render_template('searchbarcode.html',form = form)

@app.route('/displayall/<operation>', methods = ['POST','GET'])
def view_all_products(operation):
  logicObject = Logic.Logic()
  allproducts = logicObject.execute(operation, None)
  return render_template('listinginventory.html', allproducts = allproducts)
  
@app.route('/productTransactionsDisplayAll/<operation>', methods = ['POST','GET'])
def view_all_transactions(operation):
    logicObject = Logic.Logic()
    allTransactions = logicObject.execute(operation, None)
    return render_template('listProductTransactions.html', allTransactions = allTransactions)   

@app.route('/customer/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcustomer(operation):
 
  form = AddCustomer()
  if request.method ==  "POST": #and form.validate():
    #print "check"
    logicObject = Logic.Logic()
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html', feedback = feedback)
    
  else:
   return render_template('addcustomer.html', form = form)

@app.route('/manufacturer/<operation>', methods = ['POST', 'GET'])
#@login_required    
def addmanufacturer(operation):
	
	form = AddManufacturer()
	if request.method == "POST":
	
		logicObject = Logic.Logic()
		feedback = logicObject.execute(operation,form)
		return render_template('feedback.html',feedback = feedback)
	
	elif request.method == 'GET':
		return render_template('addmanufacturer.html', form = form)	

@app.route('/category/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcategory(operation):
	
	form = AddCategory()
	if request.method == "POST":
	
		logicObject = Logic.Logic()
		feedback = logicObject.execute(operation,form)
		return render_template('feedback.html',feedback = feedback)
	
	elif request.method == 'GET':
		return render_template('addcategory.html', form = form)	
	
@app.route('/productadd/<operation>', methods = ['POST', 'GET'])
#@login_required    
def addproduct(operation):
	
	logicObject = Logic.Logic()
	manufacturers = logicObject.execute('viewmanufacturers',None)
	manufacturer_choices = [(manufacturer.manufacturerId,manufacturer.name) for manufacturer in manufacturers]
	manufacturer_choices.append(('-1','None'))
	categories = logicObject.execute('viewcategories',None)
	category_choices =[(category.categoryId,category.categoryDescription) for category in categories]
	category_choices.append(('-1','None'))
	
	form = AddProduct()	
	form.manufacturerId.choices = manufacturer_choices
	form.category.choices = category_choices
	if request.method == "POST":
		if(form.manufacturerId.data == '-1'):
			form.manufacturerId.data = form.manufacturerForm.manufacturerId.data
			feedback = logicObject.execute('addmanufacturer',form.manufacturerForm)
			if(feedback.getinfo() != "Success: data added "):
				return render_template('feedback.html',feedback = feedback)
		
		if(form.category.data == '-1'):
			form.category.data = form.categoryForm.categoryId.data	
			feedback = logicObject.execute('addcategory',form.categoryForm)
			if(feedback.getinfo() != "Success: data added "):
				return render_template('feedback.html',feedback = feedback)	
		
		
		feedback = logicObject.execute(operation,form)
		
		return render_template('feedback.html',feedback = feedback)
	
	elif request.method == 'GET':
		return render_template('addproduct.html', form = form)
	
@app.route('/user', methods = ['POST', 'GET'])
def buyitem():
  form = BuyItem()
  if request.method == 'POST':
    logicObject = Logic.Logic()
    feedback = logicObject.execute('buyitem',form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('buyitem.html', form=form)

@app.route('/defaulterror')
def defaulterror():
  return "Data not present"

#to check the database part works fine
@app.route('/db')
def db_check():
	checkdb = Check()
	return checkdb.check_id()

@app.route('/hardwareImitater', methods = ['POST', 'GET'])
def hardwareImitater():
	form = HardwareImitater()
	if request.method == "POST":
		# parse the data
		dummyPosInterface = InterfaceForPos.InterfaceForPos()
		newBarcodeQtyDict =  dummyPosInterface.parseForSoftwareImitater(form) 
 		
 		# provide the form with dictionary as a parameter to the execute method
 		logicObject = Logic.Logic()
 		form.barcode.data = newBarcodeQtyDict
 		feedback = logicObject.execute('hwImitateBuy',form)
 		return render_template('feedback.html', feedback = feedback)

		
	elif request.method == 'GET':
		return render_template('hardwareImitater.html',form = form)  
