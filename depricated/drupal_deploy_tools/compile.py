#!/usr/bin/python
'''
compile_and_deploy.py - Deploy application to server

@author: nate
'''
import os
import gflags

from script_lib.common import abort, parse_gflags

from SBCDatabaseTools.deployment.common import check_at_repo_root
from SBCDatabaseTools.deployment.common import instance_compile_path
from SBCDatabaseTools.deployment.common import get_selected_instance_name
from SBCDatabaseTools.deployment.InstallActionBase import InstallActionBase
from SBCDatabaseTools.deployment.InstallActionBase import InstallError

from SBCDatabaseTools.deployment.DeleteTree import DeleteTree
from SBCDatabaseTools.deployment.DeleteFile import DeleteFile
from SBCDatabaseTools.deployment.DownloadPackage import DownloadPackage
from SBCDatabaseTools.deployment.InstallPackage import InstallPackage
from SBCDatabaseTools.deployment.Rsync import Rsync
from SBCDatabaseTools.deployment.CompileVersionModule import CompileVersionModule

from SBCDatabaseTools.instances.Packages import Packages
from SBCDatabaseTools.instances.InstanceSettings import InstanceSettings
from SBCDatabaseTools.instances.InstalledPackages import InstalledPackages

gflags.DEFINE_bool('quick',
    short_name = 'q',
    default = False,
    help = 'Perform update without doing backup')


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
    instance_name = get_selected_instance_name()
    
    # Load settings
    packages = Packages()
    instance_settings = InstanceSettings(instance_name)
    instance = instance_settings.selected_instance
    pkgs_to_install = InstalledPackages(packages)
    
    # Warn if quick
    if flags.quick:
        print "WARNING: Running update in Quick Mode"
        
    # Create temp directory to work in
    tmpdir_handle, target = instance_compile_path(instance.name)
    if os.path.exists(target):
        print "Cleaning out previous %s" % (target)
        try:
            DeleteTree(target).execute()
        except InstallError, e:
            abort(str(e))
    try:
        os.mkdir(target)
    except Exception, e:
        failed_to("create " + target, e)
        
    print ""
    print "Compiling %s to %s" % (instance_name, target)
            
    # Set command debugging
    InstallActionBase.DEBUG_FILE = open('install.debug', 'wt')
            
    # Install Drupal Base
    pkg, ver = pkgs_to_install.package_ver('drupal', pkgs_to_install.drupal_ver)
    try:
        DownloadPackage(pkg, ver).execute()
        InstallPackage(target, pkg, ver).execute()
    except InstallError, e:
        abort(str(e))
        
    # Install all other prescribed packages
    for ref in pkgs_to_install.all_packages:
        try:
            pkg = packages.package(ref.name)
            ver = pkg.version(ref.ver)
            
            DownloadPackage(pkg, ver).execute()
            InstallPackage(target, pkg, ver).execute()
        except InstallError, e:
            abort(str(e))
      
    # Compile sbc_version module
    CompileVersionModule(target, instance).execute()      
    
    
    # Get .gitignore out of Drupal root
    DeleteFile(os.path.join(target, '.gitignore')).execute()
            
            
    # Apply changes to live/ folder
    live = os.path.join(root_path, 'live')
    r = Rsync(target, live, delete=True, ignore=['sites/default/files'])
    r.execute()
    
        
    print "Finished"
    
    
    
        