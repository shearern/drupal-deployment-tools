'''Add a new component to the development tree'''
import os
import gflags
from textwrap import dedent

from common import ActionUsageError, ActionAbort, mkdir
from common_dev_repo import find_dev_repo_obj

from drupal_deploy_tools.config.ComponentConfig import ComponentConfig
from drupal_deploy_tools.config.ComponentFileMap import ComponentFileMap

from py_wizard.PyMainWizard import PyMainWizard
from py_wizard.runner import run_wizard

def usage_help():
    return """\
        USAGE: add_component (options)
    
        Call to create a new component folder in the development repo to track
        a component of the drupal site.  This will create the folder for storing
        the package files and initialize the info file describing the package.

        In general, components contain all of the code and static assets that
        get copied into a drupal deployment and includes:
          - The base Drupal code
          - Modules
          - Themes
          - Libraries

        """

gflags.DEFINE_string('name',
    short_name = 'N',
    default    = None,
    help       = 'Package name')

gflags.DEFINE_string('url',
    short_name = 'U',
    default    = None,
    help       = 'URL to download package file')

gflags.DEFINE_enum('url_type',
    short_name   = 'T',
    default      = None,
    help         = 'What type of path is the url (used when retrieving package)',
    enum_values  = ['drupal_pkg', 'git', 'none'])

gflags.DEFINE_string('version',
    short_name = 'V',
    default    = None,
    help       = 'Current version of package')

gflags.DEFINE_boolean('force',
    short_name = 'f',
    default    = False,
    help       = 'Overwrite package info if package exists')





class CreateComponentWizard(PyMainWizard):
    '''Wizard to guide user through creating component'''

    def execute(self):
        flags = gflags.FLAGS

        tree = find_dev_repo_obj()

        # Make sure components directory exists
        components_path = os.path.join(tree.path, 'components')
        if not os.path.exists(components_path):
            self.inform_user_of_action("Creating " + components_path)
            os.mkdir(components_path)

        name = self.ask_simple('name',
            "Name for this component",
            default = flags.name)

        path = os.path.join(components_path, name)
        if os.path.exists(path):
            raise ActionAbort("%s already exists" % (path))

        # Component type
        stype = self.ask_select('type',
            "How is this compontent obtained",
            options=[
                ComponentConfig.SOURCE_DL_AND_UNPACK,
                "git_clone",
                "custom_integrated"
                ])

        url = None
        if stype == ComponentConfig.SOURCE_DL_AND_UNPACK:
            url = self.ask_simple("url",
                "Url to download")
        else:
            raise NotImplementedError()

        version = self.ask_simple('version',
            "Current version of the component")

        MAP_TPLS = {
            'module': [
                (name, 'sites/all/modules/%s' % (name)),
                ],
            'theme': [
                (name, 'sites/all/themes/%s' % (name)),
                ],
            'library': [
                (name, 'sites/all/libraries/%s' % (name)),
                ],
            'base': [
                ('*', 'www/{1}'),
                ],
            'other': [
                ],
            }

        map_type = self.ask_select('map_type',
            "What type of component is this",
            options=['module', 'theme', 'library', 'base', 'other'])

        # -- Write package attribtes -----------------------------------------

        self.inform_user_of_action("Creating " + path)
        os.mkdir(path)

        config_path = os.path.join(path, 'component.ini')
        config = ComponentConfig(config_path)

        # Version
        config.version = version

        # Source
        config.source_type = stype
        if stype == ComponentConfig.SOURCE_DL_AND_UNPACK:
            config.url = url
        else:
            raise NotImplementedError()

        # Archive root folder
        if map_type == 'base':
            config.archive_root = '{name}-{ver}'

        # Mappings
        for pattern in MAP_TPLS[map_type]:
            config.add_mapping(ComponentFileMap(pattern[0], pattern[1]))

        # self.inform_user_of_action("Writing " + config_path)
        config.save()

        sub_path = os.path.join(path, 'source')
        self.inform_user_of_action("Creating " + sub_path)
        os.mkdir(sub_path)

        # Download
        self.inform_user_of_action("Downloading component source")
        tree.get_component(name).retrieve_source()



def execute(argv):
    run_wizard(CreateComponentWizard())
