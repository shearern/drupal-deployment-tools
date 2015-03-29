from PackageReference import PackageReference

class ModuleReference(PackageReference):
    '''A reference to a module from an instance'''
    
    def __init__(self, name, path, info):
        super(ModuleReference, self).__init__(name, path, info, 'module')

