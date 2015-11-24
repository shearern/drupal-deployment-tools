import sys
import gflags

def abort(msg=None):
    print ""
    if msg is not None:
        print "ERROR:", msg
    print "ABORTING"
    sys.exit(2)

def usage_error(msg):
    print "USAGE ERROR:", msg
    print ""
    print "Usage: %s ARGS\n%s" % (sys.argv[0], gflags.FLAGS)
    sys.exit(1)
    
    
def parse_gflags(argv=None):
    if argv is None:
        argv = sys.argv
    
    # Parse command line options
    try:
        argv = gflags.FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
        usage_error(str(e))
        
    return argv