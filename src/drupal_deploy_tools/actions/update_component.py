'''Retrieve new upstream source for a comoponet'''
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
        USAGE: update_component --component=name (options)
    
        Call to re-download a components source files and replace the contents
        of the source/ folder.  Most often used when the upstream source for
        the component has been updated, and we want to bring in the new
        version.
        """

gflags.DEFINE_string('component',
    short_name = 'c',
    default    = None,
    help       = 'Name of the component to ugprade')
gflags.MarkFlagAsRequired('component')


class UpdateComponentWizard(PyMainWizard):
    '''Wizard to guide user through updating a component'''

    def execute(self):
        flags = gflags.FLAGS

        tree = find_dev_repo_obj()

        # Load component config
        comp_name = gflags.FLAGS.component
        comp = tree.get_component(comp_name)
        if comp is None:
            raise ActionAbort("Component does not exist: %s" % (comp_name))

        print "Updating", comp.path

        # Ask for new details
        if comp.config.source_type == ComponentConfig.SOURCE_DL_AND_UNPACK:
            comp.config.url = self.ask_simple("url",
                "Url to download",
                default=comp.config.url)

        comp.config.version = self.ask_simple('version',
            "Version for this URL",
            default=comp.config.version)

        comp.config.save()

        # Retrieve new files
        self.inform_user_of_action("Downloading component source")
        comp.retrieve_source()


    def say_goodbye(self):
        pass


def execute(argv):
    run_wizard(UpdateComponentWizard())

