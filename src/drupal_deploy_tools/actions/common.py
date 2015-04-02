'''Common utils for actions'''
import os

class ActionUsageError(Exception): pass

class ActionAbort(Exception): pass

def mkdir(path, verbose=True):
    if not os.path.exists(path):
        if verbose:
            print "Creating %s/" % (path)
        os.mkdir(path)

