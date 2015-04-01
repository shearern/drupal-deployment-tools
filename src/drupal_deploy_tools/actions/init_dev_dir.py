'''Initialize development repo for deployment'''
import os
import gflags
from textwrap import dedent

from common import mkdir

from drupal_deploy_tools.config.ProjectConfig import ProjectConfig

from py_wizard.PyMainWizard import PyMainWizard
from py_wizard.runner import run_wizard

gflags.DEFINE_string('root',
    short_name = 'r',
    default    = '.',
    help       = 'Folder to initialize as deployment repo root')


gflags.DEFINE_string('name',
    short_name  = 'N',
    default     = None,
    help        = "Name of project to initialize")

gflags.DEFINE_string('title',
    short_name  = 'T',
    default     = None,
    help        = "Title of project to initialize")


def usage_help():
    return dedent("""\
        Call in a folder to create folders and key Drupal deployment files from
        templates.
        """)


class InitDevDirectory(PyMainWizard):
    '''Wizard to interact with user in setting up the development directory'''

    def execute(self):
        flags = gflags.FLAGS

        # path = os.path.join(flags.root, 'DRUPAL_DEV_DIR')
        # if not os.path.exists(path):
        #     print "Creating", path
        #     with open(path, 'wt') as fh:
        #         msg = "This file marks this folder as " 
        #         msg += "the root of Drupal development project"
        #         print >>fh, msg

        project_config_path = os.path.join(flags.root, 'drupal-project.ini')
        if os.path.exists(project_config_path):
            abort("%s already exists" % (project_config_path))
        config = ProjectConfig(project_config_path)


        # drupal-project.ini
        config.project_name = self.ask_name('name',
            "Name to identify project",
            default = gflags.FLAGS.name)
        config.title = self.ask_simple('title',
            "Title to display for project",
            default = gflags.FLAGS.title)

        config.save()


        # mkdir(os.path.join(flags.root, 'pkgs'))

    def say_goodbye(self):
        pass


def execute(argv):
    run_wizard(InitDevDirectory())