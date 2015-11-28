import os
import shutil
from tempfile import mkdtemp


class TemporaryDirectory(object):
    '''A directory to work in that will get removed'''

    def __init__(self, prefix='tmp', suffix='', dir=None):
        self.__path = mkdtemp(suffix, prefix, dir)
        self.__cleaned = False


    def __del__(self):
        if not self.__cleaned:
            self.clean()


    def clean(self):
        if not self.__cleaned:
            if os.path.exists(self.__path):
                shutil.rmtree(self.__path)

    @property
    def path(self):
        if not self.__cleaned:
            return self.__path