import re
import yaml
import gflags

from common import syntax_error, abort
from common import find_instances_file
from common import find_secrets_file

from InfoObject import InfoObject
from DbInstance import DbInstance
from Package import Package

class Packages(InfoObject):
    '''Listing of packages that can be installed: packages.yml'''
    
    def __init__(self):
        info = self._load_packages()
        super(Packages, self).__init__('', info)
        
        
    @property
    def packages(self):
        for name, info in self.info.items():
            yield Package(name, '.'.join([self.path, 'packages', name]), info)
            
            
    def package(self, name):
        for package in self.packages:
            if package.name == name:
                return package
        self.syntax_error("Cannot find package '%s'" % (name))
        
        
    
        
        
    def _load_packages(self):
        with open('packages.yml', 'rt') as fh:
            return yaml.load(fh)
                
                
    def validate(self):
        pass