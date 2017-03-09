from jigsaw.loaders import data, templates
from jigsaw import utilities

class Data(object):
    def __init__(self, path):
        tree = utilities.get_dir_tree(path)
        self._dict = self._convert_tree(tree)
    def _convert_tree(self, tree):
        output = {}
        # recurse on the directory tree
        for node in tree:
            # if it's a file, update the output
            if isinstance(node, str):
                output.update(data.load_file(node))
            # otherwise, recurse and it'll be great
            else:
                d, children = node
                output[d] = [self._convert_tree(c) for c in children]
        # aaaand we're done
        return output
    def update(self, other):
        self._dict.update(other._dict)

class Template(object):
    # go ahead and load them up...
    class Node(object):
        def __init__(self, path):
            self.name = utilities.get_name(path)
            self.template = templates.load_file(path)
        def render(self, data, path):
            with open(path, 'r') as f:
                f.write(self.template.render(data))
    # a template is basically a tree of paths w/jinja templates
    def __init__(self, path):
        tree = utilities.get_dir_tree(path)
        self._tree = self._convert_tree(tree)
    def _convert_tree(self, tree):
        output = []
        for node in tree:
            # if we've got a file...
            if isinstance(node, str):
                output.append(Node(node))
            # otherwise, it's a directory
            else:
                d, children = node
                output.append( (d, [self._convert_tree(c) for c in children]))
        return output
    def render(self, base, data):
        for node in self._tree:
            # if we're at a Node:
            if isinstance(node, Node):
                # get our new path
                path = utilities.get_path(base, node.name)
                node.render(data, path)
            # otherwise, recurse with a new base
            else:
                d, children = node
                for c in children:
                    new_base = utilities.get_path(base, d)
                    self.render(new_base, data)
