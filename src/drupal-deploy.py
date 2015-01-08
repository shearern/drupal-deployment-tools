#!/usr/bin/python
'''Nate's Deployment Tools for Drupal instances'''
import os
import sys

# This script is a hook for all of the sub commands


def cmd_name():
    return os.path.basename(sys.argv[0])


def list_commands():
    commands = (
        ('init_project', "Initialize a new Drupal project for deployment"),
    )

    print "Usage: %s cmd (options)" % (cmd_name())
    print "Where cmd is one of:"

    max_cmd_len = max([len(c[0]) for c in commands])
    print_pat = '  %%-%ds  %%s' % (max_cmd_len)
    for cmd, desc in commands:
        print print_pat % (cmd, desc)

    print ""
    print "Type %s help cmd: to get help on a specific command" % (cmd_name())


def usage_error(usage_error):
    print "USAGE ERROR:", usage_error
    list_commands()
    sys.exit(1)




if __name__ == '__main__':

    try:
        action = sys.argv[1]

        if action == 'init_project':
            # import...
            # module.execute()
            pass

        elif action == 'help':
            if action == 'init_project':
                # import...
                # module.help()
                pass
            else:
                usage_error("Invalid action: " + action)

        else:
            usage_error("Invalid action: " + action)


    except IndexError:
        usage_error("You must specify an action")

    print "Finished"