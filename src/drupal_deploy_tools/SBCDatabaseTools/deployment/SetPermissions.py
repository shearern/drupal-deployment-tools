import os
import pwd
import grp
import gflags
from subprocess import Popen

from script_lib.TempDirectory import TempDirectory

from InstallActionBase import InstallActionBase, InstallError
from SBCDatabaseTools.deployment.common import package_cache_path


gflags.DEFINE_boolean('ignore_group',
    default=False,
    help="Ignore group ownership on files")


class SetPermissions(InstallActionBase):
    '''Set the correct permissions on all the files in the Drupal install'''
    
    def __init__(self, drupal_dir):
        '''Init
        
        @param drupal_dir: Path to root of Drupal instance
        '''
        self.target = os.path.abspath(drupal_dir)
        
        
    def describe(self):
        return "Checking permissions for %s" % (self.target)
        
        
    def _execute(self):
        user_files_path = os.path.join(self.target, 'sites', 'default',
                                       'files')
        user_files_path = os.path.realpath(user_files_path)
        
        nate_uid = pwd.getpwnam('nate').pw_uid
        nate_gid = pwd.getpwnam('nate').pw_gid
        www_uid = pwd.getpwnam('www-data').pw_uid
        www_gid = grp.getgrnam('www-data').gr_gid
        
        for dirpath, dirnames, filenames in os.walk(self.target):

            in_user_files = False
            real_dirpath = os.path.realpath(dirpath)
            if real_dirpath[:len(user_files_path)] == user_files_path:
                in_user_files = True
            
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                stats = os.stat(path)
                
                # Check file user
                if stats.st_uid != nate_uid:
                    print "%s not owned by nate" % (path)
            
                # Check file group
                if not gflags.FLAGS.ignore_group:
                    if stats.st_gid != www_gid:
                        print "%s not owned by :www-data" % (path)
                        
                # TODO
            
        return True
        