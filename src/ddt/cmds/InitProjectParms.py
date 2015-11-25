import os
import gflags

from CommandParmsBase import CommandParmsBase
from CommandParmsBase import ParmValidationError
from ..utils import DirNotParent
from ..utils import validate_dir_path
from ..utils import subtract_path


class InitProjectParms(CommandParmsBase):
    '''Parameters for dt_init command'''

    def __init__(self):
        super(InitProjectParms, self).__init__()

        self.project_name = None
        self.project_root = None
        self.drupal_root = None

    def define_gflags(self):
        '''Define any command line flags for this command'''

        gflags.DEFINE_string(
            'name',
            short_name='n',
            help="Project name to display to the user",
            default=None)
        gflags.MarkFlagAsRequired('name')

        gflags.DEFINE_string(
            'project_dir',
            short_name='p',
            help="Directory that project files will be written to",
            default='./')
        gflags.MarkFlagAsRequired('project_dir')
        gflags.RegisterValidator(
            'project_dir',
            validate_dir_path,
            "Project directory is invalid")

        gflags.DEFINE_string(
            'drupal_root',
            short_name='d',
            help="Directory that drupal files are in",
            default='./')
        gflags.MarkFlagAsRequired('drupal_root')
        gflags.RegisterValidator(
            'drupal_root',
            validate_dir_path,
            "Drupal root directory is invalid")


    def read_gflags(self):
        flags = gflags.FLAGS
        self.project_name = flags.name
        self.project_root = flags.project_dir

        try:
            self.drupal_root = subtract_path(self.project_root, flags.drupal_root)
        except DirNotParent, e:
            raise ParmValidationError(str(e))

    def validate(self):
        '''Check provided parameter values and raise ParmValidationError if needed'''
        pass
