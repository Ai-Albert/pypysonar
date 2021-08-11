"""transform ast to a namespace hierachy
"""

import parser


def index(tree):
    return _walk(tree, {}, 0, '\t')


def _walk(node, namespace, level, separator):
    print(level, ':', separator*level, node)

    shouldIndex, name, position = parser.shouldIndex(node)
    if shouldIndex:
        _add(namespace, name, position)
        if parser.isNamespace(node):
            namespace = parser.createNamespace(namespace, name, position)

    for child in parser.getChildren(node):
        _walk(child, namespace, level+1, separator)

    return namespace


def _add(namespace, name, position):
    assert name and position
    try:
        namespace[name].append(position)
    except KeyError:
        namespace[name] = [position]
