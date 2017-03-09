from jinja2 import Template, Environment, FileSystemLoader
import os
import yaml

# most of the work goes here - specific functions for loading particular
# kinds of templates and data types

file_loader = FileSystemLoader(os.path.abspath("."))

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

default_loader = Environment(loader=file_loader)

DATAS = {".yaml" : yaml.load}
TEMPLATES = {
    ".tex" : tex_loader,
    ".md" : default_loader
}

# generating cmd line arguments
def gather_args():
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="jigsaw")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("-o", "--output", default="jigsaw.out")

    return parser.parse_args()

# and a slew of helper functions
def get_ext(filename):
    return os.path.splitext(filename)[-1]

def is_template(filename):
    return get_ext(filename) in TEMPLATES

def is_data(filename):
    return get_ext(filename) in DATAS

# now, we can worry about conversion from files to templates and data
def load_template(filename):
    # choose the right template format
    env = TEMPLATES[get_ext(filename)]
    # and then load it
    with open(filename) as f:
        return env.from_string(f.read())

def load_data(*filenames):
    output = {}
    for filename in filenames:
        # get the right data parser (should return a dict)
        parser = DATAS[get_ext(filename)]
        # and update the output
        with open(filename) as f:
            output.update(parser(f.read()))
    return output

# main loop - gather inputs, combine outputs using jinja
if __name__ == "__main__":
    args = gather_args()

    # extract the single template to use
    try:
        template_file = list(filter(is_template, args.inputs))[0]
    except KeyError:
        raise Exception
    # and get the data files
    data_files = list(filter(is_data, args.inputs))

    # we need to convert the template file into a jinja template
    template = load_template(template_file)
    # and the data into an object the template can understand
    data = load_data(*data_files)

    # finally, print the results
    with open(args.output, 'w') as f:
        f.write(template.render(data))
