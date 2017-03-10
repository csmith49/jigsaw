import os
from . import tree

# we'll often be manipulating weird files, let's make getting the relevant stuff easier
def get_extension(path):
    return os.path.splitext(path)[-1]

def is_dir(path):
    return os.path.isdir(path)

def get_name(path):
    return os.path.basename(path)

# and we'll probably have to reconstruct paths at some point
def join(base, file):
    return os.path.join(base, file)

def get_children(path):
    p, dirs, files = list(os.walk(path))[0]
    return [join(p, c) for c in dirs + files]

# and now one of the more annoying parts, getting the right form of a dir tree
def get_tree(path):
    if is_dir(path):
        name = get_name(path)
        kids = [get_tree(c) for c in get_children(path)]
        return tree.Directory(name, kids)
    else:
        return tree.File(path)

# fancy check that makes intermediate directories
def dir_check(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
