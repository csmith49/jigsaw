from jigsaw.representations import Data, Template
from argparse import ArgumentParser

# generating cmd line arguments
def gather_args():
    parser = ArgumentParser(prog="jigsaw")
    parser.add_argument('-t', '--template')
    parser.add_argument('-d', '--data', nargs="+")
    parser.add_argument("-o", "--output", default="jigsaw.out")
    return parser.parse_args()

# main loop - gather inputs, combine outputs using jinja
if __name__ == "__main__":
    args = gather_args()

    # data is just a dictionary!
    data = Data()
    for d_path in args.data:
        data.update(Data(d_path))

    # and templates are easy enough to load
    template = Template(args.template)

    # finally, print the results
    template.render(data._dict)
