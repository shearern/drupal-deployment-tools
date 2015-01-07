'''
Collection of tools specific to deploying SBC Drupal Database
'''
import os
import gflags

from script_lib.common import abort
from script_lib.TempDirectory import TempDirectory


gflags.DEFINE_string('instance',
    help="Instance to retrieve values for",
    default=None)


def check_at_repo_root():
    path = 'SBC_DB_FOLDER'
    if not os.path.exists(path):
        path = os.path.abspath(path)
        abort("missing %s\nMust be run from repository root" % (path))
        
        
def instance_compile_path(instance_name):
    tmpdir = TempDirectory(path=os.path.join('temp', 'compile', instance_name))
    return tmpdir,  tmpdir.path


def package_cache_path(package, ver):
    filename = '%s-%s.%s' % (package.name, ver.name, ver.ext)
    return os.path.join('temp', 'packages', filename)


def get_selected_instance_name():
    '''Get instance to operate on in script'''
    instance_name = None
    try:
        with open('this_instance', 'rt') as fh:
            instance_name = fh.read().strip()
    except:
        print "WARNING: No this_instance file"
    if gflags.FLAGS.instance is not None:
        if instance_name is not None:
            if gflags.FLAGS.instance != instance_name:
                msg = "WARNING: Compiling for instance %s, but this branch is for %s"
                print msg % (gflags.FLAGS.instance, instance_name)
        instance_name = gflags.FLAGS.instance
    return instance_name    
    
          