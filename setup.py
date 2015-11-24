from distutils.core import setup

setup(
    name='drupal-deploy-tools',
    version='4.0.0-dev',
    package_dir = {'': 'src'},
    packages=[
        'ddt',
    ],
    scripts=[
        'src/dt_gui',
        'src/dt_add_component',
    ],
    url='https://github.com/shearern/drupal-deployment-tools',
    license='',
    author='Nathan Shearer',
    author_email='shearern@gmail.com',
    description="Nate's common tools for deploying Drupal instances",
)
