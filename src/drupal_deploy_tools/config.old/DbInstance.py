from InfoObject import InfoObject

from ModuleReference import ModuleReference
from LibraryReference import LibraryReference
from ThemeReference import ThemeReference

class DbInstance(InfoObject):
    '''Represents an instance of the database web application'''
    
    def __init__(self, name, path, info):
        self.name = name
        super(DbInstance, self).__init__(path, info)
        
        
    @property
    def url(self):
        return self.find_info(('url', ))
    @property
    def instance_title(self):
        return self.find_info(('title', ))
    @property
    def instance_color(self):
        return self.find_info(('title-color', ), required=False)
    @property
    def ssh_server(self):
        return self.find_info(('ssh', 'server'))
    @property
    def ssh_keyfile(self):
        return self.find_info(('secrets', 'SSH_KEYFILE'))
    @property
    def ssh_user(self):
        return self.find_info(('secrets', 'SSH_USER'))
    @property
    def web_root(self):
        return self.find_info(('web_root', ))
    @property
    def db_name(self):
        return self.find_info(('db', 'name'))
    @property
    def db_user(self):
        return self.find_info(('secrets', 'DB_USER'))
    @property
    def db_pass(self):
        return self.find_info(('secrets', 'DB_PASS'))
                
                
    def validate(self):
        not_none = (
            (self.name,         'name'),
            (self.ssh_server,   'ssh_server'),
            (self.ssh_keyfile,  'ssh_keyfile'),
            (self.ssh_user,     'ssh_user'),
            (self.web_root,     'web_root'),
            (self.db_name,      'db_name'),
            (self.db_user,      'db_user'),
            (self.db_pass,      'db_pass'),
            (self.drupal_ver,   'drupal_ver'),
            )
        for value, name in not_none:
            if value is None:
                self.syntax_error("Value %s is missing" % (name))
