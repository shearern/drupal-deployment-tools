#!/usr/bin/python
'''Nate's Deployment Tools for Drupal instances'''
# This script is a hook for all of the sub commands

import os
import sys
import gflags

from drupal_deploy_tools.actions.common import ActionUsageError


def cmd_name():
    return os.path.basename(sys.argv[0])


def list_commands():
    '''List the actions (scripts) that can be invoked'''

    commands = (
        ('add_package', "Call to create a new package"),
        ('init_dev_repo', "Initialize the development repo of a Drupal project"),
    )

    print "Usage: %s cmd (options)" % (cmd_name())
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
    if action_name == 'init_dev_repo':
        from drupal_deploy_tools.actions import init_dev_repo as action_mod
    if action_name == 'add_package':
        from drupal_deploy_tools.actions import add_package as action_mod
    return action_mod


def usage_error(usage_error, action=None):
    print "USAGE ERROR:", usage_error
    if action is None:
        list_commands()
    else:
        print ""
        print "Usage: %s %s ARGS" % (os.path.basename(sys.argv[0]), action)
        print gflags.FLAGS
    sys.exit(1)


if __name__ == '__main__':

    # Determin action
    do_help = False
    argv = sys.argv[:]
    action = argv[1]
    argv.pop(1)

    # Handle help first
    if action == 'help':
        if len(argv) == 1:
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
        print ""
        print "%s DETAILS:" % (action.upper())
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

    print "Finished"