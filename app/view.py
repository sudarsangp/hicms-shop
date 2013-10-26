from flask import render_template, flash, request, session, redirect, url_for, jsonify, abort, make_response
from flask.ext.login import login_required
from app import app, login_manager

from form.forms import RegisterShopForm, SignupForm, SigninForm, ShopAdminFunction, AddCustomer ,AddManufacturer , AddCategory, AddProduct, BuyItem
from form.forms import SearchBarcode

from model.models import Check, User, db, Customer
from controller import Logic

import json
from ast import literal_eval

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

@app.route('/shopserverinfo', methods = ['POST']) 
def shop_server_info():
  fromhq = request.data
  alldata = json.loads(fromhq)
  alldetails = alldata['update']
  del alldetails[0]
  #print type(productdetails[0])
  parsed_product_list = []
  edit_product_list = []
  for i in range(len(alldetails)):
    common_dict = literal_eval(alldetails[i])
    if 'addproducts' in common_dict:
      parsed_product_list.append(common_dict['addproducts'])
    elif 'editproducts' in common_dict:
      edit_product_list.append(common_dict['editproducts'])

  logicObject = Logic.Logic()
  form = AddProduct()
  for i in range(len(parsed_product_list)):
    list_of_products = literal_eval(json.dumps(parsed_product_list[i]))
    form.barcode.data = list_of_products['barcode']
    form.proname.data = list_of_products['proname']
    form.manufacturerId.data = list_of_products['manufacturerId']
    form.category.data = list_of_products['category']
    form.price.data = list_of_products['price']
    form.minStock.data = list_of_products['minStock']
    #change this one
    form.currentStock.data = 0
    form.bundleUnit.data = list_of_products['bundleUnit']
    # change these two
    form.displayPrice.data = 0
    form.displayQty.data = 0
    feedback = logicObject.execute("addproduct",form)
  
  for i in range(len(edit_product_list)):
    edit_list_of_products = literal_eval(json.dumps(edit_product_list[i]))
    form.barcode.data = edit_list_of_products['barcode']
    form.price.data = edit_list_of_products['price']
    form.minStock.data = edit_list_of_products['minStock']
    form.bundleUnit.data = edit_list_of_products['bundleUnit']
    feedback = logicObject.execute("updateproduct",form)
 
  #check case when produc list exists provide some feedback
  
  return str(fromhq)
  