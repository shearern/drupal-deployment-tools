import os
import gflags

from CommandBase import CommandBase, CommandArgumentError
from ..ProjectFolder import ProjectFolder
from ..ProjectConfigFile import ProjectConfigFile

class InitProject(CommandBase):
    '''Command to initialize a Drupal project directory'''

    def __init__(self):

        self.project_name = None
        self.project_root = None

        super(InitProject, self).__init__()


    # -- Parameter Handling --------------------------------------------------------------

    def define_gflags(self):
        '''Define any command line flags for this command'''

        gflags.DEFINE_string(
            'name',
            short_name='n',
            help="Project name to display to the user",
            default=None)

        gflags.DEFINE_string(
            'project_dir',
            short_name='p',
            help="Directory that project files will be written to",
            default='./')

        # gflags.DEFINE_string(
        #     'drupal_root',
        #     short_name='d',
        #     help="Directory that drupal files are in",
        #     default='./')
        # gflags.MarkFlagAsRequired('drupal_root')
        # gflags.RegisterValidator(
        #     'drupal_root',
        #     validate_dir_path,
        #     "Drupal root directory is invalid")


    def ask_presave_questions(self):
        self.project_root = self.ask_path(
            'project_dir',
            "Root of Drupal project",
            must_exist=True,
            must_be_dir=True)


    def _calc_autosave_path(self):
        return os.path.join(self.project_root, '.dt_wiz_answers')


    def validate_parms(self, extra_args):

        if ProjectFolder.is_dir_a_project_dir(self.project_root):
            raise CommandArgumentError(
                'project_dir',
                "%s is already a Drupal project directory" % (self.project_root))
        if not os.path.isdir(self.project_root):
            raise CommandArgumentError(
                'project_dir',
                "%s is not a directory" % (self.project_root))

        self.name = self.ask_simple(
            'name',
            "Name to identify project")

        if len(extra_args) > 0:
            raise  CommandArgumentError(None, "Unknown parameters: %s" % (str(extra_args)))


    # -- Command Execution --------------------------------------------------------------------

    def run_command(self):

        print "Initializing Drupal project in ", self.project_root
        with open(ProjectFolder.calc_config_path_for(self.project_root), 'wt') as fh:
            fh.write(ProjectConfigFile.gen_template(self.name))


    def read_gflags(self):

        flags = gflags.FLAGS

        self.project_name = flags.name
        self.project_root = flags.project_dir


    # -- Question Types ------------------------------------------------------------------




