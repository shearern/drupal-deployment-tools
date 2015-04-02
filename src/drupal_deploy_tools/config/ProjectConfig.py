import os

from ConfigBase import ConfigBase

class ProjectConfig(ConfigBase):
    '''drupal-project.ini contains project level information'''

    def __init__(self, config_path):
        super(ProjectConfig, self).__init__(config_path)

    @property
    def project_name(self):
        self._get_ini_prop('project', 'name')
    @project_name.setter
    def project_name(self, value):
        self._set_ini_prop('project', 'name', value)

    @property
    def title(self):
        self._get_ini_prop('project', 'title')
    @title.setter
    def title(self, value):
        self._set_ini_prop('project', 'title', value)
        
    