'''Functions related to working with the development directory'''
import os
import gflags

from common import ActionUsageError
from drupal_deploy_tools.file_obj.DevTree import DevTree

gflags.DEFINE_string('dev_repo',
    short_name = 'w',
    default    = '.',
    help       = 'Path to drupal project development repo working directory')


def _check_is_dev_repo_root(path):
    # Check path
    if os.path.exists(os.path.join(path, 'drupal-project.ini')):
        return True


def _search_up_for_dev_repo_path(path):
    # Check current path
    if _check_is_dev_repo_root(path):
        return path

    # Check parent path
    path = os.path.abspath(path)
    parent = os.path.dirname(path)
    if path != parent:
        return _search_up_for_dev_repo_path(parent)
    else:
        return None


def find_dev_repo_path():
    '''Get the path to the dev_repo to work on'''
    # Use commandline option
    if _check_is_dev_repo_root(gflags.FLAGS.dev_repo):
        return gflags.FLAGS.dev_repo
    # Search from current directory
    if path is None:
        path = _search_up_for_dev_repo_path(os.cwdir)

    if path is None:
        raise ActionUsageError("Not in a drupal development repo")
    return path


def find_dev_repo_obj():
    return DevTree(find_dev_repo_path())

