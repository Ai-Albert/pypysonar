from ASTGenerator import show_ast
from Position import Position


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    show_ast()
    x = Position(1, 2, 3, 4)
    print(x.returnPosition())
