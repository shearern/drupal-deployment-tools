from .ConfigFileBase import ConfigFileBase


class FileManifest(ConfigFileBase):
    '''A listing of all the non-user files in the project'''

    def __init__(self):