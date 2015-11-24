import os

from ComponentDevDir import ComponentDevDir

from drupal_deploy_tools.config.ProjectConfig import ProjectConfig

class DevTree(object):
    '''Development folder for this project'''

    def __init__(self, path):
        self.path = path
        self.config = ProjectConfig(self.config_path)


    @property
    def components_path(self):
        return os.path.join(self.path, 'components')
    
    @property
    def config_path(self):
        return os.path.join(self.path, 'drupal-project.ini')


    def list_components(self):
        for dirname in os.listdir(self.components_path):
            path = os.path.join(self.components_path, dirname)
            if os.path.isdir(path):
                if dirname not in ('.', '..'):
                    component = ComponentDevDir(path)
                    if component.is_valid:
                        yield component


    def get_component(self, name):
        path = os.path.join(self.components_path, name)
        if os.path.isdir(path):
            component = ComponentDevDir(path)
            if component.is_valid:
                return component
    
