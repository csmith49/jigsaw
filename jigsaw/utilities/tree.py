# we represent our files as trees
class File(object):
    def __init__(self, value):
        self.value = value

class Directory(object):
    def __init__(self, value, kids):
        self.value = value
        self.kids = kids

# manipulations of the file system trees
def path_map(f, tree, path=None):
    # fix that annoying last case
    if path is None:
        path = []
    # apply the function on files
    if isinstance(tree, File):
        return File(f(path, tree.value))
    # and collect info on directories
    elif isinstance(tree, Directory):
        new_path = path + [tree.value]
        kids = [path_map(f, k, new_path) for k in tree.kids]
        return Directory(tree.value, kids)
    else:
        raise Exception("That's not a tree!")

def tree_map(f, tree):
    # just ingore the path component
    g = lambda p, t: f(t)
    return path_map(g, tree)

def tree_cata(file_f, dir_f, tree):
    if isinstance(tree, File):
        return file_f(tree.value)
    elif isinstance(tree, Directory):
        kids = [tree_cata(file_f, dir_f, k) for k in tree.kids]
        return dir_f(tree.value, kids)
    else:
        raise Exception("That's not a tree!")
