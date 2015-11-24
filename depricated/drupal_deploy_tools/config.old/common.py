import sys
import os
import gflags

gflags.DEFINE_string('secrets',
    short_name = 'S',
    default = None,
    help = "Path to secrets directory")


def abort(msg=None):
    print ""
    if msg is not None:
        print "ERROR:", msg
    print "ABORTING"
    sys.exit(2)

def find_instances_file():
    if not os.path.exists('instances.yml'):
        abort("Could not find instances.yml")
    return 'instances.yml'


def find_secrets_file(for_instance):
    filename = for_instance + '.server.sh'
    if gflags.FLAGS.secrets is not None:
        path = os.path.join(gflags.FLAGS.secrets, filename)
        if not os.path.exists(path):
            abort("Missing secrets files for instance: " + path)
    else:
        path = os.path.join('secrets', filename)
        if not os.path.exists(path):
            abort("Missing secrets files for instance: " + path)
    return path


def syntax_error(obj, error):
    abort("ERROR in %s: %s: %s" % (find_instances_file(), obj, error))