'''Initialize development repo for deployment'''
import os
import gflags

from textwrap import dedent

def usage_help():
    return dedent("""\
        Call in a folder to create folders and key Drupal deployment files from
        templates.
        """)

gflags.DEFINE_string('target',
    short_name = 't',
    default    = '.',
    help       = 'Folder to initialize as deployment repo root')


def mkdir(path):
    if not os.path.exists(path):
        print "Creating %s/" % (path)
        os.mkdir(path)


def execute():
    flags = gflags.FLAGS

    mkdir(os.path.join(flags.target, 'pkgs'))
