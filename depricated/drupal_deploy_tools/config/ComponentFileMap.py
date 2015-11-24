import re

class ComponentFileMap(object):
    '''Wraps a single mapping

    Mappings define how to map the structure of the source tar/directory
    the files come in to the Drupal deployment tree where the files should
    be placed when installing.  Each mapping is defined as a section following
    the format [map_#], and mappings are checking in order from lowest to
    greatest.

    Source paths are all produced from the root of the source/ folder.  for 
    example:
        panels
        panels/UPGRADE.txt
        panels/README.txt
        panels/templates
        panels/templates/panels-pane.tpl.php

    Distribution paths are all expressed from the root of the deployment
    directory.  For example:
        www/site/all/modules/panels
        www/site/all/modules/panels/UPGRADE.txt
        www/site/all/modules/panels/README.txt
        www/site/all/modules/panels/templates
        www/site/all/modules/panels/templates/panels-pane.tpl.php

    Each mapping as at least keys:
        source  - maps paths in the source folder.  These will be converted
                  to regular expressions, but are expressed using normal
                  path "globbing" syntax.  Each * and ? will be converted
                  to a matching group in the RE.
                  e.g.: panels/*  ->  panels\/(.*)
        dist    - maps the paths to copy files to in the ditribution.
                  These are also exprssed using standard path globbing
                  syntax, but can also contain back references using the
                  {} escaping.
                  e.g.: www/site/all/modules/panels/{1}  where {1} will be
                        replaced with group(1) from the RE match.
    '''

    MAP_SECTION_PAT=re.compile(r'^map_(\d+)$')

    def __init__(self, source, dist):
        self.__src = None
        self.__src_re_pat = None
        self.__dst = None

        self.source = source
        self.dist = dist
        self.ordering = None

    @property
    def config_section(self):
        return 'map_' + str(self.ordering)


    @property
    def source_pattern(self):
        return self.__src
    

    @property
    def source(self):
        '''Source tree path pattern'''
        return self.__src
    @source.setter
    def source(self, pattern):
        self.__src = pattern
        pattern = pattern.replace('.', '\\.')
        pattern = pattern.replace('/', '\\/')
        pattern = pattern.replace('*', '(.*)')
        pattern = pattern.replace('?', '(.)')
        self.__src_re_pat = re.compile(pattern)

    @property
    def dist_pattern(self):
        return self.__dst

    @property
    def dist(self):
        '''Distribution tree path'''
        return self.__dst
    @dist.setter
    def dist(self, value):
        self.__dst = value
    
    GROUP_PAT=re.compile(r'{(\d+)}')

    @property
    def dist_pat_groups(self):
        '''List the {} groups used in the dist pattern'''
        for i in GROUP_PAT.findall(self.__dst):
            yield int(i), '{' + str(i) + '}'