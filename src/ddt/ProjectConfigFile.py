from .ConfigFileBase import ConfigFileBase

from textwrap import dedent

class ProjectConfigFile(ConfigFileBase):
    '''Configuration for a drupal project'''










    TEMPLATE = """\
        ---
            project: {name}

        """

    @staticmethod
    def gen_template(name):
        return dedent(ProjectConfigFile.TEMPLATE).format(
            name=name,
        )
