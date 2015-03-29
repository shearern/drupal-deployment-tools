import yaml

from InfoObject import InfoObject

from ModuleReference import ModuleReference
from LibraryReference import LibraryReference
from ThemeReference import ThemeReference

class InstalledPackages(InfoObject):
    '''Prescribes which packages + versions to install (installed-packages.yml)'''
    
    def __init__(self, packages):
        info = self._load_installed_packages()
        self.packages = packages
        super(InstalledPackages, self).__init__('', info)
        
        
    @property
    def drupal_ver(self):
        return self.find_info(('drupal_ver', )).strip('v')
    
    
    def package_ver(self, name, ver_name):
        pkg = self.packages.package(name)
        ver = pkg.version(ver_name)
        return pkg, ver
        
    
    @property
    def modules(self):
        if self.info.has_key('modules'):
            for name, info in self.info['modules'].items():
                path = ".".join((self.path, 'modules', name))
                yield ModuleReference(name, path, info)
                
                
    def get_module_ref(self, name):
        for module in self.modules:
            if module.name == name:
                return module
        raise IndexError("No module named %s" % (name))
                
                
    @property
    def libraries(self):
        if self.info.has_key('libraries'):
            for name, info in self.info['libraries'].items():
                path = ".".join((self.path, 'libraries', name))
                yield LibraryReference(name, path, info)
                
                
    @property
    def themes(self):
        if self.info.has_key('themes'):
            for name, info in self.info['themes'].items():
                path = ".".join((self.path, 'themes', name))
                yield ThemeReference(name, path, info)
                
           
    @property     
    def all_packages(self):
        for pkg in self.modules:
            yield pkg
        for pkg in self.themes:
            yield pkg
        for pkg in self.libraries:
            yield pkg
                
                
    def _load_installed_packages(self):
        with open('installed-packages.yml', 'rt') as fh:
            return yaml.load(fh)
                
                
    def validate(self):
        pass