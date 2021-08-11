import ast


def parse(code):
    return ast.parse(code)


def getChildren(node):
    return ast.iter_child_nodes(node)


def isNamespace(node):
    return isinstance(node, ast.FunctionDef)


def createNamespace(namespace, name, position):
    assert name and position
    inner_ns = { name : position }
    namespace["NS" + name] = inner_ns
    return inner_ns


def shouldIndex(node):
    name = _getName(node)
    if not name:
        return False, None, None
    elif _isBuiltin(name):
        return False, None, None
    else:
        position = getPosition(node)
        assert position
        return True, name, position


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
        row = node.lineno
        col = node.col_offset + _getStartOffset(node)
        return row, col, len(_getName(node))
    except:
        return None


def _getStartOffset(node):
    if isinstance(node, ast.FunctionDef):
        return len("def ")  # FIXME
    else:
        return 0
