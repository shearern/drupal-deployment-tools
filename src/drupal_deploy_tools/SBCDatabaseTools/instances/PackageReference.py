from InfoObject import InfoObject

class PackageReference(InfoObject):
    '''A reference to a package from an instance'''
    def __init__(self, name, path, info, pkg_type):
        self.name = name
        self.pkg_type = pkg_type
        super(PackageReference, self).__init__(path, info)
        assert(pkg_type in ['module', 'library', 'theme'])
    @property
    def ver(self):
        return self.info.strip('v')


