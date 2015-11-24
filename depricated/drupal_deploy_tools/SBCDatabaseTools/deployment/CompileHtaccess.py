import os
import shutil
import gflags
from textwrap import dedent

from InstallActionBase import InstallActionBase, InstallError

class CompileHtaccess(InstallActionBase):
    '''Generate the .htaccess file'''
    
    def __init__(self, drupal_dir, instance):
        self.drupal_dir = os.path.abspath(drupal_dir)
        self.instance = instance
        
        
    def describe(self):
        return "Compile .htaccess"
    
    
    @property
    def default_htaccess_path(self):
        return os.path.join(self.drupal_dir, '.htaccess');
    
    @property
    def target_path(self):
        return os.path.join(self.drupal_dir, '.htaccess');
    
    
    def _execute(self):
        
        # Read in .htaccess
        src = None
        print "   Reading", self.default_htaccess_path
        with open(self.default_htaccess_path, 'rt') as fh:
            src = [line.rstrip() for line in fh.readlines()]
            
        # Output new .htaccess
        print "   Writing", self.target_path
        with open(self.target_path, 'wt') as fh:
            for line in src:
                print >>fh, line

        return True
