import os
from abc import ABCMeta, abstractmethod
from subprocess import Popen

class InstallError(Exception): pass


class InstallActionBase(object):
    '''Base class for defining a generic action to be performed to deplo'''
    __metaclass__ = ABCMeta
    
    DEBUG_FILE = None
    
    @abstractmethod
    def describe(self):
        '''Describe what the action is doing'''
        
        
    def execute(self):
        '''Run the install action'''
        # Record curdir
        pwd = os.path.abspath(os.curdir)

        # Tell user
        print self.describe()
        if InstallActionBase.DEBUG_FILE is not None:
            self.debug("")
            self.debug("=" * 80)
            self.debug(self.describe())
            self.debug("=" * 80)
            
        # Execute
        success = self._execute()
        
        # Return CWD
        os.chdir(pwd)
        
        # Error handling
        if not success:
            raise InstallError("Failed to "+self.describe())
        
    
    def debug(self, msg):
        if InstallActionBase.DEBUG_FILE is not None:
            print >>InstallActionBase.DEBUG_FILE, msg
            
            
    def run(self, cmd):
        # Launch
        p = None
        if InstallActionBase.DEBUG_FILE is not None:
            self.debug("$ " + " ".join(cmd))
            p = Popen(cmd,
                      stdout=InstallActionBase.DEBUG_FILE,
                      stderr=InstallActionBase.DEBUG_FILE)
        else:
            p = Popen(cmd)
            
        # Wait for completion
        p.wait()
        
        # Raise error if failed
        if p.returncode != 0:
            raise InstallError("%s: return %d" % (" ".join(cmd), p.returncode))
        
        
    def rsync(self, from_path, to_path):
        if len(from_path) == 0:
            raise Exception("from_path required")
        if from_path[-1] != '/':
            from_path += '/'
        if len(to_path) == 0:
            raise Exception("to_path required")
        if to_path[-1] != '/':
            to_path += '/'
        self.run(['/usr/bin/rsync', '-av', from_path, to_path])
        
        
    @abstractmethod
    def _execute(self):
        pass