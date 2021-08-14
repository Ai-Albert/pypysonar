import ast


def parse(code):
    return ast.parse(code)


def getChildren(node):
    return ast.iter_child_nodes(node)


def isNamespace(node):
    # TODO
    return isinstance(node, ast.FunctionDef)


def createNamespace(namespace, name, position):
    assert name and position
    inner_ns = { name : position }
    namespace["ns_"+name] = inner_ns
    return inner_ns


def shouldIndex(node):
    name = _getName(node)
    if not name:
        return False, None, None
    elif _isBuiltin(name):
        return False, None, None
    else:
        assert name
        position = getPosition(node, name)
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
    import builtins
    return name in builtins.__dict__


def getPosition(node, name):
    try:
        row = node.lineno
        col = node.col_offset + _getColOffset(node)
        return row, col, len(name)
    except AttributeError:
        return None


def _getColOffset(node):
    if isinstance(node, ast.FunctionDef):
        return len("def ")  # FIXME
    else:
        return 0
