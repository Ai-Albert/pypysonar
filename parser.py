import ast


def parse(code):
    return ast.parse(code)


def getChildren(node):
    return ast.iter_child_nodes(node)


def shouldIndex(node):
    return isinstance(node, (ast.FunctionDef, ast.arg, ast.Name))


def isNamespace(node):
    return isinstance(node, ast.FunctionDef)


def createNamespace(namespace, name, position):
    inner_ns = { name : position }
    namespace["NS" + name] = inner_ns
    return inner_ns


def getName(node):
    name = _getName(node)
    if _isBuiltin(name):
        return None
    else:
        return name


def _getName(node):
    if isinstance(node, ast.FunctionDef):
        return node.name
    elif isinstance(node, ast.arg):
        return node.arg
    elif isinstance(node, ast.Name):
        return node.id
    else:
        return None


def _isBuiltin(name):
    return name in ("print", )


def getPosition(node):
    try:
        startRow = node.lineno
        startCol = node.col_offset + _getStartOffset(node)
        endRow = startRow
        endCol = startCol + len(getName(node))
        return startRow, startCol, endRow, endCol
    except:
        return None


def _getStartOffset(node):
    # TODO: hack for the "f" function on line #3 in a.py
    if isinstance(node, ast.FunctionDef):
        return 4
    else:
        return 0
