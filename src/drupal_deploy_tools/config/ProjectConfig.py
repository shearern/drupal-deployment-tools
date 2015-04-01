import os
import ConfigParser

class ProjectConfig(object):
    '''drupal-project.ini contains project level information'''

    def __init__(self, config_path):
        self.path = config_path
        self._config = ConfigParser.RawConfigParser()
        self._modified = False

        if os.path.exists(self.path):
            self.load()


    def load(self):
        with open(self.path, 'rt') as fh:
            print "Loading", path
            self._config.readfp(fh)
            self._modified = False


    def save(self):
        with open(self.path, 'wt') as fh:
            self._config.write(fh)


    @property
    def project_name(self):
        self._config.get('project', 'name')
    @project_name.setter
    def project_name(self, value):
        if not self._config.has_section('project'):
            self._config.add_section('project')
        self._config.set('project', 'name', str(value))

    @property
    def title(self):
        self._config.get('project', 'title')
    @title.setter
    def title(self, value):
        if not self._config.has_section('project'):
            self._config.add_section('project')
        self._config.set('project', 'title', str(value))
        
    