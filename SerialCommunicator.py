from app.controller import Logic,InterfaceForPos
from app.form.forms import HardwareImitater
from app import app
from ast import literal_eval
import serial
import time, datetime
import os

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
            productPrice =  int((posInterface.getPriceForBarcode(opcode_barcode) * 1000)/10)  # 10043940
            productDisplayQuantity = posInterface.getQuantityForBarcode(opcode_barcode)
            
            responseOpcode = '4'
            responseToSend = '#' + id_string + responseOpcode + ';' + str(productPrice) + ';' + str(productDisplayQuantity) + ';'+ '\n'    
            print responseToSend
            no_of_char = ser.write(responseToSend)  #example '#14;5;7;\n'
            print "Hello World THis is Dinesh"
            time.sleep(0.1)
            return
        
        elif opcode == 6:
            opcode_transactionDetails = parts[2]
            with app.test_request_context():    
                form = HardwareImitater()
                form.transactionDate.data = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
                form.cashierId.data = id_string
                form.customerId.data = "4"
                form.barcode.data = opcode_transactionDetails 
                dummyPosInterface = InterfaceForPos.InterfaceForPos()
                newBarcodeQtyDict =  dummyPosInterface.parseForSoftwareImitater(form)
            
                logicObject = Logic.Logic()
                form.barcode.data = newBarcodeQtyDict
                feedback = logicObject.execute('hwImitateBuy',form)
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
         
     ser = serial.Serial('COM10',timeout=0.1)
#     x = ser.write('#11;1;\n')
#     x = ser.write('#14;5;3\n') 
#    print x
     posInterface1 = InterfaceForPos.InterfaceForPos()
     cashier_id_list = posInterface1.getCashiers()
     list_cashierids = list()
     for cashier in cashier_id_list:
        list_cashierids.append(cashier.cashierId)
      
     while True:
         #sendPriceChange()
         for eachcashier in list_cashierids:
         #print "in infinte"
             #print str(eachcashier)
             x = ser.write('#'+str(eachcashier) + '1;1;\n')
             
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