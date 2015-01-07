'''
Created on Dec 1, 2014

@author: nate
'''
from tempfile import mkdtemp
from shutil import rmtree

class TempDirectory(object):
    '''Temporary directory that is cleaned out after use'''
    
    def __init__(self, suffix='', prefix='tmp', dir=None, path=None):
        self.__path = mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
        if path is not None:
            self.__path = path
        
    @property
    def path(self):
        return self.__path
        
    def remove(self):
        if self.__path is not None:
            rmtree(self.__path)
            self.__path = None
        
    def __del__(self):
        self.remove()