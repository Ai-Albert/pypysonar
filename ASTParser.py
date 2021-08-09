import ast


def getName(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        return node.name
    elif isinstance(node, ast.arg):
        return node.arg
    elif isinstance(node, ast.Name):
        return getNameNodeId(node)
    else:
        return None


def getNameNodeId(node):
    if isBuiltin(node.id):
        return None
    return node.id


def isBuiltin(name):
    return name in ["print"]


def getPosition(node):
    if shouldIndex(node):
        startPointOffset = getStartPointOffset(node)
        startRow = node.lineno
        startCol = node.col_offset + startPointOffset
        endRow = startRow
        endCol = startCol + len(getName(node))
        return startRow, startCol, endRow, endCol
    else:
        return None


def getStartPointOffset(node):
    if isinstance(node, ast.FunctionDef):
        return 4
    if isinstance(node, ast.ClassDef):
        return 6
    else:
        return 0


def shouldIndex(node):
    validNodeType = isinstance(node, (ast.FunctionDef, ast.arg, ast.Name))
    validName = getName(node) is not None
    return validNodeType and validName


def index(namespace, name, position):
    try:
        namespace[name].append(position)
    except:
        namespace[name] = [position]


def shouldCreateNamespace(node):
    return isinstance(node, (ast.FunctionDef, ast.ClassDef))


def createNamespace(namespace, newNS, name, position):
    newNS[name] = position
    namespace["NS" + name] = newNS
