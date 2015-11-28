from abc import ABCMeta, abstractmethod

class InstanceDriver(object):
    '''A driver used to access the files of a Drupal instance

    Since Drupal instances are normally hosted on web servers with varring levales and types of access, different
    drivers can be specified to access the instance files.  The goal is to create a few standard drivers such
    as local files, SFTP, and maybe SSH, and then have a driver that calls on scripts to allow developers to setup
    special functionality.
    '''


