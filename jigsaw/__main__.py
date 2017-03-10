from jigsaw.representations import Data, Template
from jigsaw.utilities import is_dir, get_name
from argparse import ArgumentParser
from functools import reduce

# generating cmd line arguments
def gather_args():
    parser = ArgumentParser(prog="jigsaw")
    parser.add_argument('-t', '--template')
    parser.add_argument('-d', '--data', nargs="+")
    parser.add_argument("-o", "--output", default="output")
    return parser.parse_args()

# main loop - gather inputs, combine outputs using jinja
if __name__ == "__main__":
    args = gather_args()

    # data is summed up together
    data = reduce(lambda a, b: a + b, [Data(d) for d in args.data])

    # and templates are easy enough to load
    template = Template(args.template)

    # finally, print the results
    template.rebase(args.output)
    template.render(data.dict)
