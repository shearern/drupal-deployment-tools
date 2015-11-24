import os
from sys import stderr
import subprocess

from script_lib.TempDirectory import TempDirectory

from InstallActionBase import InstallActionBase, InstallError
from SBCDatabaseTools.deployment.common import package_cache_path

class MySqlDump(InstallActionBase):
    '''Run the mysqldump command'''
    
    CACHE_TABLES = [
        'cache',
        'cache_block',
        'cache_bootstrap',
        'cache_field',
        'cache_filter',
        'cache_form',
        'cache_image',
        'cache_libraries',
        'cache_menu',
        'cache_page',
        'cache_path',
        'cache_token',
        'cache_update',
        'cache_views',
        'cache_views_data',
        'ctools_css_cache',
        'ctools_object_cache',
        'search_dataset',
        'search_index',
        'search_node_links',
        'search_total',
        'watchdog',
        ]
    
    def __init__(self, struct_path, data_path, dbname, user, passcode):
        '''Init
        
        @param struct_path: Path to write structure output to
        @param data_path: Path to write data output to
        @param dbname: Database to dump
        @param user: Username to connect to DB as
        @param passcode: Passcode to to connect to DB as
        '''
        self.struct_path = struct_path
        self.data_path = data_path
        self.dbname = dbname
        self.dbuser = user
        self.passcode = passcode
        
        
        
    def describe(self):
        return "Dump %s data to %s" % (self.dbname,
                                       os.path.dirname(self.data_path))
    
    
    def _execute(self):
        
        # Backup Structure
        print "   Dumping structure to", self.struct_path
        with open(self.struct_path, 'wb') as fh:
            cmd = [
                '/usr/bin/mysqldump',
                '-u', self.dbuser,
                '-p' + self.passcode,
                '--no-create-db',
                '--no-data',
                '--tables', self.dbname,
                   ]
            p = subprocess.Popen(cmd, stdout=fh, stderr=stderr)
            p.wait()
            if p.returncode != 0:
                raise InstallError('mysqldump failed')
                
        # Backup Data
        print "   Dumping data to", self.data_path
        with open(self.data_path, 'wb') as fh:
            cmd = [
                '/usr/bin/mysqldump',
                '-u', self.dbuser,
                '-p' + self.passcode,
                '--tables', self.dbname,
                '--skip-extended-insert',
                '--order-by-primary',
                '--no-create-db',
                '--no-create-info',
                ]
            for table_name in self.CACHE_TABLES:
                cmd.append('--ignore-table=%s.%s' % (self.dbname, table_name))
            p = subprocess.Popen(cmd, stdout=fh, stderr=stderr)
            p.wait()
            if p.returncode != 0:
                raise InstallError('mysqldump failed')
        
        return True
        
        
