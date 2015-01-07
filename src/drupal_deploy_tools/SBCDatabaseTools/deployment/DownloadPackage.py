import os
import urllib2
import shutil

from InstallActionBase import InstallActionBase, InstallError

from SBCDatabaseTools.deployment.common import package_cache_path

class DownloadPackage(InstallActionBase):
    '''Download a package from it's source location'''
    
    def __init__(self, package, ver):
        '''Init
        
        @param drupal_dir: Path to root of Drupal instance
        @param package: Package object from instances.yml
        @param ver: PackageVer object from instances.yml
        '''
        self.pkg = package
        self.ver = ver
        

    def describe(self):
        return "download package %s ver %s" % (self.pkg.name, self.ver.name)
        
    
    def _execute(self):

        # Check already downloaded
        path = package_cache_path(self.pkg, self.ver)
        if not self.ver.do_not_cache:
            if os.path.exists(path):
                return True
        
        # Download
        url_type = self.ver.url_type
        if url_type == 'archive_download':
            print "   downloading", self.ver.url
            try:
                req = urllib2.Request(self.ver.url)
                ifh = urllib2.urlopen(req)
                with open(path, 'wb') as ofh:
                    shutil.copyfileobj(ifh, ofh)
            except Exception, e:
                os.unlink(path)
                raise e
        elif url_type == 'custom':
            print "   packing", self.ver.url
            pwd = os.path.abspath(os.curdir)
            archive_path = os.path.abspath(path)
            parent_dir = os.path.dirname(self.ver.url)
            os.chdir(parent_dir)
            cmd = [
                '/bin/tar',
                '-zcvf', archive_path,
                os.path.basename(self.ver.url),
                ]
            self.run(cmd)
            os.chdir(pwd)
                
        else:
            msg = "Don't know how to retrieve url type '%s' for package %s"
            raise InstallError(msg % (url_type, self.pkg.name))
        
        
        return True
