from abc import ABCMeta, abstractmethod

class ParmValidationError(Exception): pass

class CommandParmsBase(object):
    '''Class collect and validate parameter for a commmand within the tool'''

    def __init__(self):
        pass


    @abstractmethod
    def define_gflags(self):
        '''Define any command line flags for this command'''


    @abstractmethod
    def read_gflags(self, args):
        '''Extract values from gflags

        @param args: Arguments left over after parsing gflags
        '''


    @abstractmethod
    def validate(self):
        '''Check provided parameter values and raise ParmValidationError if needed'''

