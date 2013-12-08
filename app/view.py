from flask import render_template, flash, request, session, redirect, url_for, jsonify, abort, make_response
from flask.ext.login import login_required
from app import app, login_manager

from form.forms import RegisterShopForm, SignupForm, SigninForm, ShopAdminFunction, AddCustomer ,AddManufacturer , AddCategory, AddProduct, BuyItem, HardwareImitater, AddDisplayStock, SearchPDUId,AddDisplayUnit

from form.forms import SearchBarcode, GetStockForm, SettingsForm, SetDiscount

from model.models import Check, User, db, Customer
from controller import Logic,InterfaceForPos
from controller.Feedback import Feedback
from controller.StorageClass import StorageClass

import json, requests
from ast import literal_eval

from config import POSTS_PER_PAGE

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
  if 'email' not in session:
    return redirect(url_for('signin'))

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
      return redirect(url_for('view_all_transactions', page = 1))  

    elif operation == "viewpdubyid":
      return redirect(url_for('pdudisplaybyid', operation = operation))
    
    elif operation == "retrieveserverinformation":
      return redirect(url_for("shop_server_info"))
    
    elif operation == "adddisplaystock":
      return redirect(url_for("add_Display_Stock", operation = operation))  

    elif operation == "requeststock":
      return redirect(url_for('request_stock', operation = operation))

    elif operation == "getprice":
      return redirect(url_for('get_price', operation = operation))

    elif operation == "addpricedisplayunit":
      return redirect(url_for('addPduDisplay', operation = operation)) 
    
    elif operation == "setdiscount":
      return redirect(url_for('set_discount', operation = operation))

    else:
      return "Mapping not yet implemented"

  elif request.method == 'GET':
    return render_template('SAproduct_operation.html', form = form)

@app.route('/transaction/<operation>', methods = ['POST', 'GET'])
def submit_transaction(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  feedback = logicObject.execute(operation,None)
  return render_template('feedback.html', feedback = feedback)

@app.route('/productsearch/<operation>', methods = ['POST','GET'])
def search_barcode(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchBarcode()
  if request.method == "POST":
    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productsearch/searchBarcode')
    form_validation = form.validateNumber(form.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productsearch/searchBarcode')
    
    logicObject = Logic.Logic()
    productobj = logicObject.execute(operation,form)
    if productobj:
      return render_template('productdetailsforbarcode.html', productobj = productobj)
    else:
      return redirect(url_for('defaulterror'))

  elif request.method == 'GET':
    print "in get request"
    return render_template('searchbarcode.html',form = form)

@app.route('/productdiscount/<operation>', methods = ['POST', 'GET'])
def set_discount(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  
  #if request.method == "POST":
  #  logicObject = Logic.Logic()
  form = SetDiscount()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/productdiscount/setdiscount')
    form_validation = form.validateNumber(form.discount)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for discount" , redirecturl = '/productdiscount/setdiscount')

    logicObject = Logic.Logic()
    print form.discount.data
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html', feedback = feedback)
  
  elif request.method == 'GET':
    return render_template('setdiscount.html',form = form)
  # this part for dynamic search
  #logicObject = Logic.Logic()
  #allproducts = logicObject.execute("viewproducts", None)
  #return render_template('fordiscountlistinginventory.html', allproducts = allproducts)

@app.route('/displayall/<operation>', methods = ['POST','GET'])
def view_all_products(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  allproducts = logicObject.execute(operation, None)
  return render_template('listinginventory.html', allproducts = allproducts)


#@app.route('/productTransactionsDisplayAll/viewproducttransactions', methods = ['POST','GET'])
@app.route('/productTransactionsDisplayAll/<int:page>',methods = ['POST','GET'])
def view_all_transactions(page = 1):
  if 'email' not in session:
    return redirect(url_for('signin'))

  storageObject = StorageClass()
  logicObject = Logic.Logic()
  #allTransactions = logicObject.execute("viewproducttransactions", None)
  allTransactions = storageObject.getTransactions(page,POSTS_PER_PAGE)
  return render_template('listProductTransactions.html', allTransactions = allTransactions)   

@app.route('/customer/<operation>', methods = ['POST', 'GET'])
#@login_required
def addcustomer(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

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
  if 'email' not in session:
    return redirect(url_for('signin'))

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
  if 'email' not in session:
    return redirect(url_for('signin'))

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
  if 'email' not in session:
    return redirect(url_for('signin'))

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

@app.route('/adddisplaystock/<operation>', methods = ['POST', 'GET'])
#@login_required
def add_Display_Stock(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = AddDisplayStock()  
  if request.method == 'POST':

    form_validation = form.validateNotEmpty(form.barcode)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/adddisplaystock/adddisplaystock')
    form_validation = form.validateNumber(form.barcode)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/adddisplaystock/adddisplaystock')

    form_validation = form.validateNotEmpty(form.quantity)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for quantity" , redirecturl = '/adddisplaystock/adddisplaystock')
    form_validation = form.validateNumber(form.quantity)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for quantity" , redirecturl = '/adddisplaystock/adddisplaystock')

    logicObject = Logic.Logic()
    feedback = logicObject.execute('adddisplaystock',form)
    return render_template('feedback.html', feedback = feedback)
  
  elif request.method == 'GET':
    return render_template('adddisplaystock.html', form=form)
  
@app.route('/user', methods = ['POST', 'GET'])
def buyitem():
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = BuyItem()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('buyitem.html', form=form)

    logicObject = Logic.Logic()
    feedback = logicObject.execute('buyitem',form)
    return render_template('feedback.html', feedback = feedback)

  elif request.method == 'GET':
    return render_template('buyitem.html', form=form)

@app.route('/defaulterror')
def defaulterror():
  if 'email' not in session:
    return redirect(url_for('signin'))

  return render_template('errorstatus.html', statusmessage = "data not present" , redirecturl = '/saoperation')

#to check the database part works fine
@app.route('/db')
def db_check():
  if 'email' not in session:
    return redirect(url_for('signin'))

  checkdb = Check()
  return checkdb.check_id()

@app.route('/shopserverinfo', methods = ['POST','GET']) 
def shop_server_info():
  if 'email' not in session:
    return redirect(url_for('signin'))

  #fromhq = request.data
  #change to this one for final demo
  #fromhq = requests.get('http://ec2-54-213-168-121.us-west-2.compute.amazonaws.com/download')
  fromhq = requests.get('http://127.0.0.1:5000/download')
  #alldata = json.loads(fromhq)
  alldata = fromhq.json()
  feedback = Feedback()

  alldetails = alldata['update']
  if alldetails == 'No file':
    feedback.setinfo("No File")
    feedback.setdata("Empty")
    feedback.setcommandtype('update')
    return render_template('feedback.html', feedback = feedback)

  del alldetails[0]
  #print type(productdetails[0])
  parsed_product_list = []
  edit_product_list = []
  delete_product_list = []

  for i in range(len(alldetails)):
    common_dict = literal_eval(alldetails[i])
    if 'addproducts' in common_dict:
      parsed_product_list.append(common_dict['addproducts'])
    elif 'editproducts' in common_dict:
      edit_product_list.append(common_dict['editproducts'])
    elif 'deleteproducts' in common_dict:
      delete_product_list.append(common_dict['deleteproducts'])

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

  for i in range(len(delete_product_list)):
    delete_list_of_products = literal_eval(json.dumps(delete_product_list[i]))
    form.barcode.data = delete_list_of_products['barcode']
    feedback = logicObject.execute("deleteproduct",form)
  #check case when produc list exists provide some feedback
  feedback.setinfo("Success")
  feedback.setdata(alldata)
  feedback.setcommandtype('update')
  return render_template('feedback.html', feedback  = feedback)
  
def get_from_shop(barcode,quantity):
  urldest = 'http://g10cg3002.ngrok.com/getfromshop'
  bar_quant = {'barcode':barcode,'quantity':quantity}
  send_data = {'barcodequantity':bar_quant}
  print barcode, quantity
  jsend = json.dumps(send_data)
  r = requests.get(urldest,data = jsend)
  responsestatus = r.json()
  return responsestatus['status']

@app.route('/hardwareImitater', methods = ['POST', 'GET'])
def hardwareImitater():
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = HardwareImitater()
  if request.method == "POST":
    # parse the data
    dummyPosInterface = InterfaceForPos.InterfaceForPos()
    newBarcodeQtyDict =  dummyPosInterface.parseForSoftwareImitater(form) 
    #print newBarcodeQtyDict
    # provide the form with dictionary as a parameter to the execute method
    logicObject = Logic.Logic()
    form.barcode.data = newBarcodeQtyDict
    feedback = logicObject.execute('hwImitateBuy',form)
    if feedback.getcommandtype() == "Ask other shop":
      barcode_in = feedback.getinfo()
      quantity_in = feedback.getdata()
      feedback.setinfo(get_from_shop(barcode_in, quantity_in))
      storageObject = StorageClass()
      customerid = form.customerId.data
      emailid = storageObject.get_email_for_customer(customerid)
      send_customer_neighbour(feedback.getinfo(), emailid)
    elif feedback.getcommandtype() == "transaction success":
      storageObject = StorageClass()
      customerid = form.customerId.data
      emailid = storageObject.get_email_for_customer(customerid)
      #print "ok" + str(feedback.getdata())
      send_email(emailid, feedback.getdata(), feedback.getinfo())
    return render_template('feedback.html', feedback = feedback)
  elif request.method == 'GET':
    return render_template('hardwareImitater.html',form = form)  

@app.route('/requeststock/<operation>', methods = ['GET', 'POST'])
def request_stock(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = GetStockForm()
  if request.method == "POST":

    logicObject = Logic.Logic()
    #newBarcodeQtyDict = logicObject.parsebarcodequantity(form)
    #form.barcode.data = newBarcodeQtyDict
    #print form.barcode.data
    #print form.quantity.data
    feedback = logicObject.execute(operation,form)
    return render_template('feedback.html', feedback  = feedback)

  elif request.method == 'GET':
    return render_template('getstock.html',form = form)

@app.route('/getpriceresult/<operation>', methods = ['GET', 'POST'])
def get_price(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  logicObject = Logic.Logic()
  feedback = logicObject.execute(operation,None)
  return render_template('feedback.html', feedback  = feedback)

#@app.route('/pdudisplaybybarcode/<operation>', methods = ['POST,GET]'])
#def pdudisplaybybarcode():
#      form =  SearchPDUBarcode()
#      if request.method == "POST":
#          logicObject = Logic.Logic()
#          pduObj = logicObject.execute(operation, form)
#
#          if pduObj:
  #          return render_template('pdudetailsforbarcode.html', pduObj = pduObj)
  #        else :
 #           return redirect(url_for('defaulterror'))
 #     elif request.method == "GET" :

 #         return render_template('searchpdubarcode.html', form = form)

@app.route('/pdudisplaybyid/<operation>', methods = ['POST','GET'])
def pdudisplaybyid(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SearchPDUId()
  if request.method == "POST":

    form_validation = form.validateNotEmpty(form.Id)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for pduid" , redirecturl = '/pdudisplaybyid/viewpdubyid')
    form_validation = form.validateNumber(form.Id)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for pduid" , redirecturl = '/pdudisplaybyid/viewpdubyid')

    logicObject = Logic.Logic()
    pduObj = logicObject.execute(operation,form)

    if pduObj:
      return render_template('pdudetailsforid.html', pduObj = pduObj)
    else:
      return redirect(url_for('defaulterror'))
  elif request.method == "GET" :
    return render_template('searchpdubyid.html', form = form)

@app.route('/addpduunit/<operation>',methods = ['POST','GET'])
def addPduDisplay(operation):
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = AddDisplayUnit()
     
  if request.method == "POST":

      form_validation = form.validateNotEmpty(form.displayId)
      if str(form_validation) == 'Cannot give empty space':
        return render_template('errorstatus.html', statusmessage = form_validation + " for displayid" , redirecturl = '/addpduunit/addpricedisplayunit')
      form_validation = form.validateNumber(form.displayId)
      if str(form_validation) == 'please enter only numbers':
        return render_template('errorstatus.html', statusmessage = form_validation + " for displayid" , redirecturl = '/addpduunit/addpricedisplayunit')
      
      form_validation = form.validateNotEmpty(form.barcode)
      if str(form_validation) == 'Cannot give empty space':
        return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/addpduunit/addpricedisplayunit')
      form_validation = form.validateNumber(form.barcode)
      if str(form_validation) == 'please enter only numbers':
        return render_template('errorstatus.html', statusmessage = form_validation + " for barcode" , redirecturl = '/addpduunit/addpricedisplayunit')

      logicObject = Logic.Logic()
      feedback = logicObject.execute(operation,form)

      return render_template('feedback.html', feedback = feedback)
     
  elif request.method == "GET" :
      return render_template('addpduunit.html', form = form)

from flask.ext.mail import Message
from app import mail
from config import ADMINS,RECIPIENTS

#@app.route('/sendemail')
def send_email(recipientemail, transactiondetail, totalpriceinfo):
  if 'email' not in session:
    return redirect(url_for('signin'))
  transactionfinal = "<b> Transaction Details </b> </thead>"
  list_recipient = list()
  list_recipient.append(recipientemail)
  transactionfinal += '<table> <thead> <tr> <th> Barcode </th> <th> Quantity </th> <th> Price </th> </tr> </thead> <tbody> '
  for eachbarcodedetail in transactiondetail:
    print eachbarcodedetail
    detailinfo = eachbarcodedetail.split(',')
    transactionfinal += '<tr>' + '<td>' + str(detailinfo[0]) + '</td>' + '<td>' + str(detailinfo[1]) + '</td>' +  '<td>' + str(detailinfo[2]) + '</td> </tr>'
  transactionfinal += '</tbody> </table>'
  msg = Message("Transaction Details", sender = ADMINS[0], recipients = list_recipient)
  msg.body = 'text body'
  msg.html = transactionfinal + '<br>' + '<b>' + str(totalpriceinfo) + '</b>' + '<br>'
  with app.app_context():
    mail.send(msg)
  return "checking"

def send_customer_neighbour(details, emailid):
  if 'email' not in session:
    return redirect(url_for('signin'))

  list_recipient = list()
  list_recipient.append(emailid)
  msg = Message("Neighbour Shop Information", sender = ADMINS[0], recipients = list_recipient)
  msg.body = 'text body'
  msg.html = details
  with app.app_context():
    mail.send(msg)

import datetime, time

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
  if 'email' not in session:
    return redirect(url_for('signin'))

  form = SettingsForm()
  if request.method == 'POST':
    form_validation = form.validateNotEmpty(form.pricefreq)
    if str(form_validation) == 'Cannot give empty space':
      return render_template('errorstatus.html', statusmessage = form_validation + " for time" , redirecturl = '/settings')
    form_validation = form.validateNumber(form.pricefreq)
    if str(form_validation) == 'please enter only numbers':
      return render_template('errorstatus.html', statusmessage = form_validation + " for time" , redirecturl = '/settings')

    fname = "activepricefrequncy.txt"
    f = open(fname,'w')
    dataforfile = {}
    starttimeforfile = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    starttimedelta = datetime.datetime.strptime(starttimeforfile,'%Y-%m-%d %H:%M:%S' )
    endtimedelta = starttimedelta + datetime.timedelta(minutes = int(form.pricefreq.data))
    endtimeforfile = endtimedelta.strftime('%Y-%m-%d %H:%M:%S')
    dataforfile = {}
    f.write(';')
    dataforfile['activepricefreq'] = form.pricefreq.data
    f.write(str(dataforfile))
    dataforfile = {}
    f.write(';')
    dataforfile['starttime'] = starttimeforfile
    f.write(str(dataforfile))
    dataforfile = {}
    f.write(';')
    dataforfile['endtime'] = endtimeforfile
    f.write(str(dataforfile))
    f.close()
    datasent = "wriiten to file"
    return render_template('settingsfeedback.html',data = datasent)

  elif request.method == "GET":
    return render_template('settings.html', form = form)