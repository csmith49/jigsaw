from jigsaw.loaders import data, templates
from jigsaw.utilities.tree import *
from jigsaw import utilities
from functools import reduce

class Data(object):
    def __init__(self, path=None):
        if path is None:
            self.dict = {}
        else:
            tree = utilities.get_tree(path)
            # we ignore top-most directory names, so fix it here
            if isinstance(tree, File):
                forest = [tree]
            else:
                forest = tree.kids
            # convert every element in the forest into a dictionary
            dicts = [self.load_from_tree(f) for f in forest]
            # and then flatten
            self.dict = reduce(lambda p, q: {**p, **q}, dicts)
    def load_from_tree(self, tree):
        f = lambda p: data.load_file(p)
        g = lambda d, k: {d : k}
        return tree_cata(f, g, tree)
    def __add__(self, other):
        out = Data()
        out.dict.update(self.dict)
        out.dict.update(other.dict)
        return out

class TemplateNode(object):
    def __init__(self, path):
        self.name = utilities.get_name(path)
        self.template = templates.load_file(path)
    def render(self, data, base):
        if isinstance(self.template, templates.Resource):
            self.template.render(base)
        else:
            path = utilities.join(base, self.name)
            utilities.dir_check(path)
            with open(path, 'w') as f:
                f.write(self.template.render(data))
        # not really necessary, but why not
        return self

class Template(object):
    def __init__(self, path):
        self.tree = tree_map(TemplateNode, utilities.get_tree(path))
    def rebase(self, base):
        if isinstance(self.tree, File):
            self.tree.name = base
        elif isinstance(self.tree, Directory):
            self.tree.value = base
    def render(self, data):
        def f(path, tree):
            filepath = "."
            for p in path:
                filepath = utilities.join(filepath, p)
            return tree.render(data, filepath)
        return path_map(f, self.tree)
