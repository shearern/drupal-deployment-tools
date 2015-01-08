import re
import yaml
import gflags

from common import syntax_error, abort
from common import find_instances_file
from common import find_secrets_file

from InfoObject import InfoObject
from DbInstance import DbInstance
from Package import Package

class InstanceSettings(InfoObject):
    '''Root object representing all parsed settings'''
    
    def __init__(self, instance_name):
        self.instance_name = instance_name
        info = self._load_instance_info()
        super(InstanceSettings, self).__init__('', info)
        
    @property
    def instances(self):
        for inst_name, inst_info in self.info.items():
            yield DbInstance(inst_name,
                             '.'.join([self.path, inst_name]),
                             inst_info)

    def instance(self, name):
        for inst in self.instances:
            if inst.name == name:
                return inst
        self.syntax_error("Cannot find instance '%s'" % (name))
        
        
    @property
    def selected_instance(self):
        return self.instance(self.instance_name)

    def _load_instance_info(self):
        # Parse instances.yml
        info = None
        with open(find_instances_file(), 'rt') as fh:
            info = yaml.load(fh)
    
        # Validate
        if info.__class__ is not dict:
            syntax_error('ROOT', "not a dict")
        if not info.has_key(self.instance_name):
            msg = "instances.yml: Instance '%s' not defined"
            syntax_error(msg % (self.instance_name))
    
        # Bring in secrets
        secret_pat = re.compile(r'^([A-Z_]*)=(.*)$')
        info[self.instance_name]['secrets'] = dict()
        secret_path = find_secrets_file(self.instance_name)
        with open(secret_path, 'rt') as fh:
            for line in fh.readlines():
                line = line.strip()
                if len(line) == 0 or line[0] == '#':
                    continue
                m = secret_pat.match(line)
                if not m:
                    abort("Malformed line in %s: %s" % (secret_path, line))
                info[self.instance_name]['secrets'][m.group(1)] = m.group(2)
        for expected in ['SSH_USER', 'SSH_KEYFILE', 'DB_PASS', 'DB_USER']:
            if not info[self.instance_name]['secrets'].has_key(expected):
                abort("Secrets file %s is missing %s=" % (secret_path, expected))
    
        return info



