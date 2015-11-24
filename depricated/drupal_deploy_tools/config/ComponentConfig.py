import os
import re

from ConfigBase import ConfigBase
from ComponentFileMap import ComponentFileMap

class ComponentConfig(ConfigBase):
    '''drupal-project.ini contains project level information'''

    SOURCE_DL_AND_UNPACK='standard'     # Typcial module.  Download and unpack it
    SOURCE_GIT='git'                    # Clone a git repository
    SOURCE_INTEGRATED='integrated'      # Module source is part of this project

    def __init__(self, config_path):
        super(ComponentConfig, self).__init__(config_path)

    @property
    def name(self):
        path = os.path.abspath(self.path)
        path = os.path.dirname(path)
        return os.path.basename(path)

    @property
    def source_type(self):
        '''How is the source of this component retrieved'''
        return self._get_ini_prop('source', 'source_type')
    @source_type.setter
    def source_type(self, value):
        self._set_ini_prop('source', 'source_type', value) 

    
    @property
    def url(self):
        '''URL to retrieve component source from'''
        return self._get_ini_prop('source', 'url')
    @url.setter
    def url(self, value):
        self._set_ini_prop('source', 'url', value)


    @property
    def version(self):
        '''Version of the component in source'''
        return self._get_ini_prop('component', 'version')
    @version.setter
    def version(self, value):
        self._set_ini_prop('component', 'version', value)


    @property
    def archive_root(self):
        '''In the archive downloaded, the root folder to copy files from

        Supports token replacements:
            {name}  The name of the component
            {ver}   The version of the component
        '''
        return self._get_ini_prop('source', 'archive_root')
    @archive_root.setter
    def archive_root(self, value):
        self._set_ini_prop('source', 'archive_root', value)
    @property
    def actual_archive_root(self):
        '''The root folder expected for this version.  Replaces tokens'''
        path = self.archive_root
        path = path.replace('{name}', self.name)
        path = path.replace('{ver}', self.version)
        return path
    def translate_archive_path(self, path):
        '''Apply archive_root to convert path to file in archive to source

        For example, in drupal base, there is a file:
            drupal-7.36/includes/actions.inc
        If the .archive_root pattern is {name}-{ver}, then return:
            includes/actions.inc
        '''
        expect = self.actual_archive_root
        if path.startswith('/'):
            path = path[1:]
        if len(expect) == 0 or expect == '.' or expect == './':
            return path
        elif path.startswith(expect):
            path = path[len(expect):]
        else:
            if len(path) > 0:
                msg = "Warning: Archive path %s doesn't match root pattern: %s"
                print msg % (path, self.archive_root)
            else:
                return None

        if path.startswith('/'):
            path = path[1:]

        return path
    

    @property
    def mappings(self):
        '''List of mappings from source/ to dist/'''
        map_groups = list()
        for section in self._list_sections():
            m = ComponentFileMap.MAP_SECTION_PAT.match(section)
            if m:
                map_groups.append( (int(m.group(1)), section) )

        for sort_key, section in sorted(map_groups):
            source_pat = self._get_ini_prop(section, 'source')
            dist_pat = self._get_ini_prop(section, 'dist')
            entry = ComponentFileMap(source_pat, dist_pat)
            entry.ordering = sort_key
            yield entry


    def _find_next_mapping_sort_key(self):
        sort_keys = list()
        for section in self._list_sections():
            m = ComponentFileMap.MAP_SECTION_PAT.match(section)
            if m:
                sort_keys.append(int(m.group(1)))
        if len(sort_keys) == 0:
            return 1
        else:
            return max(sort_keys) + 1


    def add_mapping(self, mapping):
        mapping.ordering = self._find_next_mapping_sort_key()
        section = mapping.config_section
        self._set_ini_prop(section, 'source', mapping.source_pattern)
        self._set_ini_prop(section, 'dist', mapping.dist_pattern)



        
