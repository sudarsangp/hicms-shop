'''
Created on Sep 10, 2013

@author: dinesh
'''

'''
     This class determines the correct type of command and
     returns the correct type to the caller.
     
'''

class CommandFactory(object):
    
    def createCommand(self,formData):
        print formData
        
    