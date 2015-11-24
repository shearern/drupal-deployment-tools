import os

from InstallActionBase import InstallActionBase, InstallError

class DeleteFile(InstallActionBase):
    '''Delete a single file'''
    
    def __init__(self, path):
        self.__path = path
        assert len(self.__path) > 4
        
    
    def describe(self):
        return "Deleting file: " + self.__path
    
    
    def _execute(self):
        os.unlink(self.__path)
        return not os.path.exists(self.__path)
        
        