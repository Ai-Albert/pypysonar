import ast
import ASTParser as parser


def show_ast():
    with open("a.py", "r") as source:
        text = source.read()
        tree = ast.parse(text)
        namespace = {}
        walk(namespace, tree)
        print(namespace)

def walk(namespace, node, level = 0, sep = '\t'):
    print(level, ":", sep * level, node)
    print(namespace)

    name = parser.getName(node)
    position = parser.getPosition(node)

    if parser.shouldIndex(node):
        parser.index(namespace, name, position)

    for n in ast.iter_child_nodes(node):
        if parser.shouldCreateNamespace(node):
            ns = {}
            parser.createNamespace(namespace, ns, name, position)
            walk(ns, n, level + 1)
        else:
            walk(namespace, n, level + 1)




