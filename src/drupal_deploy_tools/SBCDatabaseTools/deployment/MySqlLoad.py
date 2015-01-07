import os
import subprocess
from shutil import copyfileobj

from script_lib.TempDirectory import TempDirectory

from InstallActionBase import InstallActionBase, InstallError
from SBCDatabaseTools.deployment.common import package_cache_path

class MySqlLoad(InstallActionBase):
    '''Run the mysql command to load back in data'''
    
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
        
        # Create Script to repopulate the database
        script = os.path.join(os.path.dirname(self.data_path),
                              'rebuild.sql')
        with open(script, 'wt') as fh:
            
            # Drop existing database
            print >>fh, "DROP DATABASE IF EXISTS %s;" % (self.dbname)
            print >>fh, "CREATE DATABASE %s;" % (self.dbname)
            print >>fh, "USE %s;" % (self.dbname)
            print >>fh, ""
        
            # Re-Create Structure
            with open(self.struct_path, 'rt') as ifh:
                copyfileobj(ifh, fh)
        
            # Re-Import Data
            with open(self.data_path, 'rt') as ifh:
                copyfileobj(ifh, fh)
                
            # Grant Statement
            print >>fh, ''.join(["GRANT SELECT, INSERT, UPDATE,",
                                 " DELETE, CREATE, DROP, INDEX, ALTER,",
                                 " CREATE TEMPORARY TABLES, LOCK TABLES,",
                                 " SHOW VIEWS",
                                 " ON {db_name}.* TO '{db_user}'@'localhost'",
                                 " IDENTIFIED BY '{db_pass}';",
                                 ]).format(
                                 db_name = self.dbname,
                                 db_user = self.dbuser,
                                 db_pass = self.passcode)
                                 
        # Execute Myql
        try:
            print "-" * 40
            print "To reload DB, run:"
            print "mysql -u root -p < %s" % (script)
            print "-" * 40
            raw_input("Press enter when complete")
        finally:
            os.unlink(script)
            
        
        return True
        
        
