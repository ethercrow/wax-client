
import re
from utils import flatten

re_ptr = re.compile('0x[a-f\d]+')

class UIViewTree(object):

    def __init__(self):
        super(UIViewTree, self).__init__()

        self.root = None
        self.children = []

    def to_list(self):
        return [self.root] + flatten(child.to_list() for child in self.children)

    @classmethod
    def parse_view_line(cls, line):
        result = {}
        m = re_ptr.search(line)
        if not m:
            print('Could not find pointer in ' + line)
        else:
            result.update({'pointer':m.group(0)})
        return result


    @classmethod
    def from_recursive_description(cls, s):
        result = UIViewTree()

        slines = s.split('\n')
        head, tail = slines[0], slines[1:]

        result.root = UIViewTree.parse_view_line(head)

        # strip leading "   | "
        tail = [l[5:] for l in tail]

        child_recursive_descriptions = []

        for l in tail:
            if l.startswith('<'):
                child_recursive_descriptions.append(l)
            else:
                child_recursive_descriptions[-1] += '\n' + l

        result.children = [UIViewTree.from_recursive_description(d) for d
                in child_recursive_descriptions]

        return result

    def __repr__(self):
        return "<UIViewTree root={}, children=[{}]>".format(self.root,
                ", ".join(repr(child) for child in self.children))
