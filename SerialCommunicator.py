from app.controller import Logic,InterfaceForPos
from app.form.forms import HardwareImitater
from app import app
from ast import literal_eval
import serial
import time, datetime
import os

fragset = 0
fragBuyDetailsDict0 = dict()
fragBuyDetailsDict1 = dict()

def sendPriceChange():
    fname = "pricechange.txt"
    #print fname
    if os.stat(fname)[6] == 0:
      return False
    f = open(fname,'r')
    content = f.read()
    print content, str(content)
    list_content = content.split(';')
    del list_content[0]
    print list_content, type(list_content)
    #print list_content
    for i in range(len(list_content)):
    #print eachvalue
       eachitem = literal_eval(list_content[i])
       serialdetail = eachitem['pricedetail']
       price = serialdetail['price']
       barcode = serialdetail['barcode']
       name = serialdetail['name']
       pricedisplayid = serialdetail['pricedisplayid']
       print price, barcode, name, pricedisplayid
       
       stringToSend = '#' + str(pricedisplayid) + 'Barcode:' +  str(barcode) + '                        ' + 'Price:$' +str(price) + '\n'
       print stringToSend
       x = ser.write(stringToSend)
       time.sleep(0.1)
    open(fname,'w').close()
    return True

def parseSerialInput(receivedSerialData):
    if receivedSerialData[0] != "#" :
        print "Hash is not present"
    
    else:
        message = receivedSerialData [1:]
        parts = message.split(';')
        
        id_string = parts[0]
        opcode_hex_string = parts[1]
        
        # convert opcode to integer from hexadecimal value
        opcode = int(opcode_hex_string,16)
        
        if opcode == 2: # no message so return
            return
        
        elif opcode == 3:
            opcode_barcode = parts[2]
            
            posInterface = InterfaceForPos.InterfaceForPos()
            if(posInterface.getPriceForBarcode(opcode_barcode)==-1):
                responseOpcode = '01'
                responseToSend = '#' + id_string + responseOpcode + ';' + '\n'
                print responseToSend
                print "This is for the case product not present"
                no_of_char = ser.write(responseToSend)
                return
            productPrice =  int((posInterface.getPriceForBarcode(opcode_barcode) * 1000)/10)  # 10043940
            productDisplayQuantity = posInterface.getQuantityForBarcode(opcode_barcode)
            
            responseOpcode = '4'
            bundle_unit = posInterface.getBundleUnitForBarcode(opcode_barcode)
            responseToSend = '#' + id_string + responseOpcode + ';' + str(productPrice) + ';' + str(productDisplayQuantity) + ';'+ str(bundle_unit) + ';' + '\n'    
            print responseToSend
            no_of_char = ser.write(responseToSend)  #example '#14;5;7;\n            print "Hello World THis is Dinesh"
            time.sleep(0.1)
            return
        
        elif opcode == 6:
            customerId = parts[2]
            opcode_transactionDetails = parts[3]
            with app.test_request_context():    
                form = HardwareImitater()
                form.transactionDate.data = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
                form.cashierId.data = id_string
                form.customerId.data = str(customerId)
                form.barcode.data = opcode_transactionDetails 

                global fragset
                print fragset
                    
                if(fragset == 1):
                    customerMode = parts[4] 
                    if(int(customerMode) == 0):
#                        global form.barcode.data
                        print str(fragBuyDetailsDict0[int(id_string)])
                        print form.barcode.data
                        form.barcode.data = str(form.barcode.data) +  str(fragBuyDetailsDict0[int(id_string)])  # add previous fragmented data
                        print str(form.barcode.data)
                    else:
#                        global form.barcode.data
                        form.barcode.data = str(form.barcode.data) +  str(fragBuyDetailsDict1[int(id_string)]) #  add previous fragmented data                                                           


                dummyPosInterface = InterfaceForPos.InterfaceForPos()
                if dummyPosInterface.check_if_email_exists(form.customerId.data) is None:
                    responseOpcode = '01'
                    responseToSend = '#' + id_string + responseOpcode + ';' + '\n'
                    print responseToSend
                    print "This is for the case product not present"
                    no_of_char = ser.write(responseToSend)
                    return
                newBarcodeQtyDict =  dummyPosInterface.parseForSoftwareImitater(form)
                print str(form.barcode.data)
                print type(form.barcode.data)
                logicObject = Logic.Logic()
                form.barcode.data = newBarcodeQtyDict
                feedback = logicObject.execute('hwImitateBuy',form)
                dummyPosInterface.get_check_email(feedback, customerId)
                global fragSet
                fragset == 0
            
            return 
        
        elif opcode == 5: #frag buy
            fragBuyData = parts[3]
            customer_mode = parts[4]

            print type(parts[3])
            
            if(int(customer_mode) == 0):
                if(int(id_string) not in fragBuyDetailsDict0.keys()):
                    fragBuyDetailsDict0[int(id_string)] = str(fragBuyData)
                    print "fragmentation data0 added to id " + id_string
                
                else: 
                    fragBuyDetailsDict0[int(id_string)] = str(fragBuyDetailsDict0[int(id_string)]) + str(fragBuyData)
                    print "fragmentation data0 added to id " + id_string
                
                global fragSet
                fragset = 1
            else:
                if(int(id_string) not in fragBuyDetailsDict1.keys()):
                    fragBuyDetailsDict1[int(id_string)] = str(fragBuyData)
                else:
                    fragBuyDetailsDict1[int(id_string)] = str(fragBuyDetailsDict1[int(id_string)]) + str(fragBuyData)    
                global fragSet
                fragset = 1
                 
                return

        elif opcode == 8: # Intershop request
            barcodeNeeded = parts[2]
            quantity = parts[3]
            responseOpcode = '9'
            interface_object = InterfaceForPos.InterfaceForPos()
            shopidvalue = interface_object.from_cashier_internshop(barcodeNeeded,quantity)
            responseToSend = '#' + id_string + responseOpcode + ';' + str(shopidvalue) + ';' + '\n'

            print responseToSend
            no_of_char = ser.write(responseToSend)

if __name__ == '__main__':

#     while True:    
#         ser = serial.Serial('/dev/ttyUSB0')
#         x = ser.read()
#         print x
         
     ser = serial.Serial('COM12')
#     x = ser.write('#11;1;\n')
#     x = ser.write('#14;5;3\n') 
#    print x
     posInterface1 = InterfaceForPos.InterfaceForPos()
     cashier_id_list = posInterface1.getCashiers()
     list_cashierids = list()
     for cashier in cashier_id_list:
        list_cashierids.append(cashier.cashierId)
      
     while True:
         sendPriceChange()
         for eachcashier in list_cashierids:
         #print "in infinte"
             #print str(eachcashier)
             x = ser.write('#'+str(eachcashier) + '1;1;\n')
             time.sleep(0.1)
             if(eachcashier == "1054"):
                y = ser.readline()
                print y
                if(y):
                    parseSerialInput(y)
         #print "end of infinte"
             
      
#      print "\n Received data from Serial line..Parsing"
#      parseSerialInput(x)    
#      x = ser.write('#11;1;\n')
#     posInterface = InterfaceForPos.InterfaceForPos()
#     productPrice =  posInterface.getPriceForBarcode("10043940")
#     print productPrice
#     self.readSerialData()
         
    # provide the form with dictionary as a parameter to the execute method
#     logicObject = Logic.Logic()
#     form.barcode.data = newBarcodeQtyDict
#     feedback = logicObject.execute('hwImitateBuy',form)   