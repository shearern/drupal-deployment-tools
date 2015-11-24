from PackageReference import PackageReference

class ThemeReference(PackageReference):
    '''A reference to a theme from an instance'''
    def __init__(self, name, path, info):
        super(ThemeReference, self).__init__(name, path, info, 'theme')



