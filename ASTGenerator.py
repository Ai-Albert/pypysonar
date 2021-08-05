import ast

def getPosition(node):
    if isinstance(node, ast.FunctionDef):
        startRow = node.lineno
        startCol = node.col_offset + 5
        endRow = node.lineno
        endCol = startCol + len(node.name)
    elif isinstance(node, ast.ClassDef):
        startRow = node.lineno
        startCol = node.col_offset + 7
        endRow = node.lineno
        endCol = startCol + len(node.name)
    else:
        startRow = node.lineno
        startCol = node.col_offset
        endRow = node.end_lineno
        endCol = node.end_col_offset
    return startRow, startCol, endRow, endCol

def getName(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return getattr(node, "name")
    elif isinstance(node, ast.arg):
        return getattr(node, "arg")
    elif isinstance(node, ast.Name) and node.id != "print":
        return getattr(node, "id")
    else:
        return None

def getName2(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return getattr(node, "name")
    elif isinstance(node, ast.arg):
        return getattr(node, "arg")
    elif isinstance(node, ast.Name):
        if isBuiltin(node.id):
            return getattr(node, "id")
        else:
            return None
    else:
        return None

def isBuiltin(name):
    return name in ["print"]

def shouldIndex(node):
    return isinstance(node, (ast.FunctionDef, ast.arg, ast.Name))

def isNewNamespace(node):
    return isinstance(node, ( ast.FunctionDef, ast.ClassDef ))

def walk(namespace, node, level=0, sep='\t'):
    print(level, ':', sep * level, node)
    if getName(node) is not None:
        name = getName(node)
        position = getPosition(node)
        try:
            namespace[name].append(position)
        except:
            namespace[name] = [position]
    newNS = {}
    if isNewNamespace(node):
        newNS[name] = position
        namespace["NS" + name] = newNS
    for n in ast.iter_child_nodes(node):
        if getName(node) is not None:
            walk(newNS, n, level+1)
        else:
            walk(namespace, n, level+1)

def show_ast():
    with open("a.py", "r") as source:
        text = source.read()
        tree = ast.parse(text)
        namespace = {}
        walk(namespace, tree)
        print(namespace)

show_ast()


{
    'f': [(1, 5, 1, 6), (7, 4, 7, 5)],
    'NSf': {
        'f': (1, 5, 1, 6),
        'x': [(1, 6, 1, 7), (2, 11, 2, 12)]
    },
    'g': [(4, 5, 4, 6), (7, 6, 7, 7)],
    'NSg': {
        'g': (4, 5, 4, 6),
        'x': [(4, 6, 4, 7), (5, 11, 5, 12)]
    },
    'x': [(7, 0, 7, 1), (21, 6, 21, 7)],
    'TimesTwo': [(9, 7, 9, 15), (16, 4, 16, 12)],
    'NSTimesTwo': {
        'TimesTwo': (9, 7, 9, 15),
        '__init__': [(10, 9, 10, 17)],
        'NS__init__': {
            '__init__': (10, 9, 10, 17),
            'self': [(10, 17, 10, 21), (11, 8, 11, 12)],
            'access': [(10, 23, 10, 29), (11, 17, 11, 23)]
        },
        'timesTwo': [(12, 9, 12, 17)],
        'NStimesTwo': {
            'timesTwo': (12, 9, 12, 17),
            'self': [(12, 17, 12, 21), (13, 15, 13, 19)]
        }
    },
    'y': [(16, 0, 16, 1), (17, 0, 17, 1)]
}





