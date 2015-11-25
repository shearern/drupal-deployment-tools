import gflags
import sys

from ddt.cmds.CommandParmsBase import ParmValidationError


class CommandBase(object):
    '''Class to derive from to create commands that can be run by the tool.

        When creating new commands, be sure to:
            TODO ...
    '''


def commandline_exec(parms_obj, cmd_obj):

    # Define parameters
    parms_obj.define_gflags()

    # Parse Commandline
    try:
        argv = sys.argv[1:]
        argv = gflags.FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
        print("%s\nUsage: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))
        sys.exit(1)

    # Validate parameters
    try:
        parms_obj.read_gflags(argv)
        parms_obj.validate()
    except ParmValidationError, e:
        print("%s\nUsage: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))
        sys.exit(1)

    # Run command
    cmd_obj.execute(parms_obj)