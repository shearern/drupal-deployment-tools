import os

from YamlFileObject import YamlFileObject


def get_package_info(x, y, z, a, b, c):
    '''Initialize package info file'''



class Package(YamlFileObject):
    '''Holds info about a single package that can be downloaded'''

    CORE_TYPE = 'core'
    MODULE_TYPE = 'module'
    THEME_TYPE = 'theme'
    LIBRARY_TYPE = 'library'

    DRUPAL_PKG_URL = 'drupal_pkg'
    GIT_URL = 'git'
    NO_URL = 'none'


    def __init__(self, path):
        '''Init 

        @param path: Path to the package directory
        '''
        self.__path = path
        self.__name = os.path.basename(path)

        
    @property
    def name(self):
        return self.__name
    
    @property
    def info_path(self):
        return os.path.join(self.__path, 'pkg.yml')

    @property
    def path(self):
        return self.__path


    # -- YAML Parsing --

    def get_yaml_str(self, info, name, required=True, default=None):
        if info.has_key(name):
            return str(info[name])
        if required:
            raise YamlInfoError(self.path, "Missing required key: %s" % (name))
        else:
            return None


    # def __init__(self, name, path, info):
    #     self.name = name
    #     super(Package, self).__init__(path, info)
    # @property
    # def package_type(self):
    #     return self.info['type']
    # @property
    # def versions(self):
    #     versions = self.find_info(('versions', ))
    #     for name, info in versions.items():
    #         yield PackageVer(name.strip('v'),
    #                          '.'.join([self.path, 'versions', name]),
    #                          info,
    #                          self)
    # def version(self, name):
    #     for versions in self.versions:
    #         if versions.name == name:
    #             return versions
    #     self.syntax_error("Cannot find versions '%s'" % (name))
    
    # @property
    # def install_site(self):
    #     if self.info.has_key('install_site'):
    #         return self.info['install_site'].strip()
    #     return 'all'
    
    # @property
    # def install_path(self):
    #     dname = self.dst_dir_name
    #     if self.package_type == 'module':
    #         return os.path.join('sites', self.install_site,
    #                             'modules', dname)
    #     elif self.package_type == 'theme':
    #         return os.path.join('sites', self.install_site,
    #                             'themes', dname)
    #     elif self.package_type == 'library':
    #         return os.path.join('sites', self.install_site,
    #                             'libraries', dname)
    #     elif self.package_type == 'core':
    #         return ''
    #     else:
    #         msg = "Don't know install path for package type: %s"
    #         raise Exception(msg % (self.package_type)) 
        
        
    # @property
    # def src_dir_name(self):
    #     if self.info.has_key('src_dir_name'):
    #         return self.info['src_dir_name']
    #     return self.name
    # @property
    # def dst_dir_name(self):
    #     if self.info.has_key('dst_dir_name'):
    #         return self.info['dst_dir_name']
    #     return self.name

        
    # @property
    # def url_type(self):
    #     url_type = self.find_info(('url_type', ), required=False)
    #     if url_type is None:
    #         return 'archive_download'
    #     return url_type
    # @property
    # def do_not_cache(self):
    #     if self.info.has_key('do_not_cache'):
    #         return self.info['do_not_cache']
    #     return False
        
        
#    def src_dir_name(self, for_ver=None):
#        '''Name of directory in archive to copy'''
#        name = None
#        if self.info.has_key('src_dir_name'):
#            name = self.info['src_dir_name']
#        else:
#            name = self.name
#        if for_ver is None:
#            name = name.format(ver=for_ver)
#        return name
#    def dst_dir_name(self, for_ver=None):
#        '''Name of directory to copy src_dir to'''
#        name = None
#        if self.info.has_key('dst_dir_name'):
#            name = self.info['dst_dir_name']
#        else:
#            name = self.name
#        if for_ver is None:
#            name = name.format(ver=for_ver)
#        return name

