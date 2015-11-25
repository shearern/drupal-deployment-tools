import os

def validate_dir_path(path):
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        return False
    return True


class DirNotParent(Exception): pass

def subtract_path(parent_path, child_path):
    '''Remove the parent_path from the child path

    For example, given
        parent: /user/home
        child:  /user/home/john/pictures
    return: john/pictures

    '''
    parent = os.path.normpath(parent_path).split('/')
    child  = os.path.normpath(child_path).split('/')

    if len(parent) < len(child):
        raise DirNotParent("%s is not a parent path to %s" % (parent_path, child_path))

    for i, part in enumerate(parent):
        if part != child[i]:
            raise DirNotParent("%s is not a parent path to %s" % (parent_path, child_path))

    return os.path.sep.join(child[len(parent):])






