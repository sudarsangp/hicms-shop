'''
Created on Sep 10, 2013

@author: dinesh
'''

from abc import ABCMeta,abstractmethod

'''
   This is an abstract class for representing commands like add, remove etc.
     
'''
class Command(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def execute(self):
        pass
    
    
    