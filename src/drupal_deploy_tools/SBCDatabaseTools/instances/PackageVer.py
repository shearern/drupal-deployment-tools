from InfoObject import InfoObject

class PackageVer(InfoObject):
    def __init__(self, name, path, info, package):
        self.name = name
        self.package = package
        super(PackageVer, self).__init__(path, info)
    @property
    def url_type(self):
        url_type = self.find_info(('url_type', ), required=False)
        if url_type is None:
            url_type = self.package.url_type
        if url_type is None:
            url_type = 'archive_download'
        return url_type
    @property
    def do_not_cache(self):
        if self.find_info(('do_not_cache', ), required=False, default=False):
            return True
        if self.package.do_not_cache:
            return True
        return False
    @property
    def url(self):
        url = self.find_info(('url', ))
        if self.url_type == 'custom':
            url = 'custom/' + url
        return url
    @property
    def ext(self):
        ext = None
        if self.url_type == 'custom':
            return 'tar.gz'
        for possible in ['.tar.gz', '.zip']:
            if self.url[-1*len(possible):].lower() == possible:
                ext = possible[1:]
        if ext is None:
            self.syntax_error("Failed to determine extension for: " + self.url)
        return ext
    
    @property
    def src_dir_name(self):
        name = self.package.name
        if self.package.src_dir_name is not None:
            name = self.package.src_dir_name
        if self.info.has_key('src_dir_name'):
            name = self.info['src_dir_name']
        
        if '{ver}' in name:
            name = name.replace('{ver}', self.name)
        
        return name
        
    @property
    def dst_dir_name(self):
        if self.info.has_key('dst_dir_name'):
            return self.info['dst_dir_name']
        if self.package.dst_dir_name is not None:
            return self.package.dst_dir_name
        return self.name    
