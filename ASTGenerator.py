import ast
import ASTParser as parser


def show_ast():
    with open("a.py", "r") as source:
        text = source.read()
        tree = ast.parse(text)
        namespace = {}
        walk(namespace, tree)
        print(namespace)


def walk(namespace, node, level=0, sep='\t'):
    print(level, ':', sep * level, node)
    name = parser.getName(node)
    position = parser.getPosition(node)

    if parser.shouldIndex(node):
        parser.index(namespace, name, position)

    newNS = {}
    createdNS = False
    if parser.shouldCreateNamespace(node):
        parser.createNamespace(namespace, newNS, name, position)
        createdNS = True

    for n in ast.iter_child_nodes(node):
        if createdNS:
            walk(newNS, n, level+1)
        else:
            walk(namespace, n, level+1)