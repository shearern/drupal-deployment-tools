import os
import shutil
import gflags
from textwrap import dedent

from InstallActionBase import InstallActionBase, InstallError

class CompileSettingsPhp(InstallActionBase):
    '''Generate the settigns.php file'''
    
    def __init__(self, drupal_dir, instance):
        self.drupal_dir = os.path.abspath(drupal_dir)
        self.instance = instance
        
        
    def describe(self):
        return "Compile sbc_version"
    
    
    @property
    def default_settings_path(self):
        return os.path.join(self.drupal_dir,
                            'sites', 'default',
                            'default.settings.php');
    
    @property
    def target_path(self):
        return os.path.join(self.drupal_dir,
                            'sites', 'default',
                            'settings.php');
    
    
    def _execute(self):
        
        # Read in default.settings.php
        default_settings = None
        print "   Reading", self.default_settings_path
        with open(self.default_settings_path, 'rt') as fh:
            default_settings = [line.rstrip() for line in fh.readlines()]
            
        # Update Database Settings
        line_num = default_settings.index('$databases = array();')
        if line_num is None:
            raise InstallError("Failed to find database config section")
        new_src = dedent("""\
            $databases['default']['default'] = array(
               'driver' => 'mysql',
               'database' => '{database}',
               'username' => '{username}',
               'password' => '{password}',
               'host' => 'localhost',
               'prefix' => '',
             );""").format(database=self.instance.db_name,
                           username=self.instance.db_user,
                           password=self.instance.db_pass).split("\n")
        default_settings.pop(line_num)
        for new_line in reversed(new_src):
            default_settings.insert(line_num, new_line)

        # Output new settings.php
        print "   Writing", self.target_path
        with open(self.target_path, 'wt') as fh:
            for line in default_settings:
                print >>fh, line

        return True
