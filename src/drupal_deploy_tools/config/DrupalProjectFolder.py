import os
import gflags

from drupal_deploy_tools.common import abort
from DrupalDeployFolder import DrupalDeployFolder

gflags.DEFINE_string('project',
    short_name = 'p',
    default    = None,
    help       = 'Path to Drupal project')

class DrupalProjectFolder(object):
    '''Wrapper around the Drupal Project folder being worked on'''
    
    def __init__(self):
        if gflags.FLAGS.project is not None:
            self.__path = os.path.abspath(gflags.FLAGS.project)
        else:
            self.__path = self._find_project_in_parents()

        error = self._validate_project_path()
        if error is not None:
            abort(error)

        self.config = DrupalDeployFolder(self.__path)


    def _validate_project_path(self):
        if self.__path is None:
            return "Not in a Drupal project folder"
        if not os.path.exists(os.path.join(self.__path, 'drupal-deploy')):
            return "%s is not a Drupal project folder" % (self.__path)
        if not os.path.isdir(os.path.join(self.__path, 'drupal-deploy')):
            return "drupal-deploy is not a folder"


    def _find_project_in_parents(self):
        '''Search CWD and above for Drupal project folder'''
        prev_dir = None
        cur_dir = os.path.abspath(os.cwd)

        while prev_dir is None or prev_dir != cur_dir:
            if os.path.exists(os.path.join(cur_dir, 'drupal-deploy')):
                return cur_dir
            prev_dir = cur_dir
            cur_dir = os.path.dirname(cur_dir)


