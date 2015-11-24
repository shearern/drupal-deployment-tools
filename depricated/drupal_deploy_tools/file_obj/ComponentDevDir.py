import os
import shutil
import urllib2
import tarfile

from drupal_deploy_tools.config.ComponentConfig import ComponentConfig

class ComponentDevDir(object):
    '''Represents a component in the development directory'''

    def __init__(self, dir_path):
        self.path = dir_path
        print "Config Path", self.config_path
        self.config = ComponentConfig(self.config_path)

    @property
    def config_path(self):
        return os.path.join(self.path, 'component.ini')
    
    @property
    def is_valid(self):
        if not os.path.exists(self.path):
            return False
        if not os.path.exists(self.config_path):
            return False
        return True


    # -- Temporary Folder: A temporary working location -----------------------

    @property
    def _temp_path(self):
        return os.path.join(self.path, 'tmp')
    

    def clean_tmp(self):
        if os.path.exists(self._temp_path):
            shutil.rmtree(self._temp_path)


    def make_tmp(self):
        '''Create temporary directory to work in'''
        self.clean_tmp()
        os.mkdir(self._temp_path)
        return self._temp_path


    # -- Source Folder: Holds origional component files -----------------------

    @property
    def source_path(self):
        return os.path.join(self.path, 'source')
    

    def clean_source(self):
        if os.path.exists(self.source_path):
            shutil.rmtree(self.source_path)
        os.mkdir(self.source_path)


    # -- Download file source -------------------------------------------------
    
    def retrieve_source(self):
        '''Utility to download/retrieve the source for a component'''
        if self.config.source_type == self.config.SOURCE_DL_AND_UNPACK:

            tmp = self.make_tmp()
            archive_filename = self.config.url.split('/')[-1]
            archive_path = os.path.join(tmp, archive_filename)

            # Download
            print "Downloading", self.config.url
            remotefile = urllib2.urlopen(self.config.url)
            with open(archive_path, 'wb') as fh:
                data = remotefile.read(4096)
                while data:
                    fh.write(data)
                    data = remotefile.read(4096)

            # Unpack tar.gz
            unpack_path = os.path.join(tmp, 'unpacked')
            os.mkdir(unpack_path)

            if archive_filename.lower().endswith('.tar.gz'):


                print "  Uncompressing", archive_filename
                tar = tarfile.open(archive_path)
                tar.extractall(unpack_path)
                tar.close()

            if archive_filename.lower().endswith('.zip'):
                raise NotImplementedError()

            # Move to source/
            print "  Removing", self.source_path
            self.clean_source()
            print "  Copying new source into", self.source_path
            for dirpath, dirnames, filenames in os.walk(unpack_path):

                # Make dir path relative
                if not dirpath.startswith(unpack_path):
                    raise Exception("%s didn't start with %s" % (
                        dirpath, unpack_path))
                rel_dir_path = dirpath[len(unpack_path):]
                while len(rel_dir_path) > 0 and rel_dir_path[0] == '/':
                    rel_dir_path = rel_dir_path[1:]

                # Map to expected source path
                source_rel_dirpath = self.config.translate_archive_path(
                    rel_dir_path)

                if source_rel_dirpath is None:
                    continue

                # Make directories
                for dirname in dirnames:
                    os.mkdir(os.path.join(self.source_path,
                        source_rel_dirpath, dirname))

                # Move files
                for filename in filenames:
                    path = os.path.join(unpack_path, rel_dir_path, filename)
                    new_path = os.path.join(self.source_path, source_rel_dirpath,
                        filename)
                    os.rename(path, new_path)

            self.clean_tmp()

        else:
            msg = 'Source type not implemented: ' + self.config.source_type
            raise NotImplementedError(msg)

#   http://ftp.drupal.org/files/projects/drupal-7.36.tar.gz