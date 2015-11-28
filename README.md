Drupal Deployment Tools
=======================

Nate's common tools for deploying Drupal instances.


Summary
-------

This project has the goal of assisting with the creation and maintenance of a
Drupal project.  At a high level, it seeks to assist with:

  1. Managing components (e.g.: modules) quickly and easily such as installing,
     removing, and upgrading.
  2. Converting a development instance into a production instance by helping
     with applying instance specific settings such as database parameters.
  3. Backing up and cloning instances.


Glossary
--------

    Asset                   Assets are the general name for any of the non-user
                            generated files that make up a Drupal install.  This
                            includes PHP code, Images, JavaScript, CSS, etc.
                            Asset files shouldn't be writable by the www-user.

    Component               Any distributed (or locally developed) Drupal asset
                            such as modules, themes, and libraries.  Event the
                            Drupal base code is considered a component
                            
    Backup                  A backup (as related to this tool) is a complete copy
                            of a Drupal instance including compiled files, user
                            files, and database records.
                             
    Instance                Generally refers to a single instalation of a Drupal
                            site.  For example, a single project may be deployed
                            to three instances: production, testing, and development
                            
    Drupal Rool Directory   The directory that the Drupal base archive is copied
                            to, which includes index.php.
                            
    Project Directory       The directory that contains an entire Drupal project.
                            This can be the same as the Drupal Root Directory,
                            or it can be a higher level directory.


Development Workflow
--------------------

 1. First, create a project folder to work from.

     dt_init -n "Project Name"


Project Folder
--------------

The project folder is the directory that contains all of the assets, code and instructions
needed to build a Drupal instance.  This includes:

 - The component source files (components/)
 - instructions for mapping component files to the drupal directory structure
 - Configuration explaning how to access the instances of this Drupal project
 
 
Structure:

    project.yml
    components/
     |--base/
     |   `--(see component section)
     `--panels/
         `--(see component section)
        
Commands:

    $ dt_init -n "Project Name"
    
    
Component Folder
----------------

The assets that make up a Drupal instance are divided into components.  The most
familiar components are modules, but also include:

 - **base**: The base of the Drupal install
 - **module**: A [Drupal module](https://www.drupal.org/project/project_module/categories)
 - **theme**: A [Drupal theme](https://www.drupal.org/project/project_theme)
 - **lib**: Any library.  Often PHP or JavaScript libraries
 - **other**: Any other collection of asset files to copy or compile into the Drupal instance
  
Structure:

    component.yml
    source/
     `--(upstream source files)
  
Commands:

    $ dt_add_component -n component_name -t module|theme|lib|base|other (module-archive.tar.gz)








Component Configuration (component.ini) - TODO: REVAMP
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