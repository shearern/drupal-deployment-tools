'''Function related to working with the dev_repo'''
import os
import gflags

from common import ActionUsageError

gflags.DEFINE_string('dev_repo',
    short_name = 'D',
    default    = '.',
    help       = 'Path to drupal project development repo working directory')


def _check_is_dev_repo_root(path):
    # Check path
    if os.path.exists(os.path.join(path, 'DRUPAL_DEV_REPO')):
        return path

    # Check parent path
    path = os.path.abspath(path)
    parent = os.path.dirname(path)
    if path != parent:
        return find_dev_repo_root(parent)
    else:
        return None


def find_dev_repo_path():
    '''Get the path to the dev_repo to work on'''
    path = _check_is_dev_repo_root(gflags.FLAGS.dev_repo)
    if path is None:
        raise ActionUsageError("Not in a drupal development repo")
    return path

