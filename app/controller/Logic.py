from Command import Command
from CommandFactory import CommandFactory
'''
      This class is the logic for the server.
      Any input from POS is converted to the APIs provided by Logic class. The exact conversion is 
      done by the class InterfaceForPos
      Similarly, input from browser of the client also uses the same APIs of Logic class  
'''

class Logic(object): 
    
    def __init__(self):
        self.newCommandFactory = CommandFactory()

     
    def execute(self,operation,formData):    
         newCommand = self.newCommandFactory.createCommand(operation,formData)
         result = newCommand.execute(formData) 
         return result
