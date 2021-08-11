"""transform an ast to a namespace hierachy
"""

import parser


def index(tree):
    namespace, level, separator = {}, 0, "  "
    _walk(tree, namespace, level, separator)
    return namespace


def _walk(node, namespace, level, separator):
    print(level, ':', separator*level, node)

    should_index, name, position = parser.shouldIndex(node)
    if should_index:
        _add(namespace, name, position)
        if parser.isNamespace(node):
            namespace = parser.createNamespace(namespace, name, position)
    else:
        assert not should_index
        assert not parser.isNamespace(node)

    for child in parser.getChildren(node):
        _walk(child, namespace, level+1, separator)


def _add(namespace, name, position):
    assert name and position
    try:
        namespace[name].append(position)
    except KeyError:
        namespace[name] = [position]
