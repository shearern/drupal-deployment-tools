#!/usr/bin/python
'''Nate's Deployment Tools for Drupal instances'''

HELP_DETAIL='''\
+-----------+                                                                                  
|           |                         +-------------------+   +-------------------+
| External  |                         |                   |   |                   |
| Modules/  +--> add_component / +----> Working Directory |   |  Deploy Directory |
| Themes/   |    update_component     |                   |   |                   |
| Libraries |                         +-----------+-------+   +----^--------------+
|           |                                     |                |       
+-----------+                                     |                |       
                                                  v                |       
                                                build            install    
                                                  |                ^
                                                  v                |
                                                 website-1.0.0.drupal

Typical Usage:
    On development workstation, in project directory, run:
        $ drupal-deploy.py init_dev_dir
        $ vim drupal-project.ini
        $ drupal-deploy.py add_component --name=base --type=drupal_module --ver=7.35
            --url=http://ftp.drupal.org/files/projects/drupal-7.35.tar.gz
        $ drupal-deploy.py build --ver=1.0.0
    On server, in deployment directory, run:
        # drupal-deploy.py init_deploy_dir
        # vim drupal-instance.ini
        # drupal-deploy install my-project-1.0.0.drupal

Glossary:
    Deployment Directory    Directory on server where drupal project is deployed to.
                            This directory will have multiple directories including
                            the www/ directory containing the files to serve.
    Deployment Package      A single file representing a specific version of the
                            project code and assets (excluding user files).  This can
                            be "installed" into a Deployment Directory.
    Development Directory   Project directory on development workstation where developer
                            creates the Druapl proejct


'''
# This script is a hook for all of the sub commands

import os
import sys
import gflags
from textwrap import dedent

from drupal_deploy_tools.actions.common import ActionUsageError, ActionAbort


def print_help_header():
    print __doc__.rstrip()
    print ""

def cmd_name():
    return os.path.basename(sys.argv[0])


def list_commands():
    '''List the actions (scripts) that can be invoked'''

    commands = (
        ('add_component',   "Call to create a new component"),
        ('download',        "Download the source for a component")
        ('update_component *',"Pull down the latest version of a component"),
        ('build *',           "Build deployment package from working directory"),
        ('init_deploy_dir *', "Initialize a deployment directory for a Drupal project"),
        ('init_dev_dir',    "Initialize the development directory for a Drupal project"),
        ('install *',         "Install a deployment package into the deployment directory"),
    )

    print "Usage: %s cmd (options)" % (cmd_name())
    print ""
    print "Where cmd is one of:"

    max_cmd_len = max([len(c[0]) for c in commands])
    print_pat = '  %%-%ds  %%s' % (max_cmd_len)
    for cmd, desc in commands:
        print print_pat % (cmd, desc)

    print ""
    print "Type %s help cmd: to get help on a specific command" % (cmd_name())


def load_action(action_name):
    '''Load the requested action module'''
    action_mod = None
    if action_name == 'init_dev_dir':
        from drupal_deploy_tools.actions import init_dev_dir as action_mod
    if action_name == 'add_component':
        from drupal_deploy_tools.actions import add_component as action_mod
    return action_mod


def usage_error(usage_error, action=None):
    print "USAGE ERROR:", usage_error
    if action is None:
        print ""
        list_commands()
    else:
        print ""
        print "Usage: %s %s ARGS" % (os.path.basename(sys.argv[0]), action)
        print gflags.FLAGS
    sys.exit(1)


if __name__ == '__main__':

    # Determine action
    do_help = False
    argv = sys.argv[:]
    action = None
    if len(argv) > 1:
        action = argv[1]
        argv.pop(1)
    else:
        usage_error("An action is required")

    # Handle help first
    if action == 'help' or action == '--help':
        if len(argv) == 1:
            print_help_header()
            print HELP_DETAIL.rstrip()
            print ""
            list_commands()
            sys.exit(0)
        else:
            action = argv[1]
            argv.pop(1)
            do_help = True

    # Load action module
    action_mod = load_action(action)
    if action_mod is None:
        usage_error("Not a valid action: " + action)

    # Parse flags
    argv[0] += ' ' + action
    if do_help:
        print "%s COMMAND:" % (action.upper())
        print ""
        print action_mod.usage_help()
        argv.append('--help')
    try:
        argv = gflags.FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
        #abort("%s\nUsage: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))
        usage_error(str(e), action)

    # Run action
    try:
        action_mod.execute(argv[1:])
    except ActionUsageError, e:
        usage_error(str(e), action)
    except ActionAbort, e:
        print "ERROR:", str(e)
        print "ABORTING"
        sys.exit(3)

    print "Finished"