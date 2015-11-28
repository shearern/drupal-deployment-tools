import os
from TemporaryDirectory import TemporaryDirectory

class FileTransaction(object):
    '''Wrap file operations to try and commit or revert all as a unit'''

