import os

# we'll often be manipulating weird files, let's make getting the relevant stuff easier
def get_extension(path):
    return os.path.splitext(path)[-1]

def is_dir(path):
    return os.path.isdir(path)

def get_name(path):
    return os.path.basename(path)

# and now one of the more annoying parts, getting the right form of a dir tree
def get_dir_tree(path):
    # if we're a directory, we'll need to recurse
    if is_dir(path):
        output = []
        # walk down just a step in the recursion
        p, dirs, files = os.walk(path)[0]
        # we won't go down the files
        for f in files:
            output.append(os.path.join(p, f))
        # but we will the dirs
        for d in dirs:
            sub_tree = get_dir_tree(os.path.join(p, d))
            output.append( (d, sub_tree) )
    # otherwise we're just a file and we'll return the path
    else:
        return [path]

# and we'll probably have to reconstruct paths at some point
def get_path(base, file):
    return os.path.join(base, file)
