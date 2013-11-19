from app.controller import Logic,InterfaceForPos
import serial

if __name__ == '__main__':

    while True:    
        ser = serial.Serial('/dev/ttyUSB0')
        x = ser.read()
        print x
    
#     posInterface = InterfaceForPos.InterfaceForPos()
#     productPrice =  posInterface.getPriceForBarcode("10043940")
#     print productPrice
#     self.readSerialData()
         
    # provide the form with dictionary as a parameter to the execute method
#     logicObject = Logic.Logic()
#     form.barcode.data = newBarcodeQtyDict
#     feedback = logicObject.execute('hwImitateBuy',form)