'''Add a new package to the development tree'''
import os
import gflags
from textwrap import dedent

from common import ActionUsageError, mkdir
from common_dev_repo import find_dev_repo_path

from drupal_deploy_tools.config.Package import Package

def usage_help():
    return """\
        USAGE: add_package (options)
    
        Call to create a new package folder in the development repo to track
        a component of the drupal site.  This will create the folder for storing
        the package files and initialize the info file describing the package.
        """

gflags.DEFINE_string('name',
    short_name = 'N',
    default    = None,
    help       = 'Package name')
gflags.MarkFlagAsRequired('name')


gflags.DEFINE_enum('type',
    short_name   = 'C',
    default      = None,
    help         = 'Package type',
    enum_values  = ['module', 'theme', 'library', 'core'])
gflags.MarkFlagAsRequired('type')

gflags.DEFINE_string('url',
    short_name = 'U',
    default    = None,
    help       = 'URL to download package file')

gflags.DEFINE_enum('url_type',
    short_name   = 'T',
    default      = None,
    help         = 'What type of path is the url (used when retrieving package)',
    enum_values  = ['drupal_pkg', 'git', 'none'])
gflags.MarkFlagAsRequired('url_type')

gflags.DEFINE_string('version',
    short_name = 'V',
    default    = None,
    help       = 'Current version of package')

gflags.DEFINE_boolean('force',
    short_name = 'f',
    default    = False,
    help       = 'Overwrite package info if package exists')

PKG_INFO_TEMPLATE = dedent("""\
    ---
    type:   %s
    """)

def execute(argv):
    global PKG_INFO_TEMPLATE
    flags = gflags.FLAGS

    pkg_name = flags.name

    repo_path = find_dev_repo_path()
    pkg_path = os.path.join(repo_path, 'pkgs', pkg_name)

    # Create package directory
    mkdir(pkg_path)

    # Init package info
    path = os.path.join(pkg_path, 'pkg.yml')
    if not os.path.exists(path) or flags.force:
        print "Initializing", path
        with open(path, 'wt') as fh:
            print >>fh, PKG_INFO_TEMPLATE % (pkg_name)
    else:
        raise ActionUsageError("Package %s already eixsts" % (pkg_path))

    # Load package and apply any further info
    pkg = Package(pkg_path)
    if flags.url is not None:
        pkg.url = flags.url
    if flags.version is not None:
        pkg.version = flags.version
    pkg.save_info()

