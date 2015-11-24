import os
import shutil
import gflags
from textwrap import dedent


gflags.DEFINE_string('version',
    short_name = 'V',
    default = None,
    help = 'Version number being compiled')
gflags.MarkFlagAsRequired('version')


from mako.template import Template as MakoTemplate

from InstallActionBase import InstallActionBase, InstallError

class CompileVersionModule(InstallActionBase):
    '''Generate the sbc_version module'''
    
    def __init__(self, drupal_dir, instance):
        self.drupal_dir = os.path.abspath(drupal_dir)
        self.instance = instance
        
        
    def describe(self):
        return "Compile sbc_version"
    
    
    @property
    def asset_path(self):
        return os.path.join(
            os.path.dirname(__file__), '..', '..', 'sbc_version');
    
    
    def _execute(self):
        
        # Create Directory
        target = os.path.join(self.drupal_dir,
                              'sites', 'default', 'modules',
                              'sbc_version')
        if not os.path.exists(target):
            print "   mkdirs", target
            os.makedirs(target)
        
        # Copy in static assets
        for filename in ['sbc_version.info', 'sbc_version.module']:
            src = os.path.join(self.asset_path, filename)
            dst = os.path.join(target, filename)
            print "   cp %s -> %s" % (src, dst)
            shutil.copy(src, dst)
            
        # Write dynamic CSS
        tpl = None
        path = os.path.join(self.asset_path, 'sbc_version.css.tpl')
        with open(path, 'rt') as fh:
            tpl = MakoTemplate(fh.read())
        src = tpl.render(
            name = self.instance.name,
            instance_desc = self.instance.instance_title,
            instance_color = self.instance.instance_color)
        target_path = os.path.join(target, 'sbc_version.css')
        print "   generating", target_path
        with open(target_path, 'wt') as fh:
            fh.write(src)
            
        return True
