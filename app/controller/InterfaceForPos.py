
class InterfaceForPos(object):
    '''
     This is a class for interfacing the Pos with shop server.
     
    '''
    def __init__(self):
        pass
    
    def parseForSoftwareImitater(self,formData):
        input = formData.barcode.data
        result = input.split(',')
        barcodeQtyDict = dict()
        
        x = 0   
        while x < (len(result) - 1) :
             barcodeQtyDict[result[x]] = result[x+1] 
             x = x + 2   
             
            
        return barcodeQtyDict  