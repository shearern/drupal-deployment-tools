import os
from subprocess import Popen

from script_lib.TempDirectory import TempDirectory

from InstallActionBase import InstallActionBase, InstallError
from SBCDatabaseTools.deployment.common import package_cache_path

class InstallPackage(InstallActionBase):
    '''Place a package into the appropriate directory to install it'''
    
    PACKAGE_TYPES = ['module', 'theme', 'library']
    
    def __init__(self, drupal_dir, package, ver):
        '''Init
        
        @param drupal_dir: Path to root of Drupal instance
        @param package: Package object from instances.yml
        @param ver: PackageVer object from instances.yml
        '''
        self.target = os.path.abspath(drupal_dir)
        self.pkg = package
        self.ver = ver
        
        self.__tempdir = None
        
        
    def describe(self):
        return "install package %s ver %s" % (self.pkg.name, self.ver.name)
        
        
    def execute(self):
        pwd = os.path.abspath(os.curdir)

        try:        
            super(InstallPackage, self).execute()
        finally:
            # Clean up
            os.chdir(pwd)
            self.__tempdir.remove()
            self.__tempdir = None
        
    
    def _execute(self):
        
        # Create temp dir to decompress to
        self.__tempdir = TempDirectory()
        
        # Find archive
        archive_path = package_cache_path(self.pkg, self.ver)
        archive_path = os.path.join(os.path.abspath(os.curdir), archive_path)
        if not os.path.exists(archive_path):
            raise InstallError("Missing archive: " + str(archive_path))
        
        # Decompress archive
        cmd = None
        os.chdir(self.__tempdir.path)
        if self.ver.ext == 'tar.gz':
            cmd = ['/bin/tar', '-zxvf', archive_path]
        if self.ver.ext == 'zip':
            cmd = ['/usr/bin/unzip', '-v', archive_path]
        self.run(cmd)
        
        # Check for target folder
        if not os.path.exists(self.ver.src_dir_name):
            msg = "Didn't find source dir '%s' in package '%s'"
            msg = msg % (self.ver.src_dir_name, archive_path)
            msg += ".  Found: " + ", ".join(os.listdir(self.__tempdir.path))
            raise Exception(msg)
        
        # Calc destination path
        target = os.path.join(self.target, self.pkg.install_path)
        if not os.path.exists(target):
            os.makedirs(target)
        self.rsync(self.ver.src_dir_name, target)
        
        return True
        
        
        
        
        