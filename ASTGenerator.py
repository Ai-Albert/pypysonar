import ast


def walk(node, level=0, sep='\t'):
    print(level, ':', sep * level, node)
    for n in ast.iter_child_nodes(node):
        walk(n, level+1)


def show_ast():
    with open("a.py", "r") as source:
        text = source.read()
        tree = ast.parse(text)
        walk(tree)