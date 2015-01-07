#!/usr/bin/python
'''
install.py - Pull down the MySQL data and store it

@author: nate
'''
import os
import gflags

from script_lib.common import abort, parse_gflags

from SBCDatabaseTools.deployment.common import check_at_repo_root
from SBCDatabaseTools.deployment.common import get_selected_instance_name

from SBCDatabaseTools.deployment.CompileSettingsPhp import CompileSettingsPhp
from SBCDatabaseTools.deployment.SetPermissions import SetPermissions
from SBCDatabaseTools.deployment.CompileHtaccess import CompileHtaccess
from SBCDatabaseTools.deployment.MySqlLoad import MySqlLoad

from SBCDatabaseTools.instances.InstanceSettings import InstanceSettings

gflags.DEFINE_string('root',
    short_name = 'r',
    default = None,
    help = 'Directory to run install from')


gflags.DEFINE_boolean('write_db',
    short_name = 'D',
    default = False,
    help = 'Restore the data to the database')



def failed_to(trying, e):
    abort("Failed to %s: %s" % (trying, str(e)))
    
    
if __name__ == '__main__':
    
    # Parse commandline args
    parse_gflags()
    flags = gflags.FLAGS

    # Switch directory if needed
    if flags.root is not None:
        os.chdir(flags.root)
    root_path = os.path.abspath(os.curdir)
        
    # Script Bootstrap
    check_at_repo_root()
    
    # Determine instance we're working on
    instance_name = get_selected_instance_name()

    # Load settings
    instance_settings = InstanceSettings(instance_name)
    instance = instance_settings.selected_instance
    
    # Compile settings.php file
    CompileSettingsPhp(
        drupal_dir = os.path.join(root_path, 'live'),
        instance = instance).execute()
    CompileHtaccess(drupal_dir = os.path.join(root_path, 'live'),
        instance = instance).execute()
    SetPermissions(
        drupal_dir = os.path.join(root_path, 'live')).execute()
        
    if flags.write_db:
        target = os.path.join(root_path, 'live_sql')
        MySqlLoad(
            struct_path = os.path.join(target, '01_structure.sql'),
            data_path = os.path.join(target, '02_data.sql'),
            dbname = instance.db_name,
            user = instance.db_user,
            passcode = instance.db_pass).execute()
    
