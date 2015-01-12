#!/usr/bin/python
'''Nate's Deployment Tools for Drupal instances'''
import os
import sys
import gflags

# This script is a hook for all of the sub commands


def cmd_name():
    return os.path.basename(sys.argv[0])


def list_commands():
    '''List the actions (scripts) that can be invoked'''

    commands = (
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
    return action_mod


def usage_error(usage_error):
    print "USAGE ERROR:", usage_error
    list_commands()
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
        usage_error("No module for action: " + action)

    # Parse flags
    argv[0] += ' ' + action
    if do_help:
        print ""
        print "%s DETAILS:" % (action.upper())
        print action_mod.usage_help()
        argv.append('--help')
    try:
        gflags.FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
        abort("%s\nUsage: %s ARGS\n%s" % (e, sys.argv[0], gflags.FLAGS))

    # Run action
    action_mod.execute()

    print "Finished"