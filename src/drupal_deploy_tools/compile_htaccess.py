#!/usr/bin/python
'''Generates .htaccess for an instance'''

import sys
import os
import gflags
from textwrap import dedent

from instance_parsing import parse_instances_data_dict

def abort(msg=None):
    if msg is not None:
        print "ERROR: " + msg
    print "ABORTING"
    sys.exit(2)

gflags.DEFINE_string('webroot',
    help="Root of Drupal install",
    default=None)
gflags.MarkFlagAsRequired('webroot')


if __name__ == '__main__':

    # Make sure we're in the project root folder
    if not os.path.exists("SBC_DB_FOLDER"):
        abort("Must run in project root")

    # Parse command line options
    task_args = None
    try:
        task_args = gflags.FLAGS(sys.argv)  # parse flags
    except gflags.FlagsError, e:
        abort("%s\nUsage: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))

    # Load Secrets
    instance_name = gflags.FLAGS.instance
    settings = parse_instances_data_dict()
    instance = settings.instance(instance_name)

    # Read in default settings
    source_path = os.path.join(gflags.FLAGS.webroot, '.htaccess')
    if not os.path.exists(source_path):
        abort("Can't find " + source_path)
    src = None
    with open(source_path, 'rt') as fh:
        src = [line.rstrip() for line in fh.readlines()]

    # Perform updates here
#     line_num = src.index('line to edit after')
#     if line_num is None:
#         abort("Failed to find database config section")
#     new_src = dedent("""\
#         $databases['default']['default'] = array(
#            'driver' => 'mysql',
#            'database' => '{database}',
#            'username' => '{username}',
#            'password' => '{password}',
#            'host' => 'localhost',
#            'prefix' => '',
#          );""").format(database=instance.db_name,
#                        username=instance.db_user,
#                        password=instance.db_pass).split("\n")
#     src.pop(line_num)
#     for new_line in reversed(new_src):
#         src.insert(line_num, new_line)

    # Output settings
    target_path = os.path.join(gflags.FLAGS.webroot, '.htaccess')
    print "Writing", target_path
    with open(target_path, 'wt') as fh:
        for line in src:
            print >>fh, line


