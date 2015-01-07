from PackageReference import PackageReference

class LibraryReference(PackageReference):
    '''A reference to a library from an instance'''
    def __init__(self, name, path, info):
        super(LibraryReference, self).__init__(name, path, info, 'library')


