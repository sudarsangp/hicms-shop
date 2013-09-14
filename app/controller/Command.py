'''
Created on Sep 10, 2013

@author: dinesh
'''
'''
   This is an abstract class for representing commands like add, remove etc.
     
'''

from abc import ABCMeta,abstractmethod
import Feedback

class Command(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def execute(self,formData):
        pass
    
    
    