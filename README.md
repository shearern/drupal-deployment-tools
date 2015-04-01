Drupal Deployment Tools
=======================

Nate's common tools for deploying Drupal instances.


Summary from src/drupal-depoly.sh
---------------------------------

    +-----------+                                                                                  
    |           |                         +-------------------+   +-------------------+
    | External  |                         |                   |   |                   |
    | Modules/  +--> add_component / +----> Working Directory |   |  Deploy Directory |
    | Themes/   |    update_component     |                   |   |                   |
    | Libraries |                         +-----------+-------+   +----^--------------+
    |           |                                     |                |       
    +-----------+                                     |                |       
                                                      v                |       
                                                    build            install    
                                                      |                ^
                                                      v                |
                                                     website-1.0.0.drupal

Typical Usage
-------------

On development workstation, in project directory, run:

    $ drupal-deploy.py init_dev_dir
    $ vim drupal-project.ini
    $ drupal-deploy.py add_component --name=base --type=drupal_module --ver=7.35
        --url=http://ftp.drupal.org/files/projects/drupal-7.35.tar.gz
    $ drupal-deploy.py build --ver=1.0.0

On server, in deployment directory, run:

    # drupal-deploy.py init_deploy_dir
    # vim drupal-instance.ini
    # drupal-deploy install my-project-1.0.0.drupal

Glossary:
---------

    Deployment Directory    Directory on server where drupal project is deployed
                            to.  This directory will have multiple directories
                            including the www/ directory containing the files to
                            serve.
    Deployment Package      A single file representing a specific version of the
                            project code and assets (excluding user files).
                            This can be "installed" into a Deployment Directory.
    Development Directory   Project directory on development workstation where
                            developer creates the Druapl proejct