import ast


def show_ast():
    with open("a.py", "r") as source:
        text = source.read()
        tree = ast.parse(text)
        namespace = {}
        walk(namespace, tree)
        print(namespace)


def walk(namespace, node, level=0, sep='\t'):
    print(level, ':', sep * level, node)
    name = getName(node)
    position = 0
    if shouldIndex(node):
        position = getPosition(node)
        try:
            namespace[name].append(position)
        except:
            namespace[name] = [position]
    newNS = {}
    if shouldCreateNamespace(node):
        newNS[name] = position
        namespace["NS" + name] = newNS
    for n in ast.iter_child_nodes(node):
        if enterNewNamespace(namespace, node):
            walk(newNS, n, level+1)
        else:
            walk(namespace, n, level+1)


def getName(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return node.name
    elif isinstance(node, ast.arg):
        return node.arg
    elif isinstance(node, ast.Name):
        if isBuiltin(node.id):
            return None
        else:
            return node.id
    else:
        return None


def isBuiltin(name):
    return name in ["print"]


def getPosition(node):
    startPointOffset = 0
    if isinstance(node, ast.FunctionDef):
        startPointOffset = 4
    elif isinstance(node, ast.ClassDef):
        startPointOffset = 6

    startRow = node.lineno
    startCol = node.col_offset + startPointOffset
    endRow = startRow
    endCol = startCol + len(getName(node))

    return startRow, startCol, endRow, endCol


def shouldIndex(node):
    validNodeType = isinstance(node, (ast.FunctionDef, ast.arg, ast.Name))
    validName = getName(node) is not None
    return validNodeType and validName


def shouldCreateNamespace(node):
    return isinstance(node, (ast.FunctionDef, ast.ClassDef))


def enterNewNamespace(namespace, node):
    name = getName(node)
    if name is None:
        return False
    return "NS" + name in namespace.keys()








# {
#     'f': [(1, 5, 1, 6), (7, 4, 7, 5)],
#     'NSf': {
#         'f': (1, 5, 1, 6),
#         'x': [(1, 6, 1, 7), (2, 11, 2, 12)]
#     },
#     'g': [(4, 5, 4, 6), (7, 6, 7, 7)],
#     'NSg': {
#         'g': (4, 5, 4, 6),
#         'x': [(4, 6, 4, 7), (5, 11, 5, 12)]
#     },
#     'x': [(7, 0, 7, 1), (21, 6, 21, 7)],
#     'TimesTwo': [(9, 7, 9, 15), (16, 4, 16, 12)],
#     'NSTimesTwo': {
#         'TimesTwo': (9, 7, 9, 15),
#         '__init__': [(10, 9, 10, 17)],
#         'NS__init__': {
#             '__init__': (10, 9, 10, 17),
#             'self': [(10, 17, 10, 21), (11, 8, 11, 12)],
#             'access': [(10, 23, 10, 29), (11, 17, 11, 23)]
#         },
#         'timesTwo': [(12, 9, 12, 17)],
#         'NStimesTwo': {
#             'timesTwo': (12, 9, 12, 17),
#             'self': [(12, 17, 12, 21), (13, 15, 13, 19)]
#         }
#     },
#     'y': [(16, 0, 16, 1), (17, 0, 17, 1)]
# }