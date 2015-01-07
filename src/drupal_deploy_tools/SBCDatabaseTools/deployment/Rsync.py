import os
from subprocess import Popen

from script_lib.TempDirectory import TempDirectory

from InstallActionBase import InstallActionBase, InstallError
from SBCDatabaseTools.deployment.common import package_cache_path

class Rsync(InstallActionBase):
    '''Sync files from one directory to another'''
    
    def __init__(self, src_dir, dst_dir, delete=False, ignore=None):
        '''Init
        
        @param drupal_dir: Path to root of Drupal instance
        @param package: Package object from instances.yml
        @param ver: PackageVer object from instances.yml
        '''
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.do_delete = delete
        self.ignored = list()
        if ignore is not None:
            self.ignored = ignore[:]
            
        while len(self.src_dir) > 2 and self.src_dir[-1] == '/':
            self.src_dir = self.src_dir[:-1]
        assert(len(self.src_dir) > 2)
        
        while len(self.dst_dir) > 2 and self.dst_dir[-1] == '/':
            self.src_dir = self.dst_dir[:-1]
        assert(len(self.dst_dir) > 2)
        
        
    def describe(self):
        return "Rsync from %s to %s" % (self.src_dir, self.dst_dir)
    
    
    def _execute(self):
        
        cmd = list()
        cmd.append('/usr/bin/rsync')
        cmd.append('-av')
        if self.do_delete:
            cmd.append('--delete')
        for path in self.ignored:
            cmd.append('--exclude')
            cmd.append(path)
        cmd.append(self.src_dir + '/')
        cmd.append(self.dst_dir + '/')
        
        self.run(cmd)
        
        return True
        
        