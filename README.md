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


Glossary
--------

    Deployment Directory    Directory on server where drupal project is deployed
                            to.  This directory will have multiple directories
                            including the www/ directory containing the files to
                            serve.
    Deployment Package      A single file representing a specific version of the
                            project code and assets (excluding user files).
                            This can be "installed" into a Deployment Directory.
    Development Directory   Project directory on development workstation where
                            developer creates the Druapl proejct


Deployment Directory Structure
------------------------------

This tools assumes that deployed file structures looks like this:

    apache/         - Web server config files are placed here (apache site config)
    backups/        - Is the directory where user backups are placed
    www/            - All drupal application code is placed here
    manifest        - Lists all of the "installed" files deployed to this site
    instance.ini    - Defines instance specific values such as the DB password



Component Directory Structure
-----------------------------

The components/ directory contains the building blocks of each website (deployed
code and static assets), as well as instructions for adapting these source files
for specific deplyment instances.

The basic structure is:

    component.ini       - Is the configuration for this component.
    source/             - Is the source as delivered from the upstream source
                          $ drupal_deply update_component
    tmp/                - Is created as needed for performing operations



Component Configuration (component.ini)
---------------------------------------

The component.ini file describes the component in the folder, and provides
the input needed for all the drupal_deploy commands.

The basic syntax is:

    [component]
    version = 7.36

    [source]
    source_type = standard
    url = http://ftp.drupal.org/files/projects/drupal-7.36.tar.gz
    archive_root = {name}-{ver}

    [map_1]
    source = *
    dist = www/{1}

Where:

 - **component.version** designates the current upstream version of the component
 - **source.source\_type** designates how drupal\_deploy will retrieve updates.  Values are:
    - **standard**:   Designates the source is downloaded as an archive (tar/zip) and decompressed.
                      This is the method that was desgined for all modules deployed on [drupal.org](drupal.org)
    - **git**:        Designates that source/ is git repository.  Updates involve pulling updates.  *IN DEVELOPMENT*
    - **integrated**: Designates that source/ is a module being developed within the site project tree.
                      No updates will be downloaded from an upstream source
 - **source.url**: Stores the location of the upstream source.
    - For *standard*, this is the URL of the archive
    - For *git*, I think this will be the commit or branch to checkout
 - **source.archive_root**: Is used if *source\_type* is *standard* to designate where the root of the delivered
                            code is at.  For standard drupal modules, the archives typically have all the source
                            in a folder with the same name as the module.  Sometimes, this is different though,
                            for example the version number can be included.
                            This directive instructs the udpate tool which files to extract to the source/ folder.
                            Tokens can be used:
    - *{name}* gets replaced with the module name
    - *{version}* gets replaced with the module version
 
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

Each mapping has at least keys:

 - **source**: maps paths in the source folder.  These will be converted
               to regular expressions, but are expressed using normal
               path "globbing" syntax.  Each * and ? will be converted
               to a matching group in the RE.
               e.g.: panels/*  ->  panels\/(.*)
 - **dist**:   maps the paths to copy files to in the ditribution.
               These are also exprssed using standard path globbing
               syntax, but can also contain back references using the
               {} escaping.
               e.g.: www/site/all/modules/panels/{1}  where {1} will be
                     replaced with group(1) from the RE match.