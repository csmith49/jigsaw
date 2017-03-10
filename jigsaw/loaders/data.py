import yaml
from jigsaw.utilities import get_extension

# loaders are functions of type String -> Dict
LOADERS = {
    ".yaml": yaml.load
}

def load_file(path):
    # we choose loaders by file extensions
    ext = get_extension(path)
    # get the loader - if there isn't one, bail
    try:
        loader = LOADERS[ext]
    except KeyError:
        raise Exception("Can't find loader for {}".format(path))
    # now actually open the file and get the results
    with open(path, 'r') as f:
        return loader(f.read())
