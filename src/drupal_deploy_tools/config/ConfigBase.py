import os
import ConfigParser

class ConfigError(Exception): pass

class ConfigBase(object):
    '''Base class for reading and writing configs to file.

    Assumes each instance is a wrapper around a single file.
    '''

    def __init__(self, path):
        self.path = path
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
            print "Saving", self.path
            self._config.write(fh)


    def _has_ini_prop(self, section, key):
        '''Check to see if the property exists in the file

        @param section: Section name to get property from
        @param key: Config item we're looking for
        '''
        if self._config.has_section(section):
            if self._config.has_option(section, key):
                return True
        return False


    def _get_ini_prop(self, secton, key, default=False):
        '''Check to see if the property exists in the file

        @param section: Section name to get property from
        @param key: Config item we're looking for
        @param default: Value to return if config property not set.
            If False (default) then will throw an exception if value doesn't 
            exist.
        '''
        try:
            return self._config.get('project', 'name')
        except ConfigParser.NoSectionError:
            pass

        # No value found:
        if default is False:
            msg = "Config file %s does not have required setting %s in [%s]"
            raise ConfigError(msg % (self.path, key, section))


    def _set_ini_prop(self, section, key, value):
        '''Change a configuration value

        Changed values can be written back to file by calling .save()

        @param section: Section name to get property from
        @param key: Config item we're looking for
        @param value: Value to set
        '''
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, value)
