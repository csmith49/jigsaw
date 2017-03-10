from jinja2 import Environment, FileSystemLoader
from jigsaw.utilities import get_extension, join, get_name, dir_check
import os

# this is how we interact with files - all relative to the calling directory
file_loader = FileSystemLoader(os.path.abspath("."))

# for parsing tex files, need better block delimiters
tex_loader = Environment(
    block_start_string=r'\block{',
    block_end_string='}',
    variable_start_string=r'\var{',
    variable_end_string='}',
    comment_start_string = '\#{',
	comment_end_string = '}',
    trim_blocks=True,
    autoescape=False,
    loader=file_loader
)

# and a default loader, in case we don't need anything special
default_loader = Environment(loader=file_loader)

# loaders here are jinja2 environments
LOADERS = {
    ".tex": tex_loader
}

# when we can't actually load a template, turn the fp into a resource
class Resource(object):
    def __init__(self, path):
        self.name = get_name(path)
        self.path = path
    def render(self, base):
        from shutil import copyfile
        new_path = join(base, self.name)
        dir_check(new_path)
        copyfile(self.path, new_path)
        return self

def load_file(path):
    # we choose loaders by extension
    ext = get_extension(path)
    # grab the right loader, defaulting if there isn't one
    try:
        loader = LOADERS[ext]
    except KeyError:
        loader = default_loader
    # and then open, parse, and return the resulting templates
    try:
        with open(path, 'r') as f:
            return loader.from_string(f.read())
    except:
        return Resource(path)
