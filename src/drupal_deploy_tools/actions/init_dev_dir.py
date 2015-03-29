'''Initialize development repo for deployment'''
import os
import gflags
from textwrap import dedent

from common import mkdir

gflags.DEFINE_string('root',
    short_name = 'D',
    default    = '.',
    help       = 'Folder to initialize as deployment repo root')


def usage_help():
    return dedent("""\
        Call in a folder to create folders and key Drupal deployment files from
        templates.
        """)

def execute(argv):
    flags = gflags.FLAGS

    path = os.path.join(flags.root, 'DRUPAL_DEV_REPO')
    if not os.path.exists(path):
        print "Creating", path
        with open(path, 'wt') as fh:
            msg = "This file marks this folder as " 
            msg += "the root of Drupal development project"
            print >>fh, msg

    mkdir(os.path.join(flags.root, 'pkgs'))
