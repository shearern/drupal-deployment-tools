import os

from exceptions import ProjectFolderError

from ProjectConfigFile import ProjectConfigFile

class ProjectFolder(object):
    '''Wrapper for working with project directory'''

    def __init__(self, path):
        self.__path = os.path.abspath(path)

        # Walk up the directory path until we find a project directory
        while not ProjectFolder.is_dir_a_project_dir(self.__path):
            parent = os.path.dirname(self.__path)
            if parent == self.__path:
                raise ProjectFolderError(
                    "No project folder found at %s or above" % (path))



    @staticmethod
    def calc_config_path_for(path):
        return os.path.join(path, 'dt_project.yml')

    @staticmethod
    def is_dir_a_project_dir(path):
        return os.path.exists(ProjectFolder.calc_config_path_for(path))
