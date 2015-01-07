import os
from shutil import rmtree

from InstallActionBase import InstallActionBase, InstallError

class DeleteTree(InstallActionBase):
    '''Delete a directory and files under it'''
    
    def __init__(self, path):
        self.__path = path
        assert len(self.__path) > 4
        
    
    def describe(self):
        return "Deleting tree: " + self.__path
    
    
    def _execute(self):
        rmtree(self.__path)
        return not os.path.exists(self.__path)
        
        