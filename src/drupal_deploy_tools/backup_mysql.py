#!/usr/bin/python
'''
backup_mysql.py - Pull down the MySQL data and store it

@author: nate
'''
import os
import gflags

from script_lib.common import abort, parse_gflags

from SBCDatabaseTools.deployment.common import check_at_repo_root
from SBCDatabaseTools.deployment.common import get_selected_instance_name

from SBCDatabaseTools.deployment.MySqlDump import MySqlDump

from SBCDatabaseTools.instances.InstanceSettings import InstanceSettings

gflags.DEFINE_string('root',
    short_name = 'r',
    default = None,
    help = 'Directory to run install from')



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
    
    # Do Backup
    target = os.path.join(root_path, 'live_sql')
    if not os.path.exists(target):
        os.mkdir(target)
    MySqlDump(
        struct_path = os.path.join(target, '01_structure.sql'),
        data_path = os.path.join(target, '02_data.sql'),
        dbname = instance.db_name,
        user = instance.db_user,
        passcode = instance.db_pass).execute()
        
    print "Finished"
    
