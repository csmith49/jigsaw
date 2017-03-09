from jinja2 import Environment, FileSystemLoader
from jigsaw.utilities import get_extension

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

def load_file(path):
    # we choose loaders by extension
    ext = get_extension(path)
    # grab the right loader, defaulting if there isn't one
    try:
        loader = LOADERS[ext]
    except KeyError:
        loader = default_loader
    # and then open, parse, and return the resulting templates
    with open(path, 'r') as f:
        return loader.from_string(f.read())
