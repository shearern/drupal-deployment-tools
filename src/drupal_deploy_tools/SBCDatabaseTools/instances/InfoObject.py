from common import syntax_error

class InfoObject(object):
    '''Utilities for parsing info dictionaries parsed from YAML'''
    def __init__(self, path, info):
        self.path = path
        self.info = info    # Parsed dict from YAML
        
    def find_info(self, keys, required=True, default=None):
        desc = ".".join(keys)
        if self.info.__class__ is not dict:
            msg = "Expected a dictionary, but got a %s for %s"
            self.syntax_error(msg % (self.info.__class__.__name__,
                                     self.path)) 
        info = self.info.copy()
        for key in keys:
            if info.has_key(key):
                info = info[key]
            else:
                if required:
                    self.syntax_error("Missing required key: " + desc)
                return default
        return info
    
    def syntax_error(self, msg):
        syntax_error(self.path, msg)