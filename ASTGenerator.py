import ast


def show_ast():
    with open("a.py", "r") as source:
        text = source.read()
        tree = ast.parse(text)
        base = {}
        walk(base, tree)
        print(base)


def walk(namespace, node, level=0, sep='\t'):
    print(level, ':', sep * level, node)
    if shouldIndex(node) and getName(node) is not None:
        try:
            namespace[getName(node)].append(getPosition(node))
        except:
            namespace[getName(node)] = [getPosition(node)]
    newNs = {}
    if newNamespace(node):
        newNs[getName(node)] = [getPosition(node)]
        namespace["subNS" + getName(node)] = newNs
    for n in ast.iter_child_nodes(node):
        if getName(node) is not None and namespace.keys().__contains__("subNS" + getName(node)):
            walk(newNs, n, level + 1)
        else:
            walk(namespace, n, level + 1)


def shouldIndex(node):
    return isinstance(node, (ast.FunctionDef, ast.arg, ast.Name))


def newNamespace(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return True
    return False


def getName(node):
    if isinstance(node, ast.FunctionDef):
        return node.name
    elif isinstance(node, ast.arg):
        return node.arg
    elif isinstance(node, ast.Name) and node.id != "print":
        return node.id


def getPosition(node):
    if isinstance(node, ast.FunctionDef):
        startRow = node.lineno
        startCol = node.col_offset + 4
        endRow = node.lineno
        endCol = startCol + len(node.name)
    else:
        startRow = node.lineno
        startCol = node.col_offset
        endRow = node.end_lineno
        endCol = node.end_col_offset
    return startRow, startCol, endRow, endCol

